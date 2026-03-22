import requests
import re
from urllib.parse import urlparse
from pydantic import BaseModel
import datetime

class ThreatIntelResult(BaseModel):
    is_blacklisted: bool
    domain_age_days: int
    risk_score: float

class ThreatIntelligenceAgent:
    def __init__(self):
        # In a real scenario, this would integrate with VirusTotal, PhishTank APIs, etc.
        self.mock_blacklist = ['bit.ly', 'update-kyc-hdfc-secure.com', 'tinyurl.com']
        
    def extract_domain(self, url: str) -> str:
        try:
            domain = urlparse(url).netloc
            return domain if domain else url
        except Exception:
            return url
            
    def analyze(self, url: str) -> ThreatIntelResult:
        domain = self.extract_domain(url)
        is_blacklisted = domain in self.mock_blacklist
        
        # Mock domain age (phishing domains often < 30 days)
        # If it has an IP address or 'secure', we lower the mock age
        if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', domain) or "secure" in domain:
            domain_age_days = 5  # High risk
        elif "brand" in domain or "login" in domain:
            domain_age_days = 15
        else:
            domain_age_days = 365 # Low risk default
            
        # Risk scoring
        risk_score = 0.0
        if is_blacklisted:
            risk_score += 0.8
        if domain_age_days < 30:
            risk_score += 0.5
            
        return ThreatIntelResult(
            is_blacklisted=is_blacklisted,
            domain_age_days=domain_age_days,
            risk_score=min(1.0, risk_score)
        )
