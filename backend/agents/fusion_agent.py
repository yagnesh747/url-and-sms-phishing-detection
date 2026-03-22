from pydantic import BaseModel
from typing import Optional

class FusionResult(BaseModel):
    status: str
    confidence: float
    explanations: list[str]

class DecisionFusionAgent:
    def __init__(self):
        pass
        
    def aggregate(self, url_score: float = 0.0, sms_score: float = 0.0, threat_score: float = 0.0, explanations: list[str] = None) -> FusionResult:
        """
        Combines scores. Assumes scores are probabilities or confidences [0, 1].
        """
        # A simple weighted average or maximum based rule engine.
        # Threat intel has highest weight for URLs
        
        scores = []
        if url_score > 0: scores.append(url_score)
        if sms_score > 0: scores.append(sms_score)
        
        # Base confidence is the max of model outputs
        base_confidence = max(scores) if scores else 0.0
        
        # Boost confidence if threat intel agrees it's bad
        final_score = base_confidence
        if threat_score > 0.5:
            final_score = min(0.99, base_confidence + threat_score * 0.5)
            
        if final_score > 0.7:
            status = "Malicious"
        elif final_score > 0.4:
            status = "Suspicious"
        else:
            status = "Safe"
            
        return FusionResult(
            status=status,
            confidence=round(final_score, 2),
            explanations=explanations if explanations else []
        )
