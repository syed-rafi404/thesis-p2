#!/usr/bin/env bash
# Fetch the published Bengali / Bengali-English speech models we benchmark against.
#
# Downloads go through curl, not Python. A HuggingFace lookup from Python crashes
# this machine with an access violation, which is why the repo runs with
# HF_HUB_OFFLINE=1; see CLAUDE.md. Files land in a plain directory that
# transformers loads with a local path.
#
# Three things this link does that the script has to survive:
#   * HTTP 429 when several files are asked for in a burst.
#   * An intermittent TLS handshake failure on the CDN the weights redirect to.
#   * A 307 redirect whose 282-byte body gets written to disk if curl is not
#     told to follow it, which then looks like a downloaded file. A JSON file is
#     therefore parsed after it arrives and a weights file is size-checked, and
#     anything that fails is thrown away rather than trusted.
#
# Partial weight files are kept and resumed, because a 4 GB download that
# restarts from zero on every handshake error never finishes.

set -u
DEST="${1:-F:/thesisP2/models}"
LOG="$DEST/fetch.log"
mkdir -p "$DEST"

# Smallest first. The link rate-limits after a burst and a big model can sit for
# a long time on one file, so the cheap rows are secured before the 3 GB one.
MODELS="
the-blue-panther/whisper-small-benglish
bangla-speech-processing/BanglaASR
pr0mila-gh0sh/MediBeng-Whisper-Tiny
arif11/bangla-ASR-v5
bengaliAI/tugstugi_bengaliai-asr_whisper-medium
"

FILES="config.json generation_config.json preprocessor_config.json
tokenizer_config.json special_tokens_map.json added_tokens.json
vocab.json merges.txt normalizer.json tokenizer.json
model.safetensors pytorch_model.bin"

# Whisper loads without these; only the weights and the core tokenizer files are
# worth waiting on. Without this an optional file that the link happens to be
# throttling burns forty retries and blocks everything behind it.
OPTIONAL="added_tokens.json normalizer.json tokenizer.json special_tokens_map.json"

say() { echo "[$(date +%H:%M:%S)] $*" >> "$LOG"; }

sane() {                                  # sane <file> -> is this really the file?
  local f="$1"
  [ -s "$f" ] || return 1
  case "$f" in
    *.json)
      python -c "import json,sys; json.load(open(sys.argv[1],encoding='utf-8'))" "$f" \
        >/dev/null 2>&1 || return 1 ;;
    *.safetensors|*.bin)
      [ "$(stat -c%s "$f")" -gt 1000000 ] || return 1 ;;
  esac
  return 0
}

TRIES=40

get() {                                   # get <url> <out> [tries] -> 0 ok, 2 absent, 1 gave up
  local url="$1" out="$2" tries="${3:-$TRIES}" try=0 code rc before after
  while [ "$try" -lt "$tries" ]; do
    before=$( [ -f "$out.part" ] && stat -c%s "$out.part" || echo 0 )
    # -C - resumes the part file, so an aborted attempt keeps its bytes.
    # --speed-limit/--speed-time abort a transfer that has stalled, which this
    # CDN does regularly; without them curl sits on a dead socket until
    # --max-time and no progress is made for an hour and a half.
    # -4 forces IPv4. The weights redirect to us.aws.cdn.hf.co, whose IPv6 route
    # from this machine either times out in the TLS handshake or runs at a
    # quarter of the speed. Measured: 261 KB/s dual-stack against 1009 KB/s on
    # IPv4, plus repeated "SSL/TLS connection timeout" failures.
    code=$(curl -sSL -4 -C - -w '%{http_code}' --max-time 5400 --connect-timeout 30 \
                --speed-limit 20000 --speed-time 45 \
                -o "$out.part" "$url" 2>>"$LOG")
    rc=$?
    [ "$rc" -ne 0 ] && code="000"
    case "$code" in
      200|206|416)
        if sane "$out.part"; then mv -f "$out.part" "$out"; return 0; fi
        # 416 means the range asked for is past the end: a complete part file
        # that failed the check is junk, so start it again from nothing.
        say "    $code but the file is not what it claims to be, starting over"
        rm -f "$out.part" ;;
      404) rm -f "$out.part"; return 2 ;;
      *)   after=$( [ -f "$out.part" ] && stat -c%s "$out.part" || echo 0 )
           say "    $code (curl $rc) at $((after / 1048576)) MB, gained $(( (after - before) / 1024 )) KB" ;;
    esac
    try=$((try + 1))
    [ "$try" -lt "$tries" ] && sleep 10
  done
  return 1
}

say "=== run starting, destination $DEST ==="
for m in $MODELS; do
  name="${m##*/}"
  dir="$DEST/$name"
  mkdir -p "$dir"
  say "$m"
  weights=0
  for f in $FILES; do
    # safetensors comes first in FILES, so once it is in there is no reason to
    # pull the .bin of the same weights as well. Several of these repos ship
    # both and downloading the pair doubles the time for nothing.
    if [ "$f" = "pytorch_model.bin" ] && [ "$weights" -eq 1 ]; then
      say "    skip $f, safetensors already here"
      continue
    fi
    if sane "$dir/$f"; then
      say "    have $f"
      case "$f" in model.safetensors|pytorch_model.bin) weights=1 ;; esac
      continue
    fi
    rm -f "$dir/$f"                       # a leftover that did not pass the check
    tries=$TRIES
    case " $OPTIONAL " in *" $f "*) tries=5 ;; esac
    get "https://huggingface.co/$m/resolve/main/$f" "$dir/$f" "$tries"
    case $? in
      0) say "    got  $f ($(du -h "$dir/$f" 2>/dev/null | cut -f1))"
         case "$f" in model.safetensors|pytorch_model.bin) weights=1 ;; esac ;;
      2) : ;;                             # not in this repo, fine
      *) say "    GAVE UP on $f" ;;
    esac
    sleep 2
  done
  if [ "$weights" -eq 1 ]; then say "  OK   $name"; else say "  FAIL $name: no weights"; fi
  sleep 5
done
say "=== all done ==="
