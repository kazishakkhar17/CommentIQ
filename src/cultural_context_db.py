# File: src/cultural_context_db.py
#
# Built from deep analysis of 838 labeled Bengali Facebook comments
# Phrases verified against actual emotion labels in dataset
# Cross-emotion confusion analysis used to set confidence boosts

# ── FINDINGS FROM DATA ANALYSIS ──────────────────────────────
#
# গাজা/নেশা words: GN(47%), ANG(27%), SAR(20%), CON(7%)
#   → Dominant: GN — accusation/gossip tone
#   → গাজাখোর (with -খোর suffix): 100% ANG — direct insult
#   → নেশাখোর: 80% GN, 20% SAR
#
# পিনিকে: GN(50%), SAR(25%), ANG(25%)
#   → Mockery context → SAR, accusation → GN/ANG
#
# দালাল: ANG(40%), SAR(20%), GN(20%), PA(20%)
#   → With anger words → ANG; standalone → SAR
#
# বাটপার: GN(60%), ANG(40%) — fraud/scammer context
#
# তুলসী পাতা: 100% SAR — rhetorical question "are you so pure?"
#
# চমৎকার, আগুন: 100% GP — reliable positive markers
#
# ছোটলোক: 100% ANG — strong insult
#
# মনে হয়/দেখলেই/বুঝা যায়: GN/SAR/ANG — accusation pattern
#   when combined with drug words → stronger negative signal
#
# PA markers: এক সময় পছন্দ করতাম, আমরা জানি, সঠিক পথে ছিলেন কিন্তু,
#             বললেন না, মানতেই হবে, কপি হয়েছে
# ─────────────────────────────────────────────────────────────

CULTURAL_PHRASES = {

    # ══════════════════════════════════════════════════════════
    # SARCASTIC PHRASES (SAR)
    # ══════════════════════════════════════════════════════════

    # "Are you so pure?" — rhetorical, 100% SAR in data
    "ধোয়া তুলসী পাতা": {
        "surface_meaning": "Washed holy basil leaf (pure/clean)",
        "hidden_meaning": "Are you really so innocent? (sarcastic)",
        "emotion_override": "SAR",
        "confidence_boost": 0.3
    },
    "ধোঁয়া তুলসীপাতা": {
        "surface_meaning": "Washed holy basil leaf",
        "hidden_meaning": "Acting innocent (sarcastic)",
        "emotion_override": "SAR",
        "confidence_boost": 0.3
    },
    "তুলশী পাতা": {
        "surface_meaning": "Holy basil leaf",
        "hidden_meaning": "Acting innocent/pure (sarcastic)",
        "emotion_override": "SAR",
        "confidence_boost": 0.25
    },
    # Romanized variants
    "dhoa tulsi pata": {
        "surface_meaning": "Washed holy basil leaf",
        "hidden_meaning": "Are you really so innocent?",
        "emotion_override": "SAR",
        "confidence_boost": 0.3
    },
    "tulsi pata": {
        "surface_meaning": "Holy basil leaf",
        "hidden_meaning": "Acting innocent (sarcastic)",
        "emotion_override": "SAR",
        "confidence_boost": 0.25
    },

    # "Drama within drama" — sarcastic commentary
    "নাটকের ভিতর নাটক": {
        "surface_meaning": "Drama within drama",
        "hidden_meaning": "Everything is fake/staged",
        "emotion_override": "SAR",
        "confidence_boost": 0.25
    },

    # "Hmm, very good" — sarcastic tone
    "হুম খুব ভালো লাগে": {
        "surface_meaning": "Hmm, feels very good",
        "hidden_meaning": "I don't actually enjoy this at all",
        "emotion_override": "SAR",
        "confidence_boost": 0.25
    },

    # Remittance warrior — used sarcastically
    "রেমিট্যান্স যোদ্ধা": {
        "surface_meaning": "Remittance warrior",
        "hidden_meaning": "Sarcastic label for people doing questionable things",
        "emotion_override": "SAR",
        "confidence_boost": 0.2
    },

    # "Fed honey" — bribed/manipulated
    "মধু খাওয়াইছো": {
        "surface_meaning": "Fed honey",
        "hidden_meaning": "You bribed/manipulated them",
        "emotion_override": "SAR",
        "confidence_boost": 0.2
    },

    # "Brilliant" — used sarcastically (especially with cricket context)
    "ব্রিলিয়ান্ট রান আউট": {
        "surface_meaning": "Brilliant run out",
        "hidden_meaning": "Sarcastic praise for unsportsmanlike behavior",
        "emotion_override": "SAR",
        "confidence_boost": 0.2
    },

    # "Promotion ninja technique" — sarcastic about paid promotion
    "ninja technic": {
        "surface_meaning": "Ninja technique",
        "hidden_meaning": "Sarcastically calling out hidden promotion/advertising",
        "emotion_override": "SAR",
        "confidence_boost": 0.2
    },

    # Bah darun — classic Bangladeshi sarcasm
    "বাহ দারুণ তো": {
        "surface_meaning": "Wow, great!",
        "hidden_meaning": "This is terrible/disappointing",
        "emotion_override": "SAR",
        "confidence_boost": 0.25
    },
    "bah darun to": {
        "surface_meaning": "Wow, great!",
        "hidden_meaning": "This is terrible/disappointing",
        "emotion_override": "SAR",
        "confidence_boost": 0.25
    },
    "bah darun": {
        "surface_meaning": "Wow great",
        "hidden_meaning": "Sarcastic praise",
        "emotion_override": "SAR",
        "confidence_boost": 0.2
    },

    # ══════════════════════════════════════════════════════════
    # PASSIVE AGGRESSIVE PHRASES (PA)
    # ══════════════════════════════════════════════════════════

    # "I used to like you once" — classic PA backhanded comment
    "এক সময় পছন্দ করতাম": {
        "surface_meaning": "I used to like you",
        "hidden_meaning": "I no longer respect you (disappointed)",
        "emotion_override": "PA",
        "confidence_boost": 0.3
    },
    "একসময় পছন্দ করতাম": {
        "surface_meaning": "I used to like you",
        "hidden_meaning": "Passive aggressive disappointment",
        "emotion_override": "PA",
        "confidence_boost": 0.3
    },

    # "We know" — dismissive, knowing tone
    "আমরা জানি তুমি": {
        "surface_meaning": "We know you",
        "hidden_meaning": "We know what you're really like",
        "emotion_override": "PA",
        "confidence_boost": 0.25
    },

    # "Were on right path BUT" — PA criticism with a compliment
    "সঠিক পথে ছিলেন কিন্তু": {
        "surface_meaning": "You were on the right path but",
        "hidden_meaning": "You failed/disappointed us",
        "emotion_override": "PA",
        "confidence_boost": 0.25
    },

    # "Didn't mention" — subtle criticism through omission
    "সম্পর্কে তো কিছু বললেন না": {
        "surface_meaning": "You didn't say anything about",
        "hidden_meaning": "You deliberately avoided this topic",
        "emotion_override": "PA",
        "confidence_boost": 0.2
    },

    # "Have to admit" — reluctant acknowledgment (PA)
    "মানতেই হবে": {
        "surface_meaning": "Have to admit",
        "hidden_meaning": "Reluctant, backhanded acknowledgment",
        "emotion_override": "PA",
        "confidence_boost": 0.15
    },
    "mante hobe": {
        "surface_meaning": "Have to admit",
        "hidden_meaning": "Reluctant acknowledgment",
        "emotion_override": "PA",
        "confidence_boost": 0.15
    },

    # "Was copied" — disguised criticism
    "অনেক কিছু কপি হয়েছে": {
        "surface_meaning": "Many things were copied",
        "hidden_meaning": "Criticizing as unoriginal while pretending to praise",
        "emotion_override": "PA",
        "confidence_boost": 0.2
    },

    # "Your advisors were sycophantic" — blaming others to criticize leader
    "উপদেষ্টা মন্ডলী গুলো দালালি করেছে": {
        "surface_meaning": "Your advisory board was sycophantic",
        "hidden_meaning": "Passive aggressive blame-shifting",
        "emotion_override": "PA",
        "confidence_boost": 0.2
    },

    # Standard PA phrases with romanized variants
    "আপনি ভালো আছেন তো": {
        "surface_meaning": "Are you okay?",
        "hidden_meaning": "Passive aggressive concern",
        "emotion_override": "PA",
        "confidence_boost": 0.2
    },
    "apni valo achen to": {
        "surface_meaning": "Are you okay?",
        "hidden_meaning": "Passive aggressive concern",
        "emotion_override": "PA",
        "confidence_boost": 0.2
    },
    "বুঝলাম": {
        "surface_meaning": "I understood",
        "hidden_meaning": "I disagree but won't argue",
        "emotion_override": "PA",
        "confidence_boost": 0.15
    },
    "bujhlam": {
        "surface_meaning": "I understood",
        "hidden_meaning": "Dismissive acknowledgment",
        "emotion_override": "PA",
        "confidence_boost": 0.15
    },

    # ══════════════════════════════════════════════════════════
    # ANGRY PHRASES (ANG)
    # ══════════════════════════════════════════════════════════

    # Drug insults — 100% ANG in data
    "গাজাখোর": {
        "surface_meaning": "Cannabis user",
        "hidden_meaning": "Strong insult calling someone a drug addict",
        "emotion_override": "ANG",
        "confidence_boost": 0.35
    },
    "গাঞ্জুট্টি": {
        "surface_meaning": "Drug user slang",
        "hidden_meaning": "Strong abusive insult",
        "emotion_override": "ANG",
        "confidence_boost": 0.35
    },
    "gajakhur": {
        "surface_meaning": "Cannabis user",
        "hidden_meaning": "Abusive insult",
        "emotion_override": "ANG",
        "confidence_boost": 0.35
    },
    "ganjutti": {
        "surface_meaning": "Drug addict slang",
        "hidden_meaning": "Abusive insult",
        "emotion_override": "ANG",
        "confidence_boost": 0.35
    },

    # Lowlife — 100% ANG in data
    "ছোটলোক": {
        "surface_meaning": "Small person",
        "hidden_meaning": "Lowlife/person with no class",
        "emotion_override": "ANG",
        "confidence_boost": 0.3
    },
    "chotolok": {
        "surface_meaning": "Lowlife",
        "hidden_meaning": "Abusive insult",
        "emotion_override": "ANG",
        "confidence_boost": 0.3
    },

    # Traitor — 100% ANG in political context
    "গাদ্দার": {
        "surface_meaning": "Traitor",
        "hidden_meaning": "Strong angry accusation",
        "emotion_override": "ANG",
        "confidence_boost": 0.3
    },
    "gaddar": {
        "surface_meaning": "Traitor",
        "hidden_meaning": "Strong angry accusation",
        "emotion_override": "ANG",
        "confidence_boost": 0.3
    },

    # Scammer — ANG(40%), GN(40%) — context dependent
    "বাটপারি": {
        "surface_meaning": "Fraudulent behavior",
        "hidden_meaning": "Calling out scam/fraud",
        "emotion_override": "ANG",
        "confidence_boost": 0.2
    },
    "batpari": {
        "surface_meaning": "Fraudulent behavior",
        "hidden_meaning": "Calling out scam",
        "emotion_override": "ANG",
        "confidence_boost": 0.2
    },

    # ══════════════════════════════════════════════════════════
    # GENUINE NEGATIVE (GN)
    # ══════════════════════════════════════════════════════════

    # Drug accusation words — mostly GN(62-80%) when used as description
    "নেশাখোর": {
        "surface_meaning": "Drug addict",
        "hidden_meaning": "Accusation/description (less intense than গাজাখোর)",
        "emotion_override": "GN",
        "confidence_boost": 0.2
    },
    "neshakhor": {
        "surface_meaning": "Drug addict",
        "hidden_meaning": "Negative accusation",
        "emotion_override": "GN",
        "confidence_boost": 0.2
    },

    # "Is high/stoned" — GN(50%) description
    "পিনিকে আছে": {
        "surface_meaning": "Is high/intoxicated",
        "hidden_meaning": "Negative accusation of drug use",
        "emotion_override": "GN",
        "confidence_boost": 0.2
    },
    "পিনিকে থাকে": {
        "surface_meaning": "Always stays high",
        "hidden_meaning": "Ongoing negative accusation",
        "emotion_override": "GN",
        "confidence_boost": 0.2
    },
    "pinike ache": {
        "surface_meaning": "Is high",
        "hidden_meaning": "Negative accusation",
        "emotion_override": "GN",
        "confidence_boost": 0.2
    },

    # Fake accusation — 100% GN in data
    "fake video": {
        "surface_meaning": "Fake video",
        "hidden_meaning": "Calling out misinformation",
        "emotion_override": "GN",
        "confidence_boost": 0.25
    },
    "fake unboxing": {
        "surface_meaning": "Fake unboxing",
        "hidden_meaning": "Calling out deceptive content",
        "emotion_override": "GN",
        "confidence_boost": 0.25
    },

    # ── ENGLISH NEGATIVE PHRASES (GN) ────────────────────────
    # Model trained mostly on Bengali — misses clear English negatives
    # Adding as direct overrides to fix GP bias on English negatives
    "terrible": {
        "surface_meaning": "Terrible",
        "hidden_meaning": "Strong negative sentiment",
        "emotion_override": "GN",
        "confidence_boost": 0.25
    },
    "worst": {
        "surface_meaning": "Worst",
        "hidden_meaning": "Extreme negative",
        "emotion_override": "GN",
        "confidence_boost": 0.25
    },
    "disappointed": {
        "surface_meaning": "Disappointed",
        "hidden_meaning": "Negative sentiment",
        "emotion_override": "GN",
        "confidence_boost": 0.2
    },
    "waste of money": {
        "surface_meaning": "Waste of money",
        "hidden_meaning": "Strong negative review",
        "emotion_override": "GN",
        "confidence_boost": 0.3
    },
    "very bad": {
        "surface_meaning": "Very bad",
        "hidden_meaning": "Clear negative",
        "emotion_override": "GN",
        "confidence_boost": 0.3
    },
    "not happy": {
        "surface_meaning": "Not happy",
        "hidden_meaning": "Dissatisfied",
        "emotion_override": "GN",
        "confidence_boost": 0.25
    },
    "never buying": {
        "surface_meaning": "Never buying again",
        "hidden_meaning": "Strong negative review",
        "emotion_override": "GN",
        "confidence_boost": 0.3
    },
    "what a pity": {
        "surface_meaning": "What a pity",
        "hidden_meaning": "Disappointment expression",
        "emotion_override": "GN",
        "confidence_boost": 0.25
    },
    "completely disappointed": {
        "surface_meaning": "Completely disappointed",
        "hidden_meaning": "Strong negative",
        "emotion_override": "GN",
        "confidence_boost": 0.3
    },

    # ── BENGALI NEGATIVE PHRASES (GN) ────────────────────────
    "একদম বাজে": {
        "surface_meaning": "Absolutely terrible",
        "hidden_meaning": "Strong negative review",
        "emotion_override": "GN",
        "confidence_boost": 0.3
    },
    "বাজে সার্ভিস": {
        "surface_meaning": "Bad service",
        "hidden_meaning": "Service complaint",
        "emotion_override": "GN",
        "confidence_boost": 0.3
    },
    "হতভাগ্য": {
        "surface_meaning": "Unfortunate/wretched",
        "hidden_meaning": "Expression of deep sadness/disappointment",
        "emotion_override": "GN",
        "confidence_boost": 0.25
    },
    "টিজার জমলো না": {
        "surface_meaning": "Teaser didn't land",
        "hidden_meaning": "Negative review of content",
        "emotion_override": "GN",
        "confidence_boost": 0.25
    },
    "ফালতু নিউজ": {
        "surface_meaning": "Useless news",
        "hidden_meaning": "Dismissive negative",
        "emotion_override": "GN",
        "confidence_boost": 0.25
    },

    # ── ROMANIZED BENGALI NEGATIVE (GN) ──────────────────────
    "ekdom bekar": {
        "surface_meaning": "Absolutely useless",
        "hidden_meaning": "Strong negative",
        "emotion_override": "GN",
        "confidence_boost": 0.3
    },
    "valo na": {
        "surface_meaning": "Not good",
        "hidden_meaning": "Negative assessment",
        "emotion_override": "GN",
        "confidence_boost": 0.25
    },
    "bekar product": {
        "surface_meaning": "Useless product",
        "hidden_meaning": "Negative product review",
        "emotion_override": "GN",
        "confidence_boost": 0.3
    },
    "bekar service": {
        "surface_meaning": "Useless service",
        "hidden_meaning": "Negative service review",
        "emotion_override": "GN",
        "confidence_boost": 0.3
    },

    # ══════════════════════════════════════════════════════════
    # GENUINE POSITIVE (GP)
    # ══════════════════════════════════════════════════════════

    # "Fire/Amazing" — Bangladeshi youth slang, 100% GP in data
    "পুরাই আগুন": {
        "surface_meaning": "Completely on fire",
        "hidden_meaning": "This is absolutely amazing! (Bangladeshi slang)",
        "emotion_override": "GP",
        "confidence_boost": 0.3
    },
    "পুরো আগুন": {
        "surface_meaning": "Completely amazing",
        "hidden_meaning": "Bangladeshi youth slang for amazing",
        "emotion_override": "GP",
        "confidence_boost": 0.3
    },
    "jast agun": {
        "surface_meaning": "Just fire/amazing",
        "hidden_meaning": "Bangladeshi slang for amazing",
        "emotion_override": "GP",
        "confidence_boost": 0.3
    },

    # "Will shake/rock" — positive anticipation
    "হল কাঁপাবে": {
        "surface_meaning": "Will shake the cinema hall",
        "hidden_meaning": "Will be a massive hit",
        "emotion_override": "GP",
        "confidence_boost": 0.25
    },
    "বক্স অফিস কাঁপাবে": {
        "surface_meaning": "Will shake the box office",
        "hidden_meaning": "Will be hugely successful",
        "emotion_override": "GP",
        "confidence_boost": 0.25
    },

    # Extraordinary — 100% GP
    "অসাধারণ": {
        "surface_meaning": "Extraordinary",
        "hidden_meaning": "Genuinely impressed",
        "emotion_override": "GP",
        "confidence_boost": 0.2
    },
    "osadharon": {
        "surface_meaning": "Extraordinary",
        "hidden_meaning": "Genuinely impressed",
        "emotion_override": "GP",
        "confidence_boost": 0.2
    },

    # Childhood nostalgia — 100% GP in data (শৈশব cluster)
    "শৈশবের কথা মনে পড়ে": {
        "surface_meaning": "Reminds me of childhood",
        "hidden_meaning": "Warm nostalgic positive emotion",
        "emotion_override": "GP",
        "confidence_boost": 0.2
    },
    "ছোটবেলার কথা মনে পড়ে": {
        "surface_meaning": "Reminds me of childhood",
        "hidden_meaning": "Nostalgic positive feeling",
        "emotion_override": "GP",
        "confidence_boost": 0.2
    },
    "সোনালী অতীত": {
        "surface_meaning": "Golden past",
        "hidden_meaning": "Warm nostalgic positive",
        "emotion_override": "GP",
        "confidence_boost": 0.2
    },

}


class CulturalContextChecker:
    def __init__(self):
        self.phrases = CULTURAL_PHRASES

    def check_comment(self, comment):
        """Check if comment contains any cultural phrase"""
        comment_lower = comment.lower().strip()
        matches = []
        for phrase, context in self.phrases.items():
            if phrase.lower() in comment_lower:
                matches.append({
                    'phrase': phrase,
                    'context': context
                })
        # Return the match with highest confidence boost
        if matches:
            best = max(matches, key=lambda x: x['context']['confidence_boost'])
            return {'found': True, 'phrase': best['phrase'], 'context': best['context'], 'all_matches': matches}
        return {'found': False}

    def adjust_prediction(self, comment, model_emotion, model_confidence):
        """Adjust model prediction if cultural phrase found"""
        check = self.check_comment(comment)
        if not check['found']:
            return model_emotion, model_confidence

        context = check['context']
        if context['emotion_override']:
            adjusted_emotion = context['emotion_override']
            adjusted_confidence = min(
                model_confidence + context['confidence_boost'],
                0.95
            )
            return adjusted_emotion, adjusted_confidence

        return model_emotion, model_confidence


# ── TEST ──────────────────────────────────────────────────────
if __name__ == "__main__":
    checker = CulturalContextChecker()

    test_comments = [
        # SAR
        ("আপনি কি ধোয়া তুলসী পাতা", "SAR"),
        ("কি ভাব দুধে ধোঁয়া তুলসীপাতা", "SAR"),
        ("নাটকের ভিতর নাটক", "SAR"),
        ("bah darun to", "SAR"),
        # PA
        ("এই মহানায়িকাকে এক সময় পছন্দ করতাম", "PA"),
        ("আমরা জানি তুমি তুলশী পাতা", "PA"),
        ("জুলাই সনদ সম্পর্কে তো কিছু বললেন না", "PA"),
        ("সঠিক পথে ছিলেন কিন্তু আপনার উপদেষ্টারা দালালি করেছে", "PA"),
        # ANG
        ("দেখলেই বোঝা যায় গাজাখোর", "ANG"),
        ("ছোটলোক যখন ক্রিকেটার", "ANG"),
        ("গাদ্দার ইউনুস", "ANG"),
        ("gajakhur sei lagce", "ANG"),
        # GN
        ("দেখেই মনে হচ্ছে নেশাখোর", "GN"),
        ("পিনিকে আছে দেখলেই বোঝা যায়", "GN"),
        ("fake video", "GN"),
        # GP
        ("পুরাই আগুন টিজার", "GP"),
        ("বক্স অফিস কাঁপাবে", "GP"),
        ("ছোটবেলার কথা মনে পড়ে গেলো", "GP"),
        # No match
        ("ডেলিভারি চার্জ কতো", "NEU"),
    ]

    print("Cultural Context Checker Test:\n")
    correct = 0
    for comment, expected in test_comments:
        result = checker.check_comment(comment)
        if result['found']:
            predicted = result['context']['emotion_override']
            match = "✅" if predicted == expected else "⚠️"
            if predicted == expected:
                correct += 1
            print(f"{match} '{comment[:50]}'")
            print(f"   Phrase: '{result['phrase']}'")
            print(f"   Override: {predicted} (expected: {expected})")
        else:
            match = "✅" if expected == "NEU" else "❌ MISSED"
            if expected == "NEU":
                correct += 1
            print(f"{match} '{comment[:50]}' → No match (expected: {expected})")
        print()

    print(f"Accuracy on test cases: {correct}/{len(test_comments)} ({correct/len(test_comments)*100:.0f}%)")