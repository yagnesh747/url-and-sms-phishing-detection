import os
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Ensure models directory exists
os.makedirs("models", exist_ok=True)

def train_smishing_model():
    print("Training Smishing Detection Model...")
    # Mock data for demonstration purposes
    data = {
        "text": [
            "Your SBI account is blocked. Update PAN here http://bit.ly/update-pan",
            "Hey mom, can you call me later?",
            "Urgent KYC needed for your HDFC wallet. Click link to verify.",
            "Meeting at 5 PM tomorrow in the conference room.",
            "You have won £1,000,000. Reply with bank details.",
        ],
        "label": [1, 0, 1, 0, 1] # 1 = Smishing, 0 = Safe
    }
    df = pd.DataFrame(data)
    
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000)),
        ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)
    pipeline.fit(X_train, y_train)
    
    preds = pipeline.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, preds)}")
    
    joblib.dump(pipeline, "models/smishing_model.pkl")
    print("Saved smishing model to models/smishing_model.pkl\n")

def train_url_model():
    print("Training URL Model Placeholder (Feature-based)...")
    # A real model would train on extracted lexical/host features
    # Here we simulate with a simple array [length, has_ip, num_special_chars, has_https]
    data = {
        "length": [120, 20, 80, 25, 200],
        "has_ip": [1, 0, 1, 0, 1],
        "num_special_chars": [5, 0, 3, 1, 10],
        "has_https": [0, 1, 1, 1, 0],
        "label": [1, 0, 1, 0, 1]
    }
    df = pd.DataFrame(data)
    features = df[['length', 'has_ip', 'num_special_chars', 'has_https']]
    
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(features, df['label'])
    
    joblib.dump(clf, "models/url_model.pkl")
    print("Saved URL model to models/url_model.pkl")

if __name__ == "__main__":
    train_smishing_model()
    train_url_model()
