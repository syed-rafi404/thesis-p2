"""
Bengali to Romanized (Latin) Transliteration

Custom implementation for Banglish lecture content.
Maps Bengali Unicode characters to their romanized equivalents.

This enables comparison between:
- Whisper output: "ami class ta likhbo" (romanized)
- BanglaASR output: "আমি ক্লাস টা লিখবো" → transliterated → "ami class ta likhbo"
"""

import re
from typing import Dict, List, Tuple


# ============================================================================
# BENGALI TO ROMANIZED MAPPING
# ============================================================================

# Bengali vowels (স্বরবর্ণ)
VOWELS = {
    'অ': 'o', 'আ': 'a', 'ই': 'i', 'ঈ': 'i',
    'উ': 'u', 'ঊ': 'u', 'ঋ': 'ri',
    'এ': 'e', 'ঐ': 'oi', 'ও': 'o', 'ঔ': 'ou',
}

# Bengali vowel marks (কার)
VOWEL_MARKS = {
    'া': 'a', 'ি': 'i', 'ী': 'i',
    'ু': 'u', 'ূ': 'u', 'ৃ': 'ri',
    'ে': 'e', 'ৈ': 'oi', 'ো': 'o', 'ৌ': 'ou',
    'ং': 'ng', 'ঃ': 'h', 'ঁ': 'n',
}

# Bengali consonants (ব্যঞ্জনবর্ণ)
CONSONANTS = {
    'ক': 'k', 'খ': 'kh', 'গ': 'g', 'ঘ': 'gh', 'ঙ': 'ng',
    'চ': 'ch', 'ছ': 'chh', 'জ': 'j', 'ঝ': 'jh', 'ঞ': 'n',
    'ট': 't', 'ঠ': 'th', 'ড': 'd', 'ঢ': 'dh', 'ণ': 'n',
    'ত': 't', 'থ': 'th', 'দ': 'd', 'ধ': 'dh', 'ন': 'n',
    'প': 'p', 'ফ': 'ph', 'ব': 'b', 'ভ': 'bh', 'ম': 'm',
    'য': 'j', 'র': 'r', 'ল': 'l',
    'শ': 'sh', 'ষ': 'sh', 'স': 's', 'হ': 'h',
    'ড়': 'r', 'ঢ়': 'rh', 'য়': 'y', 'ৎ': 't',
}

# Special characters
SPECIAL = {
    '্': '',   # Hasanta (virama) - removes inherent vowel
    '়': '',   # Nukta
    '।': '.',  # Danda (full stop)
    '॥': '.',  # Double danda
}

# Bengali numerals
NUMERALS = {
    '০': '0', '১': '1', '২': '2', '৩': '3', '৪': '4',
    '৫': '5', '৬': '6', '৭': '7', '৮': '8', '৯': '9',
}

# Common conjuncts (যুক্তাক্ষর) - frequently used combinations
CONJUNCTS = {
    'ক্ষ': 'kkh', 'জ্ঞ': 'gya', 'ঞ্চ': 'nch', 'ঞ্জ': 'nj',
    'ক্ক': 'kk', 'ক্ত': 'kt', 'ক্র': 'kr', 'ক্ল': 'kl',
    'গ্র': 'gr', 'ঘ্র': 'ghr',
    'চ্ছ': 'chchh', 'জ্জ': 'jj',
    'ট্ট': 'tt', 'ড্ড': 'dd',
    'ত্ত': 'tt', 'ত্র': 'tr', 'ত্ন': 'tn',
    'দ্দ': 'dd', 'দ্ধ': 'ddh', 'দ্ব': 'dw', 'দ্ম': 'dm', 'দ্র': 'dr',
    'ধ্র': 'dhr',
    'ন্ত': 'nt', 'ন্দ': 'nd', 'ন্ধ': 'ndh', 'ন্ন': 'nn', 'ন্ম': 'nm',
    'প্প': 'pp', 'প্র': 'pr', 'প্ল': 'pl',
    'ব্দ': 'bd', 'ব্ধ': 'bdh', 'ব্ব': 'bb', 'ব্র': 'br', 'ব্ল': 'bl',
    'ভ্র': 'bhr',
    'ম্ম': 'mm', 'ম্প': 'mp', 'ম্ব': 'mb', 'ম্ভ': 'mbh',
    'ল্ল': 'll', 'ল্প': 'lp',
    'শ্চ': 'shch', 'শ্ন': 'shn', 'শ্ব': 'shw', 'শ্র': 'shr',
    'ষ্ট': 'sht', 'ষ্ঠ': 'shth', 'ষ্ণ': 'shn',
    'স্ক': 'sk', 'স্ট': 'st', 'স্ত': 'st', 'স্থ': 'sth', 'স্ন': 'sn',
    'স্প': 'sp', 'স্ব': 'sw', 'স্ম': 'sm', 'স্র': 'sr',
    'হ্ন': 'hn', 'হ্ম': 'hm', 'হ্র': 'hr', 'হ্ল': 'hl',
    # Common programming/lecture terms in Bengali
    'ক্লা': 'cla', 'ক্লাস': 'class',
    'অব': 'ob', 'অবজে': 'obje',
    'প্রো': 'pro', 'প্রোগ্রা': 'progra',
    'মে': 'me', 'মেথ': 'meth',
    'ভ্যা': 'va', 'ভ্যারি': 'vari',
}


class BengaliTransliterator:
    """
    Transliterates Bengali Unicode text to Romanized (Latin) script.
    
    Designed for Banglish lecture content where technical terms
    are mixed with Bengali explanations.
    """
    
    def __init__(self):
        # Build combined mapping
        self.char_map = {}
        self.char_map.update(VOWELS)
        self.char_map.update(VOWEL_MARKS)
        self.char_map.update(CONSONANTS)
        self.char_map.update(SPECIAL)
        self.char_map.update(NUMERALS)
        
        # Sort conjuncts by length (longest first) for proper matching
        self.conjuncts = sorted(CONJUNCTS.items(), key=lambda x: -len(x[0]))
        
        # Bengali Unicode range pattern
        self.bengali_pattern = re.compile(r'[\u0980-\u09FF]+')
        
        # Technical terms that should stay in English
        self.technical_terms = {
            'class', 'object', 'method', 'function', 'variable',
            'java', 'python', 'programming', 'code', 'string',
            'int', 'boolean', 'public', 'private', 'static', 'void',
        }
    
    def transliterate_word(self, word: str) -> str:
        """
        Transliterate a single Bengali word to romanized form.
        
        Args:
            word: Bengali word in Unicode
            
        Returns:
            Romanized (Latin) equivalent
        """
        if not word:
            return ""
        
        result = []
        i = 0
        
        while i < len(word):
            # First, check for conjuncts (multi-character combinations)
            matched = False
            for conjunct, roman in self.conjuncts:
                if word[i:].startswith(conjunct):
                    result.append(roman)
                    i += len(conjunct)
                    matched = True
                    break
            
            if matched:
                continue
            
            char = word[i]
            
            # Check if it's a mapped character
            if char in self.char_map:
                roman = self.char_map[char]
                
                # Handle inherent 'o' vowel for consonants
                if char in CONSONANTS:
                    # Check if followed by vowel mark or hasanta
                    if i + 1 < len(word):
                        next_char = word[i + 1]
                        if next_char in VOWEL_MARKS:
                            # Vowel mark will handle the vowel
                            result.append(roman)
                        elif next_char == '্':
                            # Hasanta - no inherent vowel
                            result.append(roman)
                        else:
                            # Add inherent 'o' vowel
                            result.append(roman + 'o')
                    else:
                        # End of word - add inherent 'o'
                        result.append(roman + 'o')
                else:
                    result.append(roman)
            else:
                # Keep unknown characters as-is
                result.append(char)
            
            i += 1
        
        return ''.join(result)
    
    def transliterate(self, text: str) -> str:
        """
        Transliterate Bengali text to romanized form.
        
        Preserves non-Bengali text (English, numbers, punctuation).
        
        Args:
            text: Mixed Bengali/English text
            
        Returns:
            Fully romanized text
        """
        if not text:
            return ""
        
        result = []
        last_end = 0
        
        # Find all Bengali segments
        for match in self.bengali_pattern.finditer(text):
            # Add non-Bengali text before this match
            if match.start() > last_end:
                result.append(text[last_end:match.start()])
            
            # Transliterate Bengali segment
            bengali_text = match.group()
            romanized = self.transliterate_word(bengali_text)
            result.append(romanized)
            
            last_end = match.end()
        
        # Add remaining non-Bengali text
        if last_end < len(text):
            result.append(text[last_end:])
        
        return ''.join(result)
    
    def transliterate_sentences(self, text: str) -> List[Tuple[str, str]]:
        """
        Transliterate text and return sentence pairs.
        
        Returns:
            List of (original, transliterated) tuples
        """
        # Split into sentences
        sentences = re.split(r'[।.!?]', text)
        
        pairs = []
        for sent in sentences:
            sent = sent.strip()
            if sent:
                transliterated = self.transliterate(sent)
                pairs.append((sent, transliterated))
        
        return pairs


# ============================================================================
# QUICK TEST
# ============================================================================

if __name__ == "__main__":
    transliterator = BengaliTransliterator()
    
    # Test cases
    test_cases = [
        "আমি তওহিদ",
        "ক্লাস এবং অবজেক্ট",
        "প্রোগ্রামিং শিখি",
        "হ্যালো ওয়ার্ল্ড",
        "জাভা অবজেক্ট ওরিয়েন্টেড প্রোগ্রামিং",
        "এই ডিজাইনকে ক্লাস বলে",
        "ব্লুপ্রিন্ট টেমপ্লেট ডিজাইন",
    ]
    
    print("=" * 60)
    print("BENGALI → ROMANIZED TRANSLITERATION TEST")
    print("=" * 60)
    
    for bengali in test_cases:
        romanized = transliterator.transliterate(bengali)
        print(f"\n{bengali}")
        print(f"→ {romanized}")
