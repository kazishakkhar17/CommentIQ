# File: src/spam_detector.py

import re

class SpamDetector:
    def __init__(self):
        self.spam_patterns = {
            'fake_links': [
                r'http[s]?://',
                r'www\.',
                r'bit\.ly', r'tinyurl',
                r't\.me/',
            ],
            'self_promotion': [
                'visit my page', 'visit my profile',
                'follow me', 'follow for follow',
                'check my page', 'check my profile',
                'আমার পেজ', 'আমার প্রোফাইল',
                'like my page', 'share my page',
                'আমাকে follow', 'f4f', 'l4l',
            ],
            'fake_offers': [
                'free iphone', 'free gift', 'win now',
                'click here to win', 'congratulations you won',
                'earn money', 'make money fast',
                'ফ্রি পাচ্ছেন', 'জিতে নিন',
            ]
        }

    def detect(self, comment):
        comment_lower = comment.lower()

        for pattern in self.spam_patterns['fake_links']:
            if re.search(pattern, comment_lower):
                return {
                    'is_spam': True,
                    'spam_type': 'fake_link',
                    'reason': f"URL/link detected"
                }

        for phrase in self.spam_patterns['self_promotion']:
            if phrase.lower() in comment_lower:
                return {
                    'is_spam': True,
                    'spam_type': 'self_promotion',
                    'reason': f"Self-promotion phrase: '{phrase}'"
                }

        for phrase in self.spam_patterns['fake_offers']:
            if phrase.lower() in comment_lower:
                return {
                    'is_spam': True,
                    'spam_type': 'fake_offer',
                    'reason': f"Fake offer phrase: '{phrase}'"
                }

        return {'is_spam': False}


# ── TEST ──────────────────────────────────────────────────────
if __name__ == "__main__":
    detector = SpamDetector()

    test_cases = [
        "দারুণ product! আবার কিনবো ❤️",
        "Visit my page for free gifts!!!",
        "Check this out: https://bit.ly/abc123",
        "আমার পেজ like করুন please",
        "Congratulations you won a free iPhone",
        "ডেলিভারি কত দিনে আসবে?",
    ]

    print("Spam Detection Test:")
    for comment in test_cases:
        result = detector.detect(comment)
        if result['is_spam']:
            print(f"\n🚫 SPAM: '{comment[:50]}'")
            print(f"   Type: {result['spam_type']}")
            print(f"   Reason: {result['reason']}")
        else:
            print(f"\n✅ CLEAN: '{comment[:50]}'")