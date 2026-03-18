from src.agent import CommentAnalysisAgent

agent = CommentAnalysisAgent()

test_comments = [
    # ── GENUINE POSITIVE (GP) ─────────────────────────────────
    # New products/contexts never in training
    ("ফোনটা হাতে পেয়ে মন ভরে গেল 😍",                    "gp_001"),
    ("রান্না করলাম রেসিপি দেখে একদম পারফেক্ট হয়েছে",      "gp_002"),
    ("বাচ্চার জন্য কিনলাম, ও অনেক খুশি হয়েছে",            "gp_003"),
    ("package খুললাম একদম নতুন এবং intact ছিল",            "gp_004"),
    ("First time bought from here, very impressed",          "gp_005"),
    ("Received within 2 days, super fast delivery",          "gp_006"),
    ("quality onekta better than expected honestly",         "gp_007"),
    ("bhai jinis ta pailam khub valo laglo",                 "gp_008"),
    ("ai app ta use kore onek shomoy bachlo amar",           "gp_009"),

    # ── GENUINE NEGATIVE (GN) ─────────────────────────────────
    # New complaint contexts
    ("প্যাকেজিং এতটাই খারাপ ছিল যে ভেতরের জিনিস ভেঙে গেছে","gn_001"),
    ("রঙ একদম আলাদা ছিল ছবির তুলনায়",                      "gn_002"),
    ("size chart follow করলাম তবু wrong size আসলো",          "gn_003"),
    ("Stitching came apart after first wash",                "gn_004"),
    ("The material feels super cheap and thin",              "gn_005"),
    ("Screen cracked on its own after 3 days",               "gn_006"),
    ("product er smell ta onek kharap chilo",                "gn_007"),
    ("color faded after one wash ekdom",                     "gn_008"),
    ("jinis ta picture te onek valo dekhachhilo kintu reality te bekar", "gn_009"),

    # ── SARCASTIC (SAR) ───────────────────────────────────────
    # New sarcastic contexts
    ("১৫ দিনে delivery এসেছে, super fast 👏",               "sar_001"),
    ("Customer service বলল দেখছি, ৭ দিন ধরে দেখছে 🙄",     "sar_002"),
    ("হ্যাঁ অবশ্যই এই দামে সোনার product পাওয়া যায়",       "sar_003"),
    ("packaging এত সুন্দর যে ভেতরে জিনিসটাই নেই",           "sar_004"),
    ("Oh sure the tracking says delivered but I have nothing","sar_005"),
    ("Great so they raised prices AND reduced quality",       "sar_006"),
    ("5 star service they called me once in 10 days",        "sar_007"),
    ("item ashe nai but SMS e bolche delivered, genius",     "sar_008"),
    ("haan haan amra sob bujhi kintu bolbo na 😏",            "sar_009"),

    # ── PASSIVE AGGRESSIVE (PA) ───────────────────────────────
    # New PA contexts
    ("আগে এই পেজ থেকে কিনতাম সমস্যা হতো না",               "pa_001"),
    ("বাকিরা হয়তো পেয়েছে, আমার টা শুধু আসেনি",             "pa_002"),
    ("response দিলেন ঠিকই কিন্তু সমাধান হলো না",            "pa_003"),
    ("Nice to know others got their orders fine",             "pa_004"),
    ("apnar page follow kortam onek din, akhon ar jani na",  "pa_005"),
    ("ekta reply pailam shotti, problem solve hoini though", "pa_006"),

    # ── ANGRY (ANG) ───────────────────────────────────────────
    # New angry contexts
    ("টাকা কেটে নিয়েছে কিন্তু কোনো confirmation নেই",       "ang_001"),
    ("এই পেজকে report করবো সবাই সাবধান থাকুন",              "ang_002"),
    ("৩ বার ফোন করেছি কেউ তোলে না এটা কি ব্যবসা",          "ang_003"),
    ("You took my money and disappeared, this is theft",      "ang_004"),
    ("Absolutely furious right now this is unacceptable",     "ang_005"),
    ("money kaite nilo jinis dilo na ei holo apnar business", "ang_006"),
    ("vai tumi ki manush na robot reply dao ektu",            "ang_007"),
    ("report dibo consumer rights e dekhi ki hoy",           "ang_008"),

    # ── CONCERNED (CON) ───────────────────────────────────────
    # New concern contexts
    ("এই উপাদানগুলো কি শিশুদের জন্য নিরাপদ?",               "con_001"),
    ("expiry date দেখে কিনুন সবাই, সাবধান",                 "con_002"),
    ("রাস্তার অবস্থা দেখে মনে হচ্ছে সরকার জানে না",         "con_003"),
    ("Is this product tested for allergies? Please clarify", "con_004"),
    ("Everyone please check ingredients before buying this", "con_005"),
    ("product er side effect niye karo jano thakle janaben", "con_006"),

    # ── NEUTRAL (NEU) ─────────────────────────────────────────
    # New neutral contexts
    ("হাতে পেলাম, দেখি কেমন হয়",                           "neu_001"),
    ("অর্ডার করা হয়েছে",                                    "neu_002"),
    ("Received the package today",                           "neu_003"),
    ("product use korchi, review dibo pore",                 "neu_004"),
    ("notun stock aiche dekhlam",                            "neu_005"),

    # ── QUESTION ──────────────────────────────────────────────
    # New question contexts
    ("এই cream টা কি oily skin এ কাজ করে?",                 "question_001"),
    ("return করতে চাইলে কত দিনের মধ্যে করতে হবে?",          "question_002"),
    ("ঢাকার বাইরে কত দিনে পাবো?",                           "question_003"),
    ("Do you have this in size XL?",                         "question_004"),
    ("Is there any warranty on this product?",               "question_005"),
    ("exchange possible if size is wrong?",                  "question_006"),
    ("vai cod ache ki ei product e?",                        "question_007"),
    ("sylhet e deliver koro?",                               "question_008"),

    # ── SPAM ──────────────────────────────────────────────────
    # New spam styles
    ("Earn 5000tk daily from home click here bit.ly/xyz",   "spam_001"),
    ("আমার পেজে গেলে ৫০% ছাড় পাবেন follow করুন",           "spam_002"),
    ("FREE iPhone giveaway join our group now!!!",           "spam_003"),
]

expected_map = {
    'gp':       'GP',
    'gn':       'GN',
    'sar':      'SAR',
    'pa':       'PA',
    'ang':      'ANG',
    'con':      'CON',
    'neu':      'NEU',
    'question': 'QUESTION',
    'spam':     'SPAM',
}

print(f"\n{'Comment':<52} {'Exp':<9} {'Got':<9} {'Conf':<6} {'Decision':<22} {'Tools'}")
print("─" * 122)

correct = 0
total = 0
emotion_results = {}

for comment, user_id in test_comments:
    expected_key = user_id.split('_')[0]
    expected = expected_map.get(expected_key, '?')

    result = agent.analyze(comment, user_id)
    pred = result['final_prediction']
    got = pred['emotion']
    tools = ','.join(result['tools_used']) if result['tools_used'] else '-'

    match = "✅" if got == expected else "❌"
    if got == expected:
        correct += 1
    total += 1

    if expected not in emotion_results:
        emotion_results[expected] = {'correct': 0, 'total': 0}
    emotion_results[expected]['total'] += 1
    if got == expected:
        emotion_results[expected]['correct'] += 1

    print(f"{match} {comment[:51]:<52} {expected:<9} {got:<9} {pred['confidence']:.2f}  {pred['decision']:<22} {tools}")

print("\n" + "─" * 122)
print(f"\nOverall Accuracy: {correct}/{total} ({correct/total*100:.0f}%)")
print("\nPer-emotion Accuracy:")
for em, res in sorted(emotion_results.items()):
    pct = res['correct']/res['total']*100
    bar = '█' * res['correct'] + '░' * (res['total'] - res['correct'])
    print(f"  {em:<9}: {bar} {res['correct']}/{res['total']} ({pct:.0f}%)")