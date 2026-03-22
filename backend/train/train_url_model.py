import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

def generate_synthetic_url_data(n_samples=1000):
    # Features: length, has_ip, num_special_chars, has_https, is_shortened, contains_fintech_brand
    data = []
    labels = []
    
    for _ in range(n_samples // 2):
        # Legit Data (Label 0)
        data.append([
            np.random.randint(15, 60), # length
            0, # has_ip
            np.random.randint(0, 3), # specials
            1, # has_https
            0, # is_shortened
            np.random.choice([0, 1], p=[0.9, 0.1]) # fintech
        ])
        labels.append(0)
        
    for _ in range(n_samples // 2):
        # Phishing Data (Label 1)
        data.append([
            np.random.randint(40, 150), # length
            np.random.choice([0, 1], p=[0.7, 0.3]), # has_ip
            np.random.randint(2, 10), # specials
            np.random.choice([0, 1], p=[0.6, 0.4]), # has_https (phishing often uses HTTP)
            np.random.choice([0, 1], p=[0.8, 0.2]), # is_shortened
            np.random.choice([0, 1], p=[0.4, 0.6]) # fake fintech
        ])
        labels.append(1)
        
    df = pd.DataFrame(data, columns=['length', 'has_ip', 'num_special_chars', 'has_https', 'is_shortened', 'contains_fintech_brand'])
    return df, np.array(labels)

def train_and_save_model():
    print("Generating synthetic URL data...")
    X, y = generate_synthetic_url_data()
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    preds = clf.predict(X_test)
    print("\nModel Performance:")
    print(classification_report(y_test, preds))
    
    os.makedirs('models', exist_ok=True)
    model_path = os.path.join('models', 'url_model.pkl')
    joblib.dump(clf, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_and_save_model()
