# AI-Driven Multi-Agent Phishing & Smishing Detection Framework

This is a production-ready, multi-agent cybersecurity platform designed to detect phishing URLs and smishing (fraud SMS) messages in real-time, optimized for FinTech ecosystems.

## Architecture

The system uses an autonomous Multi-Agent architecture:
- **URL Analysis Agent**: Extracts lexical, host-based, and ML-inferred features from URLs.
- **Smishing Detection Agent**: Analyzes text for urgency, FinTech keywords, and invokes an NLP classifier.
- **Threat Intelligence Agent**: Simulates external lookups (WHOIS, domain age, blacklists).
- **Decision Fusion Agent**: Aggregates scores and outputs a final verdict (Safe/Suspicious/Malicious).
- **Explainability Agent**: Generates human-readable context for why a threat was flagged.

## Folder Structure
- `/backend`: FastAPI Python application with the agent code and ML scripts.
- `/frontend`: Vite + React modern dashboard with Tailwind CSS.
- `/docker-compose.yml`: Root orchestrator for deployment.

## Prerequisites
- Docker and Docker Compose installed.
- (Alternatively) Python 3.10+ and Node.js 18+ for local running.

## Running the Application

### Method 1: Docker Compose (Recommended)
1. Open a terminal in the root directory.
2. Run: `docker-compose up --build -d`
3. Access the dashboard at `http://localhost:3000`.
4. Backend API runs on `http://localhost:8000`.

### Method 2: Local Development
**Backend:**
```bash
cd backend
pip install -r requirements.txt
python train/train_models.py # Generates dummy models
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Sample Test Inputs

#### URL Agent Inputs
- **Malicious/Phishing:** `http://update-kyc-hdfc-secure.com/login` (Flags: IP/Unknown domain + KYC keywords + No HTTPS + Domain Age)
- **Suspicious:** `http://bit.ly/1234` (Flags: Shortener + No direct malicious branding)
- **Safe:** `https://google.com`

#### Smishing Agent Inputs
- **Malicious:** `URGENT: Your SBI YONO account is suspended. Update PAN via http://bit.ly/kyc-update immediately.`
- **Safe:** `Hey John, let's grab coffee at 5 PM.`

#### Full Scan Inputs
Combine a malicious SMS and a malicious URL to see the Decision Fusion agent increase the confidence metrics and print detailed explainability traits.

---
Built as an enterprise-grade conceptual cybersecurity implementation.
