from typing import Dict, Any

class ExplainabilityAgent:
    def __init__(self):
        pass
        
    def generate_explanation(self, url_res: Dict[str, Any] = None, sms_res: Dict[str, Any] = None, threat_res: Dict[str, Any] = None) -> list[str]:
        explanations = []
        
        if url_res:
            features = url_res.get('features', {})
            if features.get('has_ip'):
                explanations.append("URL uses an IP address instead of a domain name (common in phishing).")
            if features.get('is_shortened'):
                explanations.append("URL uses a link shortener service to obscure the destination.")
            if features.get('contains_fintech_brand') and not features.get('has_https'):
                explanations.append("URL targets a FinTech brand but does not use HTTPS.")
            if features.get('num_special_chars', 0) > 3:
                explanations.append(f"URL contains suspicious number of special characters ({features['num_special_chars']}).")
                
        if sms_res:
            keywords = sms_res.get('detected_keywords', [])
            if keywords:
                explanations.append(f"SMS contains urgency or financial trigger words: {', '.join(keywords)}.")
                
        if threat_res:
            if threat_res.get('is_blacklisted'):
                explanations.append("The domain matches records in known phishing threat intelligence databases.")
            if threat_res.get('domain_age_days', 365) < 30:
                explanations.append(f"The domain was registered recently ({threat_res['domain_age_days']} days ago).")
                
        if not explanations:
            explanations.append("No distinctly malicious patterns were extracted.")
            
        return explanations
