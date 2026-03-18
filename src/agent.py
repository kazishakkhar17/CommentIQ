# File: src/agent.py

from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from src.rag_user_history import UserHistoryRAG
from src.cultural_context_db import CulturalContextChecker
from src.negation_detector import NegationDetector
from src.spam_detector import SpamDetector
from src.question_detector import QuestionDetector
import torch

class CommentAnalysisAgent:
    def __init__(self, model_path='models/final_model'):
        print("Loading model...")
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSequenceClassification.from_pretrained(model_path)

        self.classifier = pipeline(
            "text-classification",
            model=model,
            tokenizer=tokenizer,
            return_all_scores=True,
            device=0 if torch.cuda.is_available() else -1
        )

        print("Loading tools...")
        self.rag = UserHistoryRAG()
        self.rag.load('models/rag_database.pkl')
        self.cultural_checker = CulturalContextChecker()
        self.negation_detector = NegationDetector()
        self.spam_detector = SpamDetector()
        self.question_detector = QuestionDetector()

        self.AUTO_REPLY_THRESHOLD = 0.60
        self.HUMAN_REVIEW_THRESHOLD = 0.40

        self.id2label = {
            'LABEL_0': 'GP',
            'LABEL_1': 'GN',
            'LABEL_2': 'SAR',
            'LABEL_3': 'PA',
            'LABEL_4': 'ANG',
            'LABEL_5': 'CON',
            'LABEL_6': 'NEU'
        }
        print("✅ Agent ready")

    def analyze(self, comment, user_id=None, use_rag=True):
        """Main analysis pipeline"""

        # Step 0: Spam check — hard exit, no reply
        spam_result = self.spam_detector.detect(comment)
        if spam_result['is_spam']:
            return {
                'comment': comment,
                'base_prediction': {'emotion': 'SPAM', 'confidence': 1.0},
                'tools_used': ['spam_detector'],
                'adjustments_made': [{
                    'tool': 'spam_detector',
                    'reason': spam_result['reason'],
                    'change': f"Spam type: {spam_result['spam_type']}"
                }],
                'final_prediction': {
                    'emotion': 'SPAM',
                    'confidence': 1.0,
                    'decision': 'NO_REPLY'
                }
            }

        # Step 1: Question check — runs FIRST before model
        # Questions have distinctive structure that model misses
        # Running early prevents model GP/NEU bias from blocking it
        question_result = self.question_detector.detect(comment)
        if question_result['is_question']:
            return {
                'comment': comment,
                'base_prediction': {'emotion': 'QUESTION', 'confidence': 0.90},
                'tools_used': ['question_detector'],
                'adjustments_made': [{
                    'tool': 'question_detector',
                    'reason': question_result['reason'],
                    'change': f"Detected as QUESTION"
                }],
                'final_prediction': {
                    'emotion': 'QUESTION',
                    'confidence': 0.90,
                    'decision': 'AUTO_REPLY'
                }
            }

        # Step 2: Model prediction
        raw_predictions = self.classifier(comment)
        if isinstance(raw_predictions[0], list):
            raw_predictions = raw_predictions[0]
        top_pred = max(raw_predictions, key=lambda x: x['score'])
        base_emotion = self.id2label.get(top_pred['label'], top_pred['label'])
        base_confidence = top_pred['score']

        analysis = {
            'comment': comment,
            'base_prediction': {
                'emotion': base_emotion,
                'confidence': round(base_confidence, 3)
            },
            'tools_used': [],
            'adjustments_made': []
        }

        # Step 3: Negation check
        negation_result = self.negation_detector.detect(comment)
        if negation_result['has_negation']:
            adjusted_emotion = self.negation_detector.flip_sentiment(base_emotion)
            if adjusted_emotion != base_emotion:
                analysis['tools_used'].append('negation_detector')
                analysis['adjustments_made'].append({
                    'tool': 'negation',
                    'reason': f"Found '{negation_result['negation_word']}' ({negation_result['language']})",
                    'change': f"{base_emotion} → {adjusted_emotion}"
                })
                base_emotion = adjusted_emotion

        # Step 4: Cultural context check
        cultural_result = self.cultural_checker.check_comment(comment)
        if cultural_result['found']:
            adj_emotion, adj_confidence = self.cultural_checker.adjust_prediction(
                comment, base_emotion, base_confidence
            )
            if adj_emotion != base_emotion:
                analysis['tools_used'].append('cultural_checker')
                analysis['adjustments_made'].append({
                    'tool': 'cultural_context',
                    'reason': f"Phrase '{cultural_result['phrase']}' detected",
                    'change': f"{base_emotion} → {adj_emotion}"
                })
                base_emotion = adj_emotion
                base_confidence = adj_confidence

        # Step 5: RAG user history
        if use_rag and user_id and base_confidence < 0.85:
            user_history = self.rag.retrieve_user_history(user_id, k=5)
            if user_history:
                analysis['tools_used'].append('user_history_rag')
                analysis['adjustments_made'].append({
                    'tool': 'user_history',
                    'reason': f"Retrieved {len(user_history)} past comments",
                    'insight': "User comment pattern analyzed"
                })

        # Step 6: Decision
        if base_confidence >= self.AUTO_REPLY_THRESHOLD:
            decision = "AUTO_REPLY"
        elif base_confidence >= self.HUMAN_REVIEW_THRESHOLD:
            decision = "HUMAN_REVIEW"
        else:
            decision = "FLAG_LOW_CONFIDENCE"

        analysis['final_prediction'] = {
            'emotion': base_emotion,
            'confidence': round(base_confidence, 3),
            'decision': decision
        }

        return analysis