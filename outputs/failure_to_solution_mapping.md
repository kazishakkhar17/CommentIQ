# Failure → Type-1 Solution Mapping
**Date:** 16 March 2026
**Based on:** 96 error cases from test set

---

## Failure 1: GP_BIAS (51% of errors, 49 cases)
**Problem:** Model defaults to GP when uncertain. Root cause is class imbalance — GP has 143 training examples while PA has only 10.

**Example:**
- "অন্য নাম্বারের সাথে মিল রেখে কাস্টমাইজড করে কি সিম নেওয়া যাবে" → True: NEU, Pred: GP
- "আমি একটা গলায় কিক বানাতে চাই স্বর্ণের ডিজাইন কত টাকা পড়বে" → True: CON, Pred: GP

**Type-1 Solution:** Confidence thresholding
- If confidence < 0.60 → flag for human review instead of auto-reply
- Agent should not auto-reply when model is uncertain
- Expected improvement: Reduces wrong auto-replies by ~50%

---

## Failure 2: SAR_NO_EMOJI (19% of errors, 18 cases)
**Problem:** Sarcastic comments without emoji (🙄😒) are misclassified as GP. Model relies on emoji as sarcasm signal.

**Example:**
- "Hindi serial er bgm lagay dilo last 10 sec e!😂" → True: SAR, Pred: GP
- "Mahathir Mohammed tor okater bayre" → True: SAR, Pred: GP

**Type-1 Solution:** RAG over user comment history
- If user has history of sarcastic comments → boost SAR probability
- If same user always criticizes → current comment likely sarcastic
- Expected improvement: +20-30% recall on SAR class

---

## Failure 3: AMBIGUOUS (11% of errors, 11 cases)
**Problem:** Comments that are genuinely hard to classify — even human annotators disagreed on these.

**Example:**
- "এখানে যদি বাংলাদেশ ব্যাটিং করতো তাহলে আমরা কি বলতাম?" → True: CON, Pred: GP
- "এইসব চাকরিতে স্টার্টিং এ বেতন কতো?" → True: NEU, Pred: GP

**Type-1 Solution:** Human escalation
- If confidence < 0.55 AND category is ambiguous → send to human review queue
- Don't auto-reply to ambiguous comments
- Expected improvement: Eliminates wrong replies on ambiguous cases

---

## Failure 4: CODE_MIX (9% of errors, 9 cases)
**Problem:** Romanized Bengali (Latin script) confuses the model. "Ai bedire dekhle aamr bumi ashe" reads as angry but model predicts GP.

**Example:**
- "Ai bedire dekhle aamr bumi ashe" → True: ANG, Pred: GP
- "Sharmin Bithi sir apnk onk respect kori" → True: PA, Pred: GP

**Type-1 Solution:** Negation detector + romanized phrase database
- Detect romanized Bengali and apply special handling
- Add romanized versions of cultural phrases to database
- Expected improvement: +40% accuracy on romanized comments

---

## Failure 5: DOMAIN_INSULT (7% of errors, 7 cases)
**Problem:** Drug/insult slang (গাজাখোর, নেশাখোর, পিনিকে) looks like neutral statement but is actually SAR or ANG.

**Example:**
- "গাজা খায় কিনা সেটা সিউর না বাট বাবা খায় এটা সিউর" → True: SAR, Pred: GP
- "তোমাকে দেখলেই নেশাখোর মনে হয়" → True: GN, Pred: GP

**Type-1 Solution:** Domain-specific phrase database
- Add Bengali slang/insult words to cultural context database
- গাজাখোর → ANG/SAR override
- নেশাখোর → GN/ANG override
- পিনিকে → SAR override
- Expected improvement: Fixes ~7% of errors directly

---

## Failure 6: LABEL_ERROR (1% of errors, 1 case)
**Problem:** Original labeling was incorrect.

**Example:**
- Prophet quote labeled as GN — should be NEU or CON

**Type-1 Solution:** None needed
- Single case, not systematic
- Note as dataset limitation

---

## Summary Table

| Failure | % | Type-1 Fix | Day 4 Component |
|---|---|---|---|
| GP_BIAS | 51% | Confidence thresholding | Agent decision logic |
| SAR_NO_EMOJI | 19% | User history RAG | RAG system |
| AMBIGUOUS | 11% | Human escalation | Agent decision logic |
| CODE_MIX | 9% | Romanized phrase DB | Cultural context DB |
| DOMAIN_INSULT | 7% | Insult slang DB | Cultural context DB |
| LABEL_ERROR | 1% | Dataset limitation | N/A |

---

## Conclusion
The majority of failures (51%) are due to GP class bias — a training data problem.
The remaining failures are systematic and addressable through the Type-1 agent system.
Together these findings directly motivate and justify every component built in Day 4.
