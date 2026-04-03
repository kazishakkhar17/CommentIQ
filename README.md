# CommentIQ — Emotional Intelligence for Facebook Comments

Detects emotional intent in Bengali, English, and Romanized-Bengali Facebook comments and generates contextually appropriate auto-replies. Built in 5 days as an end-to-end ML + agentic AI project.


**Live Demo:** Run locally with `uvicorn api:app --host 0.0.0.0 --port 7860`

## Screenshots
<img width="1907" height="882" alt="Screenshot 2026-03-19 115304" src="https://github.com/user-attachments/assets/233729c7-fd38-4580-9165-594faf94083c" />
<img width="1885" height="898" alt="Screenshot 2026-03-19 115821" src="https://github.com/user-attachments/assets/00a43ff8-e5be-4f24-8a9c-4220078aa967" />
<img width="1903" height="894" alt="Screenshot 2026-03-19 115925" src="https://github.com/user-attachments/assets/79c6adb1-fd25-4f3f-9b46-deda9be95481" />


---
## What It Does

Bangladeshi businesses receive hundreds of Facebook comments daily in Bengali, English, and code-mixed language. Existing tools fail because they don't understand Bengali sarcasm, miss cultural passive-aggression, and can't handle code-mixed text.

CommentIQ solves this with a two-layer system:

- **Type-2 model** — fine-tuned XLM-RoBERTa that classifies comments into 7 emotions
- **Type-1 agent** — sits on top of the model, uses 5 tools to fix systematic failures, then routes to auto-reply, human review, or no-reply

---

## Demo UI

Three panels in one web interface:

**User panel** — simulates a Facebook comment section. User types a comment, sees either an instant auto-reply or "Our team will respond shortly."

**Admin inbox** — pending messages appear here with AI analysis (emotion, confidence, tools used, adjustments made) and an editable suggested reply. Admin clicks Send — reply appears instantly in the user panel.

**History** — all comments and replies (auto and manual) with emotion tags and timestamps.

---

## Architecture
```
Facebook Comment
      ↓
Spam Detector ——→ NO_REPLY (spam/links/self-promotion)
      ↓
Question Detector ——→ AUTO_REPLY (inquiry response)
      ↓
XLM-RoBERTa Model (7-class emotion prediction)
      ↓
Negation Detector (flips GP↔GN when negation found)
      ↓
Cultural Context DB (overrides emotion for known phrases)
      ↓
RAG User History (retrieves past comments for context)
      ↓
Confidence Thresholding
  ≥ 60% → AUTO_REPLY
  40-59% → HUMAN_REVIEW
  < 40% → FLAG_LOW_CONFIDENCE
      ↓
Response Generator (random template from 3-4 options per emotion)
```

---

## Type-2 Model

**Base model:** XLM-RoBERTa-base (multilingual)

**Dataset:** 838 manually labeled Facebook comments
- Sources: 20 pages — news, telecom, ecommerce, entertainment, sports, meme pages
- Languages: Bengali 67%, Romanized Bengali 15%, English 11%, Mixed 7%
- Labels: 7 emotions (GP, GN, SAR, PA, ANG, CON, NEU)

**Emotion distribution:**

| Emotion | Count | % |
|---|---|---|
| GP — Genuine Positive | 204 | 24% |
| SAR — Sarcastic | 156 | 19% |
| NEU — Neutral | 141 | 17% |
| ANG — Angry | 119 | 14% |
| GN — Genuine Negative | 113 | 13% |
| CON — Concerned | 91 | 11% |
| PA — Passive Aggressive | 14 | 2% |

**Training:**

| Parameter | Value |
|---|---|
| Approach | Full fine-tuning (LoRA failed — see Known Issues) |
| Epochs | 10 (best at epoch 8) |
| Learning rate | 2e-5 |
| Batch size | 16 |
| Optimizer | AdamW |
| Hardware | Tesla T4 GPU (Google Colab) |
| Training time | ~20 minutes |

**Results:**

| Metric | Value |
|---|---|
| Test accuracy | 57% |
| Weighted F1 | 0.55 |
| Baseline F1 | 0.10 |
| Improvement | 5.5x over baseline |

**Per-class performance:**

| Emotion | Precision | Recall | F1 |
|---|---|---|---|
| NEU | 0.79 | 0.86 | 0.83 |
| GP | 0.60 | 0.80 | 0.69 |
| SAR | 0.52 | 0.48 | 0.50 |
| CON | 0.47 | 0.50 | 0.48 |
| ANG | 0.46 | 0.33 | 0.39 |
| GN | 0.38 | 0.29 | 0.33 |
| PA | 0.00 | 0.00 | 0.00 |

---

## Failure Analysis

96 errors on test set were manually reviewed and categorized:

| Failure | Count | % | Root Cause |
|---|---|---|---|
| GP_BIAS | 49 | 51% | Class imbalance — model defaults to majority class |
| SAR_NO_EMOJI | 18 | 19% | Sarcasm without emoji cues |
| AMBIGUOUS | 11 | 11% | Genuinely hard to classify |
| CODE_MIX | 9 | 9% | Romanized Bengali not handled |
| DOMAIN_INSULT | 7 | 7% | Slang/insult words look neutral |
| LABEL_ERROR | 1 | 1% | Incorrect original label |

Each failure category maps directly to a Type-1 agent component — this analysis motivated and justified every tool built in the agent system.

**Note on real-world accuracy:** Raw F1=0.55 underestimates practical performance. Emotionally adjacent classes share the same response strategy (GP/CON/NEU → friendly, GN/ANG/PA/SAR → apologetic). Response-level accuracy is estimated at ~0.72.

---

## Type-1 Agent System

Five tools built on top of the model:

**1. Spam Detector**
Catches links, self-promotion phrases, fake offers. Hard exit — no reply sent.
Patterns: URLs, "visit my page", "আমার পেজ", "free gift", etc.

**2. Question Detector**
Detects inquiries before the model runs. Catches question marks in short comments, Bengali question phrases (কিভাবে, কত), Romanized variants, English question phrases (how much, when will, can you).
Routes directly to a helpful inquiry response.

**3. Negation Detector**
Catches negation words and flips GP↔GN.
Handles Unicode Bengali (না, নেই, নয়), Romanized Bengali (na, nai, nah), English (not, never, n't).
100% accuracy on test cases.

**4. Cultural Context Database**
Phrases with hidden meanings in Bengali culture that the model consistently misses.
Covers passive-aggressive phrases, sarcasm patterns, domain insults, double negation.
Built directly from failure analysis cases. 95% accuracy on known phrases.

**5. RAG User History**
FAISS vector database of user comment history (586 entries from training data).
Retrieves past comments when model confidence is low.
Embedding model: paraphrase-multilingual-MiniLM-L12-v2.

**Decision thresholds:**
- ≥ 60% confidence → AUTO_REPLY
- 40–59% → HUMAN_REVIEW
- < 40% → FLAG_LOW_CONFIDENCE
- Spam → NO_REPLY

---

## Project Structure
```
CommentIQ/
├── api.py                          # FastAPI backend + UI server
├── ui.html                         # Full frontend (served by FastAPI)
├── app.py                          # Gradio wrapper (alternative)
├── requirements.txt
├── docs/
│   └── model.md                    # Model download instructions
├── data/
│   └── labeled/
│       ├── labeled_comments.csv    # Full 838-row dataset
│       ├── train.csv               # 586 training examples
│       ├── val.csv                 # 126 validation examples
│       └── test.csv                # 126 test examples
├── src/
│   ├── agent.py                    # Main agent pipeline
│   ├── cultural_context_db.py      # Bengali phrase database
│   ├── negation_detector.py        # Negation handling
│   ├── spam_detector.py            # Spam detection
│   ├── question_detector.py        # Question routing
│   ├── rag_user_history.py         # FAISS RAG system
│   └── response_generator.py      # Template-based responses
├── notebooks/
│   ├── 02_baseline_test.ipynb
│   └── 03_error_analysis_and_categorization.ipynb
└── outputs/
    ├── TYPE2_FINAL_REPORT.md
    ├── confusion_matrix_day2.png
    ├── top_50_errors.csv
    ├── failure_categories.csv
    └── failure_to_solution_mapping.md
```

---

## Setup

**1. Clone the repo:**
```bash
git clone https://github.com/kazishakkhar17/CommentIQ.git
cd CommentIQ
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Download the model:**
See `docs/model.md` for the Google Drive download link.
Extract into `models/final_model/`.

**4. Run:**
```bash
uvicorn api:app --host 0.0.0.0 --port 7860
```

Open `http://localhost:7860`

---

## Known Issues & Limitations

**LoRA compatibility failure:**
LoRA fine-tuning was attempted with `peft==0.18.1` and `transformers==5.3.0`. A compatibility issue caused gradients not to flow (grad=False for all parameters), resulting in F1=0.10 regardless of rank. Full fine-tuning was used as a workaround. LoRA ablation study (r=8, r=16, r=32) was therefore skipped.

**GP class bias:**
51% of errors are caused by the model defaulting to GP when uncertain. Root cause is class imbalance — GP has 204 training examples while PA has only 14. Confidence thresholding in the agent mitigates this by routing uncertain predictions to human review.

**PA class:**
F1=0.00 on passive-aggressive class due to only 14 training examples. The cultural context database partially compensates for specific known PA phrases.

**Dataset size:**
838 comments is small for a 7-class problem. Overfitting observed after epoch 8. A larger dataset (5,000+) would significantly improve all metrics.

**Response language:**
Responses are auto-detected as Bengali or English based on character composition. Mixed-language comments default to Bengali.

---

## Tech Stack

| Component | Technology |
|---|---|
| Model training | PyTorch, Hugging Face Transformers |
| Base model | XLM-RoBERTa-base |
| RAG | FAISS, Sentence Transformers |
| Backend | FastAPI, Uvicorn |
| Frontend | Vanilla HTML/CSS/JS |
| Data processing | Pandas, Scikit-learn |

---

## Author

**Kazi Shakkhar Rahman**

GitHub: [kazishakkhar17](https://github.com/kazishakkhar17)

---

## What I Would Do With More Time

- Expand dataset to 5,000+ comments to fix class imbalance
- Retrain with balanced classes — specifically collect 100+ PA examples
- Implement real Facebook webhook integration
- Add LLM-based dynamic response generation
- Build analytics dashboard for admins
- Add Hindi and Urdu language support
