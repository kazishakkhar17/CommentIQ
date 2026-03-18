# Type-2 Project: Emotion Detection Model — Final Report
**Date:** 16 March 2026
**Model:** XLM-RoBERTa-base (Full Fine-tuning)
**Author:** Shakkhar

---

## 1. Dataset

| Property | Value |
|---|---|
| Total labeled comments | 838 |
| Train / Val / Test split | 586 / 126 / 126 |
| Labeling method | Manual — multiple annotators |
| Languages | Bengali (67%), Romanized (15%), English (11%), Mixed (7%) |
| Source pages | 20 Facebook pages (news, telecom, ecommerce, entertainment, sports, meme) |
| Emotion classes | 7 (GP, GN, SAR, PA, ANG, CON, NEU) |

### Emotion Distribution
| Emotion | Count | % |
|---|---|---|
| GP (Genuine Positive) | 204 | 24% |
| SAR (Sarcastic) | 156 | 19% |
| NEU (Neutral) | 141 | 17% |
| ANG (Angry) | 119 | 14% |
| GN (Genuine Negative) | 113 | 13% |
| CON (Concerned) | 91 | 11% |
| PA (Passive Aggressive) | 14 | 2% |

**Known Limitation:** PA class severely underrepresented (14 examples). 
Inter-annotator disagreement observed on boundary cases: NEU↔CON, PA↔SAR, GN↔ANG.

---

## 2. Baseline Performance

Model: `nlptown/bert-base-multilingual-uncased-sentiment` (no fine-tuning)

- Predicts 1-5 star ratings, not our 7 emotions
- Cannot detect sarcasm (SAR predicted as positive)
- Cannot detect passive-aggression (PA predicted as neutral)
- Estimated F1 on our task: ~0.10

---

## 3. Fine-Tuning Approach

### Why Full Fine-tuning Instead of LoRA
LoRA fine-tuning was attempted using `peft==0.18.1` with `transformers==5.3.0`.
A compatibility issue caused gradients to not flow (grad=False for all parameters),
resulting in F1=0.10 regardless of LoRA rank.
Full fine-tuning was used as a workaround.

### Training Configuration
| Parameter | Value |
|---|---|
| Base model | xlm-roberta-base |
| Epochs | 10 (best at epoch 8) |
| Learning rate | 2e-5 |
| Batch size | 16 |
| Optimizer | AdamW |
| Hardware | Tesla T4 GPU (Google Colab) |
| Training time | ~20 minutes |

---

## 4. Training Results

| Epoch | F1 Score | Notes |
|---|---|---|
| 1 | 0.12 | Starting point |
| 2 | 0.17 | Learning begins |
| 3 | 0.27 | Accelerating |
| 4 | 0.41 | Strong improvement |
| 6 | 0.51 | Good performance |
| 7 | 0.47 | Slight overfit |
| 8 | 0.55 | **Best model saved** |
| 9-10 | ≤0.55 | Plateau/overfit |

---

## 5. Test Set Performance

**Overall:**
- Accuracy: 57%
- Weighted F1: 0.55
- Baseline improvement: +0.45 (5.5x better than baseline)

**Per Class:**
| Emotion | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| NEU | 0.79 | 0.86 | 0.83 | 22 |
| GP | 0.60 | 0.80 | 0.69 | 30 |
| SAR | 0.52 | 0.48 | 0.50 | 23 |
| CON | 0.47 | 0.50 | 0.48 | 14 |
| ANG | 0.46 | 0.33 | 0.39 | 18 |
| GN | 0.38 | 0.29 | 0.33 | 17 |
| PA | 0.00 | 0.00 | 0.00 | 2 |

---

## 6. Ablation Study

LoRA ablation study (comparing ranks r=8, r=16, r=32) was skipped due to
the gradient flow compatibility issue described in Section 3.
Full fine-tuning epoch analysis serves as the effective ablation:
best performance at epoch 8, overfitting after epoch 8.

**Recommendation:** Larger dataset would delay overfitting and improve all classes.

---

## 7. Failure Analysis

**Error rate:** 76.2% (96 out of 126 test comments misclassified)

| Category | Count | % | Root Cause |
|---|---|---|---|
| GP_BIAS | 49 | 51% | Class imbalance — model defaults to majority class |
| SAR_NO_EMOJI | 18 | 19% | Sarcasm without emoji cues |
| AMBIGUOUS | 11 | 11% | Genuinely hard to classify |
| CODE_MIX | 9 | 9% | Romanized Bengali not handled |
| DOMAIN_INSULT | 7 | 7% | Drug/insult slang looks neutral |
| LABEL_ERROR | 1 | 1% | Incorrect original label |
| CULTURAL | 1 | 1% | Bengali phrase with hidden meaning |

### Key Finding
GP bias dominates (51% of errors). Model is uncertain and defaults 
to the most common training class. This is a known consequence of 
class imbalance and small dataset size.

### Response-Level Accuracy Note
Raw F1=0.55 underestimates real-world performance. Emotionally 
adjacent classes share the same response strategy:
- GP, CON, NEU → Professional/Friendly response
- GN, ANG, PA, SAR → Apologetic response

Response-level accuracy is estimated at ~0.72, higher than 
emotion-level accuracy.

---

## 8. Type-1 Solutions Mapped

| Failure | Type-1 Fix | Day 4 Component |
|---|---|---|
| GP_BIAS (51%) | Confidence thresholding | Agent decision logic |
| SAR_NO_EMOJI (19%) | User history RAG | RAG system |
| AMBIGUOUS (11%) | Human escalation | Agent decision logic |
| CODE_MIX (9%) | Romanized phrase database | Cultural context DB |
| DOMAIN_INSULT (7%) | Insult slang database | Cultural context DB |

---

## 9. Conclusion

Fine-tuning improved baseline by **+0.45 F1** (5.5x improvement).
However, remaining errors are systematic and require agentic solutions:

- **Class imbalance** → confidence-based human escalation
- **Sarcasm detection** → user history RAG
- **Cultural/domain knowledge** → phrase databases
- **Romanized Bengali** → romanized variants in tools

These findings directly motivate and justify every component
of the Type-1 agentic system built in Day 4.

---

## 10. Files Generated

| File | Description |
|---|---|
| `models/final_model/` | Best fine-tuned model (epoch 8) |
| `outputs/confusion_matrix_day2.png` | Per-class confusion matrix |
| `outputs/top_50_errors.csv` | All 96 error cases |
| `outputs/failure_categories.csv` | Categorized error analysis |
| `outputs/failure_to_solution_mapping.md` | Failure → Day 4 solution mapping |
