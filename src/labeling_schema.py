# File: src/labeling_schema.py

EMOTION_LABELS = {
    'genuine_positive': 'GP',      # দারুণ! ❤️
    'genuine_negative': 'GN',      # খারাপ লাগলো 😞
    'sarcastic': 'SAR',            # বাহ কি সুন্দর 🙄
    'passive_aggressive': 'PA',    # আপনি ভালো আছেন তো?
    'angry': 'ANG',                # চোর! ফেরত দাও!
    'concerned': 'CON',            # সাবধান থাকবেন
    'neutral': 'NEU'               # ধন্যবাদ
}

INTENT_LABELS = {
    'support': 'SUP',              # ভালো হয়েছে
    'criticism': 'CRI',            # উন্নতি করুন
    'question': 'QUE',             # কবে পাওয়া যাবে?
    'trolling': 'TRO',             # হাহাহা fail
    'spam': 'SPM',                 # Visit my page!!!
    'complaint': 'COM'             # 3 days no delivery
}

RESPONSE_TONE = {
    'friendly': 'FRI',             # ধন্যবাদ ভাই!
    'apologetic': 'APO',           # দুঃখিত
    'professional': 'PRO',         # আমরা দেখছি
    'ignore': 'IGN'                # Don't reply
}

# Language tags used in dataset
LANGUAGE_TAGS = {
    'bengali':    'Unicode Bengali script — বাংলা',
    'english':    'Pure English',
    'mixed':      'Both Bengali and English in same comment',
    'romanized':  'Bengali meaning written in Latin script — ami tomake valobasi'
}