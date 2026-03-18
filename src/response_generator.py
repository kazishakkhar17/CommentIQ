import random

# File: src/response_generator.py

class ResponseGenerator:
    def __init__(self):
        self.templates = {
            # ---------------------------------------------------
            # Genuine Positive
            # ---------------------------------------------------
            'GP': {
                'bengali': [
                    "ধন্যবাদ আপনার সুন্দর মন্তব্যের জন্য! ❤️",
                    "আপনার reaction আমাদের অনুপ্রেরণা! 🙏",
                    "খুশি হলাম জেনে যে আপনার ভালো লেগেছে! 😊",
                    "আপনার support দেখে আনন্দিত হলাম! 😄"
                ],
                'english': [
                    "Thank you for your kind comment! ❤️",
                    "We're thrilled you enjoyed it! 😊",
                    "Your support means a lot to us! 🙏",
                    "Glad you liked it! 😄"
                ],
                'tone': 'friendly'
            },

            # ---------------------------------------------------
            # Genuine Negative
            # ---------------------------------------------------
            'GN': {
                'bengali': [
                    "দুঃখিত আপনার এই অভিজ্ঞতার জন্য। আমরা উন্নতির চেষ্টা করছি। 😔",
                    "আপনার feedback আমাদের কাছে গুরুত্বপূর্ণ। আমরা বিষয়টি দেখছি। 🛠️",
                    "আপনার concern আমরা লক্ষ্য করেছি এবং কাজ করছি। 🙏"
                ],
                'english': [
                    "Sorry for your negative experience. We're working to improve. 😔",
                    "Thank you for your feedback. We'll look into it. 🛠️",
                    "We've noted your concern and are addressing it. 🙏"
                ],
                'tone': 'apologetic'
            },

            # ---------------------------------------------------
            # Sarcastic
            # ---------------------------------------------------
            'SAR': {
                'bengali': [
                    "আপনার মন্তব্যটি বুঝতে পেরেছি। 😊 সত্যিকারের কোনো feedback থাকলে জানাবেন।",
                    "আচ্ছা, বুঝলাম! 😅 তবে কোনো genuine মতামত থাকলে শেয়ার করুন।",
                    "আপনার কথাটা মাথায় রাখলাম। 😎 কিছু জানাতে চাইলে বলুন।"
                ],
                'english': [
                    "Understood your comment! 😊 If you have genuine feedback, feel free to share.",
                    "Got it! 😅 But if you have real thoughts, we'd love to hear them.",
                    "Noted! 😎 If there's something specific you'd like to share, let us know."
                ],
                'tone': 'light_professional'
            },

            # ---------------------------------------------------
            # Passive-Aggressive
            # ---------------------------------------------------
            'PA': {
                'bengali': [
                    "আপনার concern বুঝতে পারছি। আমরা বিষয়টি দেখছি। 🤔",
                    "ধন্যবাদ জানানোর জন্য। আমরা এটি ঠিক করার চেষ্টা করছি। 🙏",
                    "আপনার মন্তব্যটি লক্ষ্য করেছি। প্রয়োজনীয় পদক্ষেপ নেওয়া হচ্ছে। 👌"
                ],
                'english': [
                    "We understand your concern and are looking into it. 🤔",
                    "Thanks for letting us know. We're working on it. 🙏",
                    "We've noted your comment and are taking the necessary steps. 👌"
                ],
                'tone': 'professional'
            },

            # ---------------------------------------------------
            # Angry
            # ---------------------------------------------------
            'ANG': {
                'bengali': [
                    "আমরা দুঃখিত এবং আপনার ক্ষোভ বুঝতে পারছি। 😔 আমাদের team দ্রুত বিষয়টি সমাধান করবে।",
                    "এই অভিজ্ঞতার জন্য আন্তরিক দুঃখিত। আমরা এখনই সমাধানে কাজ করছি। 🔧",
                    "আপনার frustration বুঝতে পারছি। আমরা দ্রুত action নিচ্ছি। 💪"
                ],
                'english': [
                    "We're truly sorry and understand your frustration. 😔 Our team will resolve this quickly.",
                    "Sincerely sorry for this experience. We're working on a resolution right away. 🔧",
                    "We hear you and are taking prompt action. 💪"
                ],
                'tone': 'apologetic_urgent'
            },

            # ---------------------------------------------------
            # Concerned
            # ---------------------------------------------------
            'CON': {
                'bengali': [
                    "ধন্যবাদ আপনার concern এর জন্য। আমরা সাবধান আছি। 👀",
                    "আপনার পরামর্শের জন্য কৃতজ্ঞ। আমরা খেয়াল রাখছি। 🙏",
                    "আপনার মতামত আমাদের সাহায্য করছে। ধন্যবাদ। ✅"
                ],
                'english': [
                    "Thank you for your concern. We're being careful. 👀",
                    "Grateful for your advice. We're keeping an eye on it. 🙏",
                    "Your input helps us. Thank you. ✅"
                ],
                'tone': 'grateful_professional'
            },

            # ---------------------------------------------------
            # Neutral
            # ---------------------------------------------------
            'NEU': {
                'bengali': [
                    "ধন্যবাদ আপনার মন্তব্যের জন্য। 🙂",
                    "জানানোর জন্য ধন্যবাদ। 🙏",
                    "আপনার মন্তব্য আমাদের কাছে পৌঁছেছে। ✅"
                ],
                'english': [
                    "Thank you for your comment. 🙂",
                    "Thanks for letting us know. 🙏",
                    "Your comment has been noted. ✅"
                ],
                'tone': 'neutral_polite'
            },

            # ---------------------------------------------------
            # Question / Inquiry
            # ---------------------------------------------------
            'QUESTION': {
                'bengali': [
                    "আপনার প্রশ্নের জন্য ধন্যবাদ। 🙂 বিস্তারিত জানতে আমাদের inbox এ message করুন।",
                    "ধন্যবাদ জানানোর জন্য। আমাদের page দেখুন অথবা আমাদের সাথে যোগাযোগ করুন। 📩",
                    "আপনার inquiry পেয়েছি। আমরা শীঘ্রই জানাবো। ✅"
                ],
                'english': [
                    "Thank you for your question. 🙂 Please message us for more details.",
                    "Thanks for reaching out. Please check our page or get in touch with us. 📩",
                    "We've received your inquiry and will get back to you soon. ✅"
                ],
                'tone': 'helpful_informative'
            },

            # ---------------------------------------------------
            # Spam — no reply
            # ---------------------------------------------------
            'SPAM': {
                'bengali': [],
                'english': [],
                'tone': 'no_reply'
            }
        }

    def generate(self, emotion, language='bengali'):
        # Spam gets no reply
        if emotion == 'SPAM':
            return {
                'response_text': None,
                'tone': 'no_reply',
                'emotion_responded_to': 'SPAM'
            }

        if emotion not in self.templates:
            emotion = 'NEU'

        # ← FIXED: random.choice instead of [0]
        response = random.choice(self.templates[emotion][language])
        return {
            'response_text': response,
            'tone': self.templates[emotion]['tone'],
            'emotion_responded_to': emotion
        }


# ── TEST ──────────────────────────────────────────────────────
if __name__ == "__main__":
    generator = ResponseGenerator()

    test_cases = [
        ('GP',   'bengali'),
        ('GN',   'bengali'),
        ('SAR',  'bengali'),
        ('PA',   'bengali'),
        ('ANG',  'bengali'),
        ('CON',  'english'),
        ('NEU',  'english'),
        ('SPAM', 'bengali'),
    ]

    print("Response Generator Test:")
    for emotion, lang in test_cases:
        result = generator.generate(emotion, lang)
        print(f"\n{emotion} ({lang}):")
        print(f"  Response: {result['response_text']}")
        print(f"  Tone: {result['tone']}")