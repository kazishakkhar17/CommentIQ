# File: src/negation_detector.py

import re

class NegationDetector:
    def __init__(self):
        self.negation_words = {
            # Bengali Unicode
            'bengali': ['না', 'নেই', 'নয়', 'নাই', 'কখনো না', 'না না'],
            # Romanized Bengali
            'bengali_roman': ['na', 'nai', 'nah', 'nei', 'noy', 'na re', 'naa'],
            # English
            'english': ['not', 'no', 'never', 'neither', 'nor', "n't", 'nothing']
        }

    def detect(self, comment):
        """Check if comment contains negation"""
        comment_lower = comment.lower()

        # Check Bengali Unicode
        for neg in self.negation_words['bengali']:
            if neg in comment_lower:
                return {
                    'has_negation': True,
                    'negation_word': neg,
                    'language': 'bengali'
                }

        # Check Romanized Bengali
        # Word boundary check to avoid matching 'na' inside 'name'
        for neg in self.negation_words['bengali_roman']:
            pattern = r'\b' + re.escape(neg) + r'\b'
            if re.search(pattern, comment_lower):
                return {
                    'has_negation': True,
                    'negation_word': neg,
                    'language': 'bengali_roman'
                }

        # Check English
        for neg in self.negation_words['english']:
            if neg in comment_lower:
                return {
                    'has_negation': True,
                    'negation_word': neg,
                    'language': 'english'
                }

        return {'has_negation': False}

    def flip_sentiment(self, emotion):
        """Flip positive/negative if negation detected"""
        flip_map = {
            'GP': 'GN',   # Genuine Positive → Negative
            'GN': 'GP',   # Genuine Negative → Positive
            # SAR, PA, ANG, CON, NEU not flipped — more complex
        }
        return flip_map.get(emotion, emotion)


# ── TEST ──────────────────────────────────────────────────────
if __name__ == "__main__":
    detector = NegationDetector()

    test_cases = [
        # (comment, original_emotion, expected_after_flip)
        ("দারুণ না", "GP", "GN"),              # Bengali negation
        ("darun na", "GP", "GN"),               # Romanized negation
        ("eta valo nai bhai", "GP", "GN"),      # Romanized negation
        ("This is NOT good", "GP", "GN"),       # English negation
        ("ভালো না", "GP", "GN"),               # Bengali negation
        ("never satisfied", "GP", "GN"),        # English negation
        ("দারুণ product!", "GP", "GP"),         # No negation — stays
        ("valo laglo", "GP", "GP"),             # No negation — stays
        ("সার্ভিস ভালো না", "GP", "GN"),       # Bengali negation
        ("not bad at all", "GN", "GP"),         # Double negative
    ]

    print("Negation Detection Test:\n")
    correct = 0
    for comment, original, expected in test_cases:
        result = detector.detect(comment)
        if result['has_negation']:
            final = detector.flip_sentiment(original)
            match = "✅" if final == expected else "❌"
            if final == expected:
                correct += 1
            print(f"{match} '{comment}'")
            print(f"   Negation: '{result['negation_word']}' ({result['language']})")
            print(f"   {original} → {final} (expected: {expected})")
        else:
            match = "✅" if original == expected else "❌"
            if original == expected:
                correct += 1
            print(f"{match} '{comment}' → No negation, stays: {original}")
        print()

    print(f"Accuracy: {correct}/{len(test_cases)} ({correct/len(test_cases)*100:.0f}%)")