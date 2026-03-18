# File: src/question_detector.py

import re

class QuestionDetector:
    def __init__(self):
        self.question_words = {
            'bengali': [
                'কিভাবে', 'কীভাবে', 'কোথায়', 'কখন',
                'কতটুকু', 'কতদিন', 'কত টাকা', 'কত দিন',
                'কার কাছে', 'কোন নম্বর', 'কোন নাম্বার'
            ],
            'bengali_roman': [
                'kivabe', 'kivabe', 'kothai', 'kokhon',
                'koto din', 'koto taka', 'koto charge'
            ],
            'english': [
                'how much', 'how many', 'how do', 'how can',
                'how long', 'when will', 'where can', 'where do',
                'what is', 'what are', 'what time',
                'do you deliver', 'is it available',
                'can i', 'can you', 'will you'
            ]
        }

    def detect(self, comment):
        comment_lower = comment.lower().strip()

        # Only use ? mark if combined with short comment
        # (avoids catching sarcastic long comments with ?)
        if '?' in comment and len(comment.split()) <= 12:
            return {
                'is_question': True,
                'reason': 'question mark in short comment'
            }

        # Check Bengali specific question phrases (not single words like কি)
        for phrase in self.question_words['bengali']:
            if phrase in comment_lower:
                return {
                    'is_question': True,
                    'reason': f"Bengali question phrase: '{phrase}'"
                }

        # Check Romanized Bengali
        for phrase in self.question_words['bengali_roman']:
            if phrase in comment_lower:
                return {
                    'is_question': True,
                    'reason': f"Romanized question phrase: '{phrase}'"
                }

        # Check English question phrases (not single words)
        for phrase in self.question_words['english']:
            if phrase in comment_lower:
                return {
                    'is_question': True,
                    'reason': f"English question phrase: '{phrase}'"
                }

        return {'is_question': False}


# ── TEST ──────────────────────────────────────────────────────
if __name__ == "__main__":
    detector = QuestionDetector()

    test_cases = [
        ("ডেলিভারি চার্জ কত?", True),
        ("delivery koto din lagbe?", True),
        ("When will it be available?", True),
        ("how much does it cost?", True),
        ("কিভাবে অর্ডার করবো?", True),
        ("can you deliver to Khulna?", True),
        ("দারুণ product! আবার কিনবো ❤️", False),
        ("বাহ কি সুন্দর 🙄", False),          # has কি but not a question
        ("This is darun না", False),
        ("আপনি ভালো আছেন তো?", False),        # PA phrase, short but cultural
        ("গাজাখোর তুমি", False),
    ]

    print("Question Detection Test:")
    correct = 0
    for comment, expected in test_cases:
        result = detector.detect(comment)
        status = "✅" if result['is_question'] == expected else "❌"
        if result['is_question'] == expected:
            correct += 1
        print(f"\n{status} '{comment}'")
        if result['is_question']:
            print(f"   Reason: {result['reason']}")
        else:
            print(f"   Not a question")

    print(f"\nAccuracy: {correct}/{len(test_cases)}")