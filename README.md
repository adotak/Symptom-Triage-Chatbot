# MediGuide 🩺

An AI-powered symptom triage chatbot designed for patients in Pakistan, particularly in underserved and rural areas with limited access to healthcare.

## What it does
MediGuide takes your symptoms as input and classifies the urgency into one of three categories:
- 🔴 **EMERGENCY** – Go to the nearest hospital immediately
- 🟡 **SEE A DOCTOR** – Visit a clinic or GP within 24–48 hours
- 🟢 **HOME CARE** – Rest and basic remedies should help

Supports both **English and Urdu**.

## Tech Stack
- Python
- Google Antigravity SDK
- Gemini 3.0

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/adotak/Symptom-Triage-Chatbot.git
cd Symptom-Triage-Chatbot
```

### 2. Install dependencies
```bash
pip install google-antigravity python-dotenv
```

### 3. Add your API key
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_gemini_api_key_here
```
Get your free API key from [Google AI Studio](https://aistudio.google.com).

### 4. Run
```bash
# Terminal version
python triage.py

# Or start the Web Interface (with Voice support!)
python triage_web.py
```

## Usage
Just type your symptoms in English or Urdu and MediGuide will assess the urgency and guide you on what to do next.

```
You: I have chest pain and difficulty breathing since this morning

MediGuide: 🔴 EMERGENCY – Please go to the nearest hospital immediately...
```

## Disclaimer
This is not a substitute for professional medical advice. Always consult a real doctor for medical decisions.

## Author
Ahmad – CS Sophomore @ UET Peshawar

## Features
- Bilingual support (English & Urdu)
- 3-tier urgency classification
- Designed for low-resource healthcare settings in Pakistan
- Lightweight — runs entirely in terminal

## Future Plans
- Web/mobile interface
- Voice input support
- Integration with nearby clinic locator
- Expand to more Pakistani regional languages (Pashto, Sindhi)

## Contributing
Pull requests are welcome. For major changes, please open an issue first.

## License
MIT