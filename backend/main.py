import json
import logging
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from database import init_db, get_db
from crew_logic import AnalyzerCrew

app = FastAPI(title="Phishing & Smishing Detection Framework")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

crew = AnalyzerCrew()

# Basic in-memory cache for repeated queries
response_cache = {}

@app.on_event("startup")
async def startup_event():
    await init_db()

class URLRequest(BaseModel):
    url: str

class SMSRequest(BaseModel):
    sms: str

class FullScanRequest(BaseModel):
    url: str
    sms: str

def parse_crew_result(crew_output):
    """CrewAI returns a CrewOutput object with raw string. We want json."""
    try:
        raw_str = crew_output.raw.strip()
        # Clean markdown code blocks if present
        if raw_str.startswith("```json"):
            raw_str = raw_str[7:-3]
        elif raw_str.startswith("```"):
            raw_str = raw_str[3:-3]
            
        result = json.loads(raw_str)
        return {
            "verdict": result.get("verdict", "Unknown"),
            "confidence": result.get("confidence", 0.0) * 100, # convert to 0-100%
            "explanation": result.get("explanation", "No explanation provided.")
        }
    except Exception as e:
        logging.error(f"Failed to parse CrewAI output: {e} | Raw: {crew_output.raw}")
        return {
            "verdict": "Error processing result",
            "confidence": 0.0,
            "explanation": f"Failed to parse AI output: {str(e)}"
        }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/analyze-url")
async def analyze_url(payload: URLRequest, db = Depends(get_db)):
    cache_key = f"url_{payload.url}"
    if cache_key in response_cache:
        return response_cache[cache_key]

    raw_result = crew.run_url_scan(payload.url)
    parsed = parse_crew_result(raw_result)
    
    response = {
        "status": parsed["verdict"],
        "confidence": parsed["confidence"],
        "explanation": parsed["explanation"],
        "details": {"input": payload.url}
    }
    
    response_cache[cache_key] = response
    
    # Save to MongoDB
    await db.scan_history.insert_one({
        "scan_type": "url",
        "input_content": payload.url,
        "status": parsed["verdict"],
        "confidence": parsed["confidence"],
        "explanations": parsed["explanation"],
        "timestamp": datetime.utcnow()
    })
    
    return response

@app.post("/analyze-sms")
async def analyze_sms(payload: SMSRequest, db = Depends(get_db)):
    cache_key = f"sms_{payload.sms}"
    if cache_key in response_cache:
        return response_cache[cache_key]

    raw_result = crew.run_sms_scan(payload.sms)
    parsed = parse_crew_result(raw_result)
    
    response = {
        "status": parsed["verdict"],
        "confidence": parsed["confidence"],
        "explanation": parsed["explanation"],
        "details": {"input": payload.sms}
    }
    
    response_cache[cache_key] = response
    
    await db.scan_history.insert_one({
        "scan_type": "sms",
        "input_content": payload.sms,
        "status": parsed["verdict"],
        "confidence": parsed["confidence"],
        "explanations": parsed["explanation"],
        "timestamp": datetime.utcnow()
    })

    return response

@app.post("/full-scan")
async def full_scan(payload: FullScanRequest, db = Depends(get_db)):
    cache_key = f"full_{payload.url}_{payload.sms}"
    if cache_key in response_cache:
        return response_cache[cache_key]

    raw_result = crew.run_full_scan(payload.url, payload.sms)
    parsed = parse_crew_result(raw_result)
    
    response = {
        "status": parsed["verdict"],
        "confidence": parsed["confidence"],
        "explanation": parsed["explanation"],
        "details": {"url": payload.url, "sms": payload.sms}
    }
    
    response_cache[cache_key] = response
    
    await db.scan_history.insert_one({
        "scan_type": "full",
        "input_content": f"URL: {payload.url} | SMS: {payload.sms}",
        "status": parsed["verdict"],
        "confidence": parsed["confidence"],
        "explanations": parsed["explanation"],
        "timestamp": datetime.utcnow()
    })

    return response

@app.get("/history")
async def get_history(limit: int = 50, db = Depends(get_db)):
    cursor = db.scan_history.find().sort("timestamp", -1).limit(limit)
    records = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        # Format timestamp for JSON serialization
        if "timestamp" in doc and hasattr(doc["timestamp"], "isoformat"):
             doc["timestamp"] = doc["timestamp"].isoformat()
        records.append(doc)
    return records

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
