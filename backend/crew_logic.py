import os
import re
import json
import joblib
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

# Load Models
url_model = None
if os.path.exists("models/url_model.pkl"):
    url_model = joblib.load("models/url_model.pkl")

# We defer importing transformers until needed to speed up fastAPI boot if possible, or just import here:
try:
    from transformers import pipeline
    sms_model = pipeline("text-classification", model="models/sms_model", return_all_scores=True)
except Exception:
    sms_model = None

# Set up LLM
llm_provider = os.getenv("LLM_PROVIDER", "groq").lower()
if llm_provider == "groq" and os.getenv("GROQ_API_KEY"):
    llm = ChatGroq(temperature=0, model_name="llama3-8b-8192")
elif os.getenv("OPENAI_API_KEY"):
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
else:
    # default fallback just in case no API key config (will crash if called without key)
    llm = None

# --- TOOLS ---
@tool("Scikit-Learn URL Analyzer")
def analyze_url_tool(url: str) -> str:
    """Extracts features from a URL and runs it through a Random Forest Classifier to output a phishing probability."""
    features = {
        'length': len(url),
        'has_ip': 1 if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url) else 0,
        'num_special_chars': len(re.findall(r'[@\-?=&]', url)),
        'has_https': 1 if url.startswith("https://") else 0,
        'is_shortened': 1 if re.search(r'bit\.ly|tinyurl|t\.co', url) else 0,
        'contains_fintech_brand': 1 if re.search(r'kyc|hdfc|sbi|icici|yono|paytm|phonepe', url.lower()) else 0
    }
    
    # ML check
    confidence = 0.0
    if url_model:
        X = [[
            features['length'], features['has_ip'], features['num_special_chars'],
            features['has_https'], features['is_shortened'], features['contains_fintech_brand']
        ]]
        confidence = float(url_model.predict_proba(X)[0][1])
    else:
        # Heuristics
        score = 0
        if features['has_ip']: score += 0.4
        if features['is_shortened']: score += 0.3
        if features['contains_fintech_brand'] and not features['has_https']: score += 0.5
        if features['length'] > 75: score += 0.2
        confidence = min(0.99, score)
        
    return json.dumps({"confidence": confidence, "features": features})

@tool("Transformers SMS Analyzer")
def analyze_sms_tool(text: str) -> str:
    """Runs SMS text through a HuggingFace Transformer model to output a smishing probability and extracts keywords."""
    fintech_keywords = [
        "kyc", "blocked", "suspend", "update pan", "dear customer", "otp", 
        "yono", "sbi", "hdfc", "login", "claim", "reward", "urgent"
    ]
    detected_keywords = [kw for kw in fintech_keywords if kw in text.lower()]
    
    confidence = 0.0
    if sms_model:
        # returns [[{'label': 'LABEL_0', 'score': 0.1}, {'label': 'LABEL_1', 'score': 0.9}]]
        res = sms_model(text[:512])[0]
        for pred in res:
            if pred['label'] == 'LABEL_1':
                confidence = pred['score']
    else:
        # Heuristics
        score = len(detected_keywords) * 0.25
        if re.search(r'http[s]?://|bit\.ly', text.lower()):
            score += 0.4
        confidence = min(0.99, score)
        
    return json.dumps({"confidence": confidence, "detected_keywords": detected_keywords})

@tool("Threat Intelligence Lookup")
def threat_intel_tool(url: str) -> str:
    """Performs simulated WHOIS / Blacklist lookup for a domain."""
    import random
    # Simulated response
    risk_score = 0.0
    flags = []
    
    if "bit.ly" in url or "tinyurl" in url:
        risk_score += 0.6
        flags.append("URL Shortener used (hides intent)")
        
    if "http://" in url:
        risk_score += 0.3
        flags.append("Unsecured HTTP connection")
        
    if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url):
        risk_score += 0.8
        flags.append("Direct IP address used instead of domain name")
        
    return json.dumps({"risk_score": min(0.99, risk_score), "threat_flags": flags})

# --- AGENTS ---
class AnalyzerCrew:
    def __init__(self):
        self.url_agent = Agent(
            role='URL Security Analyst',
            goal='Analyze URLs for phishing patterns using ML models and heuristics.',
            backstory='You are a cybersecurity expert specializing in lexical analysis and domain reputability.',
            tools=[analyze_url_tool],
            llm=llm,
            verbose=True
        )

        self.sms_agent = Agent(
            role='Smishing Detection Analyst',
            goal='Analyze text messages for social engineering, urgency, and smishing traits using NLP.',
            backstory='You are a veteran social engineering counter-intelligence officer.',
            tools=[analyze_sms_tool],
            llm=llm,
            verbose=True
        )

        self.threat_agent = Agent(
            role='Threat Intelligence Analyst',
            goal='Perform domain and infrastructure lookups to determine domain age and blacklist status.',
            backstory='You are an OSINT specialist with access to global threat databases.',
            tools=[threat_intel_tool],
            llm=llm,
            verbose=True
        )

        self.explainability_agent = Agent(
            role='Cybersecurity Explainability Expert',
            goal='Synthesize raw ML agent scores and features into a single human-readable explanation and final weighted fused score.',
            backstory='You are the interface between complex AI models and human users. You explain exactly WHY a text or URL is dangerous in plain English.',
            llm=llm,
            verbose=True
        )

    def run_full_scan(self, url: str, sms: str):
        task1 = Task(
            description=f'Analyze the URL: {url}. Extract probability and features.',
            expected_output='A JSON string containing the exact float probability and extracted features.',
            agent=self.url_agent
        )
        task2 = Task(
            description=f'Analyze the SMS: "{sms}". Extract probability and keywords.',
            expected_output='A JSON string containing the exact float probability and detected keywords.',
            agent=self.sms_agent
        )
        task3 = Task(
            description=f'Perform threat lookup on the URL: {url}.',
            expected_output='A JSON string containing the exact float risk score and threat flags.',
            agent=self.threat_agent
        )
        task4 = Task(
            description='''
            Synthesize the results from the URL, SMS, and Threat tasks.
            1. Apply the fusion scoring logic: URL Confidence * 0.40 + SMS Confidence * 0.30 + Threat Score * 0.20. 
               Base the final 10% on your own Explainability Agent assessment (how manipulative does the SMS+URL combo look? 0.0 to 1.0).
               Calculate the Final Confidence (0.0 to 1.0).
            2. Determine the verdict: Final Confidence < 0.3 (Safe), 0.3 to 0.7 (Suspicious), > 0.7 (Malicious).
            3. Write a clear, concise human-readable explanation (1-2 sentences) of exactly WHY this is safe/suspicious/malicious.
            
            Return output strictly as valid JSON with keys: "verdict" (string), "confidence" (float 0.0 - 1.0), "explanation" (string).
            ''',
            expected_output='Strict JSON string with "verdict", "confidence" (float), and "explanation".',
            agent=self.explainability_agent
        )

        crew = Crew(
            agents=[self.url_agent, self.sms_agent, self.threat_agent, self.explainability_agent],
            tasks=[task1, task2, task3, task4],
            process=Process.sequential
        )
        
        result = crew.kickoff()
        return result
        
    def run_url_scan(self, url: str):
        task1 = Task(
            description=f'Analyze the URL: {url}. Extract probability and features.',
            expected_output='A JSON string containing the exact float probability and extracted features.',
            agent=self.url_agent
        )
        task2 = Task(
            description=f'Perform threat lookup on the URL: {url}.',
            expected_output='A JSON string containing the exact float risk score and threat flags.',
            agent=self.threat_agent
        )
        task3 = Task(
            description='''
            Synthesize the results from the URL and Threat tasks.
            1. Apply fusion logic: (URL Confidence * 0.60) + (Threat Score * 0.30) + (Own Explainability Assessment 0.10).
            2. Determine verdict based on Final Confidence.
            3. Write a clear, concise human-readable explanation.
            
            Return output strictly as valid JSON with keys: "verdict", "confidence" (float 0.0 - 1.0), "explanation".
            ''',
            expected_output='Strict JSON string with "verdict", "confidence" (float), and "explanation".',
            agent=self.explainability_agent
        )
        
        crew = Crew(
            agents=[self.url_agent, self.threat_agent, self.explainability_agent],
            tasks=[task1, task2, task3],
            process=Process.sequential
        )
        return crew.kickoff()

    def run_sms_scan(self, sms: str):
        task1 = Task(
            description=f'Analyze the SMS: "{sms}". Extract probability and keywords.',
            expected_output='A JSON string containing the exact float probability and detected keywords.',
            agent=self.sms_agent
        )
        task2 = Task(
            description='''
            Synthesize the results from the SMS task.
            1. Apply logic: (SMS Confidence * 0.85) + (Own Assessment 0.15).
            2. Determine verdict based on Final Confidence.
            3. Write a clear, concise human-readable explanation.
            
            Return output strictly as valid JSON with keys: "verdict", "confidence" (float 0.0 - 1.0), "explanation".
            ''',
            expected_output='Strict JSON string with "verdict", "confidence" (float), and "explanation".',
            agent=self.explainability_agent
        )
        
        crew = Crew(
            agents=[self.sms_agent, self.explainability_agent],
            tasks=[task1, task2],
            process=Process.sequential
        )
        return crew.kickoff()
