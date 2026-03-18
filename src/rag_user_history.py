# File: src/rag_user_history.py

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd
import pickle
import os

class UserHistoryRAG:
    def __init__(self):
        # Multilingual embedding model — understands Bengali, English, Romanized
        self.embedder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        
        # FAISS index for fast similarity search
        # dimension=384 because MiniLM produces 384-dimensional vectors
        self.dimension = 384
        self.index = faiss.IndexFlatL2(self.dimension)
        
        # Store comments and user IDs in parallel lists
        # index position links them: comments[i] belongs to user_ids[i]
        self.comments = []
        self.user_ids = []

    def add_user_comments(self, user_id, comments_list):
        """Add a user's comments to the RAG database"""
        for comment in comments_list:
            # Convert text to vector (384 numbers)
            embedding = self.embedder.encode(comment)
            # Add vector to FAISS index
            self.index.add(np.array([embedding], dtype='float32'))
            # Store metadata
            self.comments.append(comment)
            self.user_ids.append(user_id)

    def retrieve_user_history(self, user_id, k=5):
        """Get last k comments from a specific user"""
        user_comments = [
            c for c, uid in zip(self.comments, self.user_ids)
            if uid == user_id
        ]
        return user_comments[-k:]

    def retrieve_similar_comments(self, query_comment, k=3):
        """Find k most similar comments in database"""
        query_embedding = self.embedder.encode(query_comment)
        distances, indices = self.index.search(
            np.array([query_embedding], dtype='float32'), k
        )
        results = []
        for idx in indices[0]:
            results.append({
                'comment': self.comments[idx],
                'user_id': self.user_ids[idx]
            })
        return results

    def save(self, path='models/rag_database.pkl'):
        """Save entire RAG database to disk"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data = {
            'comments': self.comments,
            'user_ids': self.user_ids,
            'index': faiss.serialize_index(self.index)
        }
        with open(path, 'wb') as f:
            pickle.dump(data, f)
        print(f"✅ RAG database saved: {len(self.comments)} comments")

    def load(self, path='models/rag_database.pkl'):
        """Load RAG database from disk"""
        with open(path, 'rb') as f:
            data = pickle.load(f)
        self.comments = data['comments']
        self.user_ids = data['user_ids']
        self.index = faiss.deserialize_index(data['index'])
        print(f"✅ RAG database loaded: {len(self.comments)} comments")


# ── BUILD AND TEST ────────────────────────────────────────────
if __name__ == "__main__":
    print("Building RAG database from training data...")
    rag = UserHistoryRAG()

    # Load training data — simulate user history
    # In real app user IDs come from Facebook API
    # Here we group by emotion to create fake user patterns
    train_df = pd.read_csv('data/labeled/train.csv')

    for idx, row in train_df.iterrows():
        # 10 simulated users per emotion type
        user_id = f"user_{row['emotion']}_{idx % 10}"
        rag.add_user_comments(user_id, [row['comment_text']])

    # Save database
    rag.save('models/rag_database.pkl')

    # Test retrieval
    test_user = "user_SAR_0"
    history = rag.retrieve_user_history(test_user, k=3)
    print(f"\nTest — {test_user}'s comment history:")
    for i, comment in enumerate(history, 1):
        print(f"  {i}. {comment[:60]}...")

    # Test similarity search
    print("\nTest — similar comments to 'বাহ কি সুন্দর':")
    similar = rag.retrieve_similar_comments('বাহ কি সুন্দর', k=3)
    for s in similar:
        print(f"  [{s['user_id']}]: {s['comment'][:60]}...")