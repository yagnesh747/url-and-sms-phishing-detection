import joblib
import os
import re
from pydantic import BaseModel

class SmishingAgentResult(BaseModel):
    is_smishing: bool
    confidence: float
    detected_keywords: list[str]

class SmishingDetectionAgent:
    def __init__(self):
        self.model_path = "models/smishing_model.pkl"
        self.model = None
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            
        self.fintech_keywords = [
            "kyc", "blocked", "suspend", "update pan", "dear customer", "otp", 
            "yono", "sbi", "hdfc", "login", "claim", "reward", "urgent"
        ]

    def analyze(self, text: str) -> SmishingAgentResult:
        text_lower = text.lower()
        detected_keywords = [kw for kw in self.fintech_keywords if kw in text_lower]
        
        # Priority to ML model if it exists
        if self.model:
            # Random forest pipeline returns string '1' or int 1 for smishing in our training script
            try:
                pred = self.model.predict([text])[0]
                proba = self.model.predict_proba([text])[0]
                
                # proba[1] corresponds to probability of class 1 (smishing)
                confidence = float(proba[1]) if len(proba) > 1 else float(pred)
                return SmishingAgentResult(
                    is_smishing=confidence > 0.5,
                    confidence=confidence,
                    detected_keywords=detected_keywords
                )
            except Exception as e:
                pass # fallback to heuristics
                
        # Heuristic rules
        score = min(len(detected_keywords) * 0.25, 0.99)
        if re.search(r'http[s]?://|bit\.ly', text_lower):
            score += 0.4
            
        confidence = min(0.99, score)
        
        return SmishingAgentResult(
            is_smishing=confidence > 0.5,
            confidence=confidence,
            detected_keywords=detected_keywords
        )
