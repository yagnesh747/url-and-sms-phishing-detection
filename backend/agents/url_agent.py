import re
import joblib
import os
from pydantic import BaseModel

class URLAgentResult(BaseModel):
    is_phishing: bool
    confidence: float
    features: dict

class URLAnalysisAgent:
    def __init__(self):
        # We try to load a model; if it doesn't exist, we fallback to heuristics
        self.model_path = "models/url_model.pkl"
        self.model = None
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)

    def extract_features(self, url: str) -> dict:
        features = {}
        features['length'] = len(url)
        features['has_ip'] = 1 if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url) else 0
        features['num_special_chars'] = len(re.findall(r'[@\-?=&]', url))
        features['has_https'] = 1 if url.startswith("https://") else 0
        
        # Extended heuristics for explanation
        features['is_shortened'] = 1 if re.search(r'bit\.ly|tinyurl|t\.co', url) else 0
        features['contains_fintech_brand'] = 1 if re.search(r'kyc|hdfc|sbi|icici|yono|paytm|phonepe', url.lower()) else 0
        
        return features

    def analyze(self, url: str) -> URLAgentResult:
        features = self.extract_features(url)
        
        # Simple heuristic fallback if model is unavailable or just for fast checking
        score = 0
        if features['has_ip'] == 1: score += 0.4
        if features['is_shortened'] == 1: score += 0.3
        if features['contains_fintech_brand'] == 1 and features['has_https'] == 0: score += 0.5
        if features['length'] > 75: score += 0.2
        if features['num_special_chars'] > 3: score += 0.2
        
        # Cap confidence at 0.99
        confidence = min(0.99, score)
        
        return URLAgentResult(
            is_phishing=confidence > 0.5,
            confidence=confidence,
            features=features
        )
