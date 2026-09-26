"""Write the defense deck's slide files and index.

The deck this built was published as a claude.ai artifact on 2026-09-26 and that artifact
no longer exists, so every /_blob/ id below is dead. The pictures themselves are in img/
here (and in ../slide_images/), so republishing means uploading them again and replacing
the ids. The slide text is the durable part; ../DEFENSE_SLIDES.md is its plain-text twin.
"""
import io, json, os, pathlib

ROOT = pathlib.Path(__file__).parent
SL = ROOT / "project" / "slides"
SL.mkdir(parents=True, exist_ok=True)

# Dead ids, see the module docstring. Kept so the slide files still render locally.
IMG = {
    "baselines": "/_blob/cd208d16845e7a0a0bfb6ff87a8f3ab2",
    "pipeline": "/_blob/30b5cac28c62b8bdce8f658787c0f940",
    "archwhisper": "/_blob/8d872550f3726d2eb36046954fd04780",
    "asrfinal": "/_blob/46eb8806cab698133fd555c034248463",
    "boardreading": "/_blob/db75300c7ddd44cf64acb00fa7e357d7",
    "notesrecall": "/_blob/65d87dc837909f04cd74847b2c8049d3",
    "datacomp": "/_blob/e3a62edfc9899ce3f71877316e2b899b",
    "perlecture": "/_blob/dd5913fcf66662f45db27baf823e7cde",
    "frame": "/_blob/736cb672d59a8290101f95e1cad2b489",
    "raw": "/_blob/146b4db6956861201cd07b1ad608882e",
    "clean": "/_blob/6c33980f2e9743b19741098f421562f9",
    "boxes": "/_blob/4ec793650d92c58ae757c79786e27428",
}

INK, PAPER, DEEP = "#1F2933", "#FBFBF8", "#16202B"
GREEN, ORANGE, MUTED, LINE = "#2A9D4F", "#C25E00", "#52606D", "#DDE2E6"
SANS = "'IBM Plex Sans', Arial, sans-serif"
SERIF = "'EB Garamond', Georgia, serif"

LIGHT = ("background:%s; color:%s; font-family:%s; padding:128px; "
         "display:flex; flex-direction:column; gap:40px" % (PAPER, INK, SANS))
DARK = ("background:%s; color:%s; font-family:%s; padding:128px; "
        "display:flex; flex-direction:column; gap:40px" % (DEEP, PAPER, SANS))


def h2(t, color=None):
    return ('<h2 style="font-family:%s; font-size:68px; font-weight:600; line-height:1.1%s">%s</h2>'
            % (SERIF, ("; color:" + color) if color else "", t))


def eyebrow(t, color=None):
    return ('<p style="font-size:26px; font-weight:600; letter-spacing:2px; '
            'text-transform:uppercase; color:%s">%s</p>' % (color or GREEN, t))


def pic(key, alt, h=560):
    return ('<img src="%s" alt="%s" style="width:1664px; height:%dpx; object-fit:contain">'
            % (IMG[key], alt, h))


def note(txt):
    return "<aside>%s</aside>" % txt


def card(title, body, accent=GREEN):
    return ('<div style="flex:1; display:flex; flex-direction:column; gap:14px; '
            'background:#FFFFFF; padding:34px; border:1px solid %s; border-radius:14px">'
            '<h3 style="font-size:30px; font-weight:600; color:%s">%s</h3>'
            '<p style="font-size:26px; line-height:1.45; color:%s">%s</p></div>'
            % (LINE, accent, title, MUTED, body))


S = {}

S["cover"] = (
 '<section id="cover" style="background:%s; color:%s; font-family:%s; padding:128px; '
 'display:flex; flex-direction:column; justify-content:center; gap:36px">'
 '%s'
 '<h1 style="font-family:%s; font-size:96px; font-weight:600; line-height:1.08">'
 'A Vision-Language Framework for Classroom Content in Two Languages</h1>'
 '<p style="font-size:34px; color:#BFD8D5; line-height:1.4">Turning a recorded Banglish '
 'whiteboard lecture into a usable lecture note</p>'
 '<div style="display:flex; gap:80px">'
 '<div style="display:flex; flex-direction:column; gap:8px">'
 '<p style="font-size:26px; color:#9AA5B1">Presented by</p>'
 '<p style="font-size:28px">Syed Ar Rafi &#183; 24141215</p>'
 '<p style="font-size:28px">Adiba Islam Khan &#183; 24141216</p>'
 '<p style="font-size:28px">Ahsan Habib &#183; 22201027</p></div>'
 '<div style="display:flex; flex-direction:column; gap:8px">'
 '<p style="font-size:26px; color:#9AA5B1">Supervised by</p>'
 '<p style="font-size:28px">Dr. Md. Golam Rabiul Alam</p>'
 '<p style="font-size:28px">Md. Tanzim Reza, co-supervisor</p>'
 '<p style="font-size:26px; color:#9AA5B1">Department of CSE, Brac University</p></div></div>'
 '%s</section>'
 % (DEEP, PAPER, SANS, eyebrow("Undergraduate thesis defense", "#7FCF9B"), SERIF,
    note("Good morning. We built a system that turns a recorded Banglish lecture into "
         "notes a student can actually read. I am X, this is Y and Z, and we will take "
         "about twenty minutes."))
)

S["problem"] = (
 '<section id="problem" data-transition="fade" style="%s">'
 '%s%s'
 '<div style="display:flex; flex-direction:column; gap:20px">'
 '<div style="background:#FFFFFF; padding:30px; border-left:8px solid %s; border-radius:10px">'
 '<p style="font-size:24px; color:%s; font-weight:600">WHAT THE LECTURER SAID</p>'
 '<p style="font-size:32px; line-height:1.4">so ajke amra ei duita gate er inputs and '
 'outputs kivabe create kore sheta dekhbo</p></div>'
 '<div style="background:#FFFFFF; padding:30px; border-left:8px solid %s; border-radius:10px">'
 '<p style="font-size:24px; color:%s; font-weight:600">OFF-THE-SHELF WHISPER &#8594; ENGLISH TRANSLATION</p>'
 '<p style="font-size:32px; line-height:1.4">inputs and outputs create a sheet of a book '
 'and it a logical circuit&#8230;</p></div>'
 '<div style="background:#FFFFFF; padding:30px; border-left:8px solid %s; border-radius:10px">'
 '<p style="font-size:24px; color:%s; font-weight:600">A BENGALI MODEL &#8594; BENGALI SCRIPT</p>'
 '<p style="font-size:32px; line-height:1.4">Bengali letters, even for the English '
 'technical terms</p></div></div>'
 '<p style="font-size:30px; color:%s; line-height:1.4">The class is in two languages at '
 'once. Students write it in the Roman alphabet. <b style="color:%s">No tool produces that.</b></p>'
 '%s</section>'
 % (LIGHT, eyebrow("The problem"), h2("One sentence, three ways"),
    GREEN, MUTED, ORANGE, MUTED, "#B4232C", MUTED, MUTED, INK,
    note("Read the first line aloud in Banglish. Pause. Then show what the two kinds of "
         "existing tool return. Neither is what the student writes."))
)

S["overview"] = (
 '<section id="overview" style="%s">'
 '%s%s'
 '<div style="display:flex; gap:28px">%s%s%s</div>'
 '<p style="font-size:30px; color:%s; line-height:1.45">Banglish is code-mixed Bengali and '
 'English written in the Roman alphabet. It has no standard spelling, and it is what '
 'students actually write in their notebooks.</p>'
 '%s</section>'
 % (LIGHT, eyebrow("What we built"), h2("Video in, a note the student can read out"),
    card("Speech", "A fine-tuned recogniser writes the lecture in romanized Banglish, not "
                   "English and not Bengali script."),
    card("Whiteboard", "Each board is rebuilt from the video with the lecturer removed, "
                       "and read into text by a vision-language model."),
    card("Notes", "One section per board, pointing at numbered regions of the board image, "
                  "with every quotation checked against the transcript."),
    MUTED,
    note("Thirty seconds. Do not explain the pipeline yet, that is slide 6."))
)

S["baselines"] = (
 '<section id="baselines" data-transition="fade" style="%s">'
 '%s%s%s'
 '<p style="font-size:30px; color:%s; line-height:1.4">Five published models, our own 177 '
 'held-out clips. <b style="color:%s">Not one produced romanized Banglish on a single clip.</b> '
 'Four write Bengali script, the fifth translates to English.</p>'
 '%s</section>'
 % (LIGHT, eyebrow("Why this was needed"),
    h2("What existing models actually produce"), pic("baselines", "Baseline comparison", 500),
    MUTED, INK,
    note("This is a measured slide, not a related-work list. The orange bars transliterate "
         "their Bengali to Roman to be fair to them; the best still sits at 47.1 against "
         "our 15.8. If asked: we are not claiming a better Bengali recogniser, we did not "
         "test that."))
)

S["corpus"] = (
 '<section id="corpus" style="%s">'
 '%s%s'
 '<div style="display:flex; gap:40px; align-items:center">'
 '<img src="%s" alt="Corpus by lecturer" style="width:880px; height:500px; object-fit:contain">'
 '<div style="flex:1; display:flex; flex-direction:column; gap:26px">'
 '<div><p style="font-size:64px; font-weight:600; color:%s">44</p>'
 '<p style="font-size:27px; color:%s">lecture recordings, 8.33 hours</p></div>'
 '<div><p style="font-size:64px; font-weight:600; color:%s">5.15 h</p>'
 '<p style="font-size:27px; color:%s">transcribed by hand, word by word, 609 timed segments</p></div>'
 '<div><p style="font-size:64px; font-weight:600; color:%s">3</p>'
 '<p style="font-size:27px; color:%s">lecturers, who are the three of us</p></div></div></div>'
 '%s</section>'
 % (LIGHT, eyebrow("The corpus"), h2("Hand-checked Banglish, because none existed"),
    IMG["datacomp"], GREEN, MUTED, GREEN, MUTED, GREEN, MUTED,
    note("Say plainly that the three lecturers are us. It is in the ethics statement and "
         "it is better said than discovered. About an hour of human checking per ten "
         "minutes of video."))
)

S["pipeline"] = (
 '<section id="pipeline" style="%s">'
 '%s'
 '<img src="%s" alt="The full pipeline" style="width:1664px; height:680px; object-fit:contain">'
 '%s</section>'
 % (LIGHT, h2("The system, end to end"), IMG["pipeline"],
    note("Walk it once, top to bottom, about forty seconds. Left column speech, right "
         "column vision, they meet at the note model. The grey box on the left is "
         "training: it happens once, not for every lecture."))
)

S["archwhisper"] = (
 '<section id="archwhisper" style="%s">'
 '%s%s'
 '<img src="%s" alt="Whisper with LoRA" style="width:1664px; height:520px; object-fit:contain">'
 '<p style="font-size:29px; color:%s; line-height:1.4">Whisper large-v3-turbo, weights '
 'frozen. LoRA rank 16 on the query and value projections. <b style="color:%s">809 million '
 'parameters untouched; only the small matrices train.</b></p>'
 '%s</section>'
 % (LIGHT, eyebrow("Speech"), h2("How the recogniser was adapted"), IMG["archwhisper"],
    MUTED, INK,
    note("The picture on the left is the real log-Mel array of one held-out clip. Every "
         "size in the diagram is read from the model's configuration file."))
)

S["prereg"] = (
 '<section id="prereg" data-transition="fade" style="%s">'
 '%s%s'
 '<div style="display:flex; flex-direction:column; gap:18px; background:#1E2B38; '
 'padding:44px; border:1px solid #33465A; border-radius:16px">'
 '<p style="font-size:26px; color:#7FCF9B; font-weight:600; letter-spacing:1px">'
 'WRITTEN DOWN BEFORE ANY RUN</p>'
 '<p style="font-size:31px; line-height:1.5">Validation lectures fixed &#8594; 2, 12 and 14, '
 'never used for testing</p>'
 '<p style="font-size:31px; line-height:1.5">Search order fixed &#8594; learning rate, rank, '
 'layers, epochs, seed</p>'
 '<p style="font-size:31px; line-height:1.5">Acceptance rule fixed &#8594; keep the default '
 'unless the winner beats it by more than the seed spread</p></div>'
 '<p style="font-size:32px; color:#BFD8D5; line-height:1.4">The test set was touched '
 '<b style="color:%s">once</b>, at the end, with two seeds.</p>'
 '%s</section>'
 % (DARK, eyebrow("Method", "#7FCF9B"), h2("Settings chosen before any result was seen", PAPER),
    PAPER,
    note("This slide buys credibility for everything after it. Pre-registration is unusual "
         "at undergraduate level and the panel will notice."))
)

S["asrresult"] = (
 '<section id="asrresult" style="%s">'
 '%s%s%s'
 '<p style="font-size:30px; color:%s; line-height:1.4"><b style="color:%s">CER 67.7 to 15.8 '
 'and 16.0 per cent</b> across two seeds, six whole lectures never seen in training, 177 '
 'clips, better on 164 and 167 of them.</p>'
 '<p style="font-size:28px; color:%s; line-height:1.4">At the rate the pre-registered search '
 'chose, one seed reached 16.2 and <b style="color:#B4232C">the other collapsed to 118.7 per '
 'cent</b> with 82 runaway clips. The pair above is the runner-up rate, run after we saw '
 'that. The report says so.</p>'
 '%s</section>'
 % (LIGHT, eyebrow("Speech"), h2("The speech result"), pic("asrfinal", "ASR result", 430),
    MUTED, INK, MUTED,
    note("Volunteer the diverged seed yourself. A panel that hears you say it stops looking "
         "for what else you hid. This is the single most important delivery on the deck."))
)

S["unseen"] = (
 '<section id="unseen" style="%s">'
 '%s%s'
 '<div style="display:flex; gap:32px">'
 '<div style="flex:1; background:#FFFFFF; padding:44px; border:1px solid %s; border-radius:14px">'
 '<p style="font-size:27px; color:%s">Test lecturers heard in training</p>'
 '<p style="font-size:76px; font-weight:600; color:%s">67.7 &#8594; 15.8</p>'
 '<p style="font-size:26px; color:%s">character error rate, per cent</p></div>'
 '<div style="flex:1; background:#FFFFFF; padding:44px; border:1px solid %s; border-radius:14px">'
 '<p style="font-size:27px; color:%s">A lecturer the model never heard</p>'
 '<p style="font-size:76px; font-weight:600; color:%s">72.8 &#8594; 50.3</p>'
 '<p style="font-size:26px; color:%s">character error rate, per cent</p></div></div>'
 '<p style="font-size:30px; color:%s; line-height:1.45">Both are in the thesis and both are '
 'labelled. <b style="color:%s">The headline number has the test lecturers heard in training. '
 'The unseen-lecturer number is much worse.</b></p>'
 '%s</section>'
 % (LIGHT, eyebrow("Speech"), h2("What happens on an unheard lecturer"),
    LINE, MUTED, GREEN, MUTED, LINE, MUTED, ORANGE, MUTED, MUTED, INK,
    note("Do not dodge this. Each lecturer held out in turn, all six runs significant. "
         "If they ask whether you would still beat the baselines on an unseen lecturer: "
         "much less clearly, and say so."))
)

S["boardproblem"] = (
 '<section id="boardproblem" style="%s">'
 '%s%s'
 '<img src="%s" alt="One frame, lecturer occluding the board" '
 'style="width:1280px; height:530px; object-fit:contain; align-self:center">'
 '<p style="font-size:30px; color:%s; line-height:1.4">Her arm is across the truth table and '
 'the last two columns do not exist yet. <b style="color:%s">No single frame of this era '
 'shows the finished board.</b></p>'
 '%s</section>'
 % (LIGHT, eyebrow("Whiteboard"), h2("Why one frame is never enough"), IMG["frame"],
    MUTED, INK,
    note("This is a real frame at 12:40 of the digital logic lecture. The slide after it "
         "shows what the reconstruction recovers from the era as a whole."))
)

S["boardrecon"] = (
 '<section id="boardrecon" style="%s">'
 '%s%s'
 '<div style="display:flex; gap:28px">'
 '<div style="flex:1; display:flex; flex-direction:column; gap:12px">'
 '<img src="%s" alt="Rebuilt board" style="width:800px; height:420px; object-fit:contain; '
 'border:1px solid %s; border-radius:10px">'
 '<p style="font-size:26px; color:%s">Rebuilt: every pixel from a real frame, lecturer removed</p></div>'
 '<div style="flex:1; display:flex; flex-direction:column; gap:12px">'
 '<img src="%s" alt="Cleaned board" style="width:800px; height:420px; object-fit:contain; '
 'border:1px solid %s; border-radius:10px">'
 '<p style="font-size:26px; color:%s">Cleaned: background whitened for readability</p></div></div>'
 '<p style="font-size:29px; color:%s; line-height:1.4">Median <b style="color:%s">97.7 per '
 'cent</b> of tiles clear across 145 boards. <b style="color:%s">Nothing is generated.</b> '
 'We hand-checked 98 boards: 82 complete, 9 with writing genuinely lost.</p>'
 '%s</section>'
 % (LIGHT, eyebrow("Whiteboard"), h2("Rebuilt from the video, not generated"),
    IMG["raw"], LINE, MUTED, IMG["clean"], LINE, MUTED, MUTED, GREEN, INK,
    note("Tiled mosaic over erase-separated eras. Say the nine losses out loud. We ruled "
         "out generative inpainting because it would invent writing."))
)

S["prompt"] = (
 '<section id="prompt" data-transition="fade" style="%s">'
 '%s%s%s'
 '<p style="font-size:32px; color:#BFD8D5; line-height:1.45">Same model, same 35 boards, only '
 'the prompt changed: <b style="color:%s">31.2 to 88.8 per cent</b>. Same boards, only the '
 'model size changed: 83.7 to 89.0. <b style="color:%s">The prompt is worth 57.6 points and '
 'the model size 5.3, about eleven times less.</b></p>'
 '%s</section>'
 % (DARK, eyebrow("The main finding", "#7FCF9B"),
    h2("Prompt design beats model size", PAPER),
    '<img src="%s" alt="Board reading by prompt" style="width:1664px; height:440px; '
    'object-fit:contain">' % IMG["boardreading"],
    "#7FCF9B", PAPER,
    note("Slow down here. This is the finding that does not depend on our dataset and it is "
         "the supervisor's own area. Then the honesty line: the prompt was chosen on the "
         "boards it is reported on, so we split them by a rule fixed in advance and on the "
         "half we never touched it is 28.4 to 84.7, better on 17 of 18 boards."))
)

S["boxes"] = (
 '<section id="boxes" style="%s">'
 '%s%s'
 '<img src="%s" alt="Board with numbered boxes" style="width:1280px; height:470px; '
 'object-fit:contain; align-self:center">'
 '<p style="font-size:29px; color:%s; line-height:1.45"><b style="color:%s">Our code finds '
 'the blocks of writing and numbers them.</b> The model is then shown the board with the '
 'boxes already on it and asked to name and transcribe each number. That is Set-of-Mark '
 'prompting.</p>'
 '%s</section>'
 % (LIGHT, eyebrow("Whiteboard"), h2("The model names the boxes, it does not place them"),
    IMG["boxes"], MUTED, INK,
    note("If anyone looks closely: on this board the model swapped two names, calling the "
         "block diagram Gate symbol and the gate symbol Block diagram. It is in the thesis "
         "caption. Say it before they say it."))
)

S["notes"] = (
 '<section id="notes" style="%s">'
 '%s%s'
 '<div style="display:flex; gap:36px; align-items:center">'
 '<img src="%s" alt="Board content reaching the notes" style="width:900px; height:470px; '
 'object-fit:contain">'
 '<div style="flex:1; display:flex; flex-direction:column; gap:18px">'
 '<p style="font-size:27px; color:%s; font-weight:600">THREE CHECKS, ALL COUNTED IN EVERY FILE</p>'
 '<p style="font-size:28px; line-height:1.4">Quotations matched word for word against the '
 'transcript, deleted when they fail &#8212; 31 kept, 8 deleted</p>'
 '<p style="font-size:28px; line-height:1.4">Box references checked against boxes that '
 'exist &#8212; 1 survived</p>'
 '<p style="font-size:28px; line-height:1.4">Anything not from the lecture confined to a '
 'labelled box</p></div></div>'
 '%s</section>'
 % (LIGHT, eyebrow("Notes"), h2("Board content reaching the notes: 37.2 to 89.1 per cent"),
    IMG["notesrecall"], GREEN,
    note("Board-content recall scores only facts physically written on the board, which the "
         "language model cannot invent from prior knowledge. That is what makes it a "
         "grounding measure rather than a fluency one."))
)

S["reader"] = (
 '<section id="reader" style="%s">'
 '%s%s'
 '<table style="font-family:%s; font-size:31px; color:%s">'
 '<tr><th style="width:46%%; text-align:left">Twenty readers, one lecture, shown blind</th>'
 '<th style="width:14%%">Ours</th><th style="width:14%%">Original</th>'
 '<th style="width:12%%">Same</th><th style="width:14%%">p</th></tr>'
 '<tr><td>Prefer overall</td><td>15</td><td>4</td><td>1</td><td>0.019</td></tr>'
 '<tr><td>Better layout</td><td>18</td><td>2</td><td>0</td><td>0.0004</td></tr>'
 '<tr><td>Explains the concepts more clearly</td><td>10</td><td>2</td><td>8</td><td>0.039</td></tr>'
 '<tr><td>Easier to read and understand</td><td>10</td><td>4</td><td>6</td><td>0.18</td></tr></table>'
 '<p style="font-size:28px; color:%s; line-height:1.45"><b style="color:%s">This is a pilot '
 'and we call it one.</b> Twenty people, one lecture, no correction for multiple '
 'comparisons; under Bonferroni only the layout result survives. Ease of reading did not '
 'reach significance and we do not claim it.</p>'
 '%s</section>'
 % (LIGHT, eyebrow("Does it help a reader"), h2("Asking readers which note helps more"),
    SANS, INK, MUTED, INK,
    note("Two-sided exact binomial on those who expressed a preference. Ties excluded, which "
         "is the conservative convention. Order was not randomised and ours was always shown "
         "second, which works against the result."))
)

S["negatives"] = (
 '<section id="negatives" style="%s">'
 '%s%s'
 '<table style="font-family:%s; font-size:30px; color:%s">'
 '<tr><th style="width:38%%; text-align:left">What we tried</th>'
 '<th style="width:32%%; text-align:left">What we measured</th>'
 '<th style="width:30%%; text-align:left">Outcome</th></tr>'
 '<tr><td>Dual-ASR fusion</td><td>+0.7 points, p = 0.32</td><td>No effect</td></tr>'
 '<tr><td>Visual bias on the decoder</td><td>Any strength hurts recall</td><td>Abandoned</td></tr>'
 '<tr><td>Occlusion as a pointer</td><td>p = 0.054 and 0.159</td><td>Not supported</td></tr>'
 '<tr><td>Board clean-up, for the model</td><td>93.6 to 91.7</td><td>Made it worse</td></tr></table>'
 '<p style="font-size:29px; color:%s; line-height:1.45">The last one is the interesting one. '
 'We built the clean-up expecting it to help the model read, measured it, and it did not. '
 '<b style="color:%s">We kept it because it looks better to a person, and said so.</b></p>'
 '%s</section>'
 % (LIGHT, eyebrow("Honesty"), h2("Four things that did not work"), SANS, INK, MUTED, INK,
    note("Say this slide with a straight face. It is why the rest is believable. Four "
         "measured negatives, reported at the same level of detail as the positives."))
)

S["contrib"] = (
 '<section id="contrib" data-transition="fade" style="%s">'
 '%s%s'
 '<div style="display:flex; flex-direction:column; gap:20px">'
 '<p style="font-size:32px; line-height:1.45"><b style="color:#7FCF9B">1.</b> Prompt design '
 'matters about eleven times more than model size for reading a handwritten board. 57.6 '
 'points against 5.3, re-checked on a held-out half.</p>'
 '<p style="font-size:32px; line-height:1.45"><b style="color:#7FCF9B">2.</b> A note-quality '
 'measure a language model cannot satisfy from prior knowledge, because it scores only facts '
 'physically on the board.</p>'
 '<p style="font-size:32px; line-height:1.45"><b style="color:#7FCF9B">3.</b> English-word '
 'measures are invalid for code-mixed speech: they reward translating and punish '
 'transcribing.</p>'
 '<p style="font-size:32px; line-height:1.45"><b style="color:#7FCF9B">4.</b> The first '
 'measurement of what published Bengali models actually emit on spontaneous Banglish.</p></div>'
 '<p style="font-size:29px; color:#BFD8D5; line-height:1.4">The corpus is a contribution too. '
 'It is not the only one, and <b style="color:%s">none of these four depends on it.</b></p>'
 '%s</section>'
 % (DARK, eyebrow("Contributions", "#7FCF9B"),
    h2("What is new here, apart from the dataset", PAPER), PAPER,
    note("Have this ready and do not rush it. This is the question the supervisor has asked "
         "more than once. Lead with the prompt result, not the corpus."))
)

S["limits"] = (
 '<section id="limits" style="%s">'
 '%s%s'
 '<div style="display:flex; gap:26px">'
 '<div style="flex:1; display:flex; flex-direction:column; gap:16px">'
 '<p style="font-size:28px; line-height:1.4">Three lecturers, one university, one language pair.</p>'
 '<p style="font-size:28px; line-height:1.4">5.15 hours is small for speech recognition.</p>'
 '<p style="font-size:28px; line-height:1.4">Training was unstable at the chosen learning '
 'rate; one seed diverged.</p></div>'
 '<div style="flex:1; display:flex; flex-direction:column; gap:16px">'
 '<p style="font-size:28px; line-height:1.4">The board prompt was selected on the boards it '
 'is reported on; a held-out half supports it but does not undo that.</p>'
 '<p style="font-size:28px; line-height:1.4">The reader study is a pilot of twenty.</p>'
 '<p style="font-size:28px; line-height:1.4"><b style="color:#B4232C">Nothing here measures '
 'whether the generated prose is true.</b> One factual error was found by reading.</p></div></div>'
 '%s</section>'
 % (LIGHT, eyebrow("Limitations"), h2("What this work does not show"),
    note("Do not skip this slide for time. Stating limits before the panel finds them is "
         "the strongest position you can be in."))
)

S["future"] = (
 '<section id="future" style="%s">'
 '%s%s'
 '<div style="display:flex; gap:28px">%s%s%s</div>'
 '<p style="font-size:34px; color:%s; line-height:1.4">Thank you. We are happy to take '
 'questions.</p>'
 '%s</section>'
 % (LIGHT, eyebrow("Next"), h2("Where this goes from here"),
    card("A real reader study", "Randomised order, several lectures, and readers answering "
         "questions about the lecture after studying a note, which measures learning rather "
         "than preference."),
    card("Is the prose true?", "A reader who knows the subject going through the notes "
         "statement by statement against the recording."),
    card("More lecturers", "More institutions and subject areas, to show the result is not "
         "about these three voices."),
    INK,
    note("Close on the thank you and stay on this slide for questions. Backup slides follow "
         "if you need them."))
)

S["b_leak"] = (
 '<section id="b_leak" style="%s">'
 '%s%s'
 '<p style="font-size:31px; color:%s; line-height:1.45">An earlier split trained on a video '
 'that was also the test speaker. We found it with voice embeddings, corrected it, and '
 '<b style="color:%s">retired the old numbers</b>. Speaker similarity 0.99 against 0.77 '
 'confirmed the labels.</p>'
 '<p style="font-size:31px; color:%s; line-height:1.45">Every split since is by whole '
 'lecture, recorded in a file, and the voice of every recording was checked.</p>'
 '%s</section>'
 % (LIGHT, eyebrow("Backup", ORANGE), h2("The leak we found in our own work"), MUTED, INK,
    MUTED, note("If asked about leakage. Volunteering that you found and fixed your own "
                "leak is stronger than denying one."))
)

S["b_metric"] = (
 '<section id="b_metric" style="%s">'
 '%s%s'
 '<p style="font-size:31px; color:%s; line-height:1.45">The inherited measure counts English '
 'lexicon words. A better Banglish transcript emits <b style="color:%s">fewer</b> of them, so '
 'the measure moves <b style="color:%s">the wrong way</b> as transcription improves.</p>'
 '<p style="font-size:31px; color:%s; line-height:1.45">It also swings 8.1 points between two '
 'runs on identical data. We found this twice, independently, in one project. That is why '
 'note quality is scored on board content instead.</p>'
 '%s</section>'
 % (LIGHT, eyebrow("Backup", ORANGE), h2("Why we did not use the inherited metric"),
    MUTED, INK, INK, MUTED,
    note("If asked why not BLEU or ROUGE, or why not the term measure from the earlier phase."))
)

S["b_perlecture"] = (
 '<section id="b_perlecture" style="%s">'
 '%s%s%s'
 '<p style="font-size:29px; color:%s; line-height:1.4">Every one of the six test lectures '
 'improves. Lecturer B improves least, ending at 52 against 12 to 16, and contributed the '
 'least training speech at 0.7 hours. One lecture per lecturer, so this is an observation, '
 'not a controlled result.</p>'
 '%s</section>'
 % (LIGHT, eyebrow("Backup", ORANGE), h2("Per-lecture breakdown"),
    pic("perlecture", "Per-lecture error rates", 440), MUTED,
    note("If asked whether the average hides a failure, or why lecturer B is different."))
)

S["b_ethics"] = (
 '<section id="b_ethics" style="%s">'
 '%s%s'
 '<div style="display:flex; flex-direction:column; gap:18px">'
 '<p style="font-size:30px; line-height:1.45">The three people recorded are the three of us. '
 'No third-party participant, and no external consent to obtain.</p>'
 '<p style="font-size:30px; line-height:1.45">No student was a subject of any recording. The '
 'camera faces the whiteboard and the person writing on it.</p>'
 '<p style="font-size:30px; line-height:1.45">Nothing is published. No lecture content leaves '
 'our machines, because every model runs locally.</p>'
 '<p style="font-size:30px; line-height:1.45">Recordings were made in Brac University '
 'classrooms and other classrooms available to us.</p></div>'
 '%s</section>'
 % (LIGHT, eyebrow("Backup", ORANGE), h2("Who was recorded, and consent"),
    note("If asked about ethics or data protection. This is also why the ethics review was "
         "straightforward: we are our own subjects."))
)

ORDER = ["cover", "problem", "overview", "baselines", "corpus", "pipeline", "archwhisper",
         "prereg", "asrresult", "unseen", "boardproblem", "boardrecon", "prompt", "boxes",
         "notes", "reader", "negatives", "contrib", "limits", "future",
         "b_leak", "b_metric", "b_perlecture", "b_ethics"]

for sid in ORDER:
    io.open(SL / (sid + ".html"), "w", encoding="utf-8").write(S[sid])

index = {
    "v": 4,
    "createdOnFiles": {"v": 1, "at": "2026-09-26T00:00:00Z"},
    "title": "InsightLens Thesis Defense",
    "order": ORDER,
    "sections": {
        "s1": {"description": "The problem and why existing tools do not solve it",
               "start": "cover"},
        "s2": {"description": "Adapting the speech model and what it achieved",
               "start": "archwhisper"},
        "s3": {"description": "Rebuilding the whiteboard and reading it with a vision model",
               "start": "boardproblem"},
        "s4": {"description": "The notes, the reader study and what did not work",
               "start": "notes"},
        "s5": {"description": "Backup slides held for questions", "start": "b_leak"},
    },
    "faces": {
        "eb-garamond": {"family": "EB Garamond",
                        "href": "https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;600&display=swap"},
        "ibm-plex-sans": {"family": "IBM Plex Sans",
                          "href": "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600&display=swap"},
    },
    "designSystems": [],
}
io.open(ROOT / "project" / "deck.json", "w", encoding="utf-8").write(
    json.dumps(index, indent=1))
print("wrote %d slides + index" % len(ORDER))
