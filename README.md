# AFIM Fund Analyzer 📊


## Project Setup in 3 Steps

### 1. Install Dependencies

pip install flask requests

### 2. Run the Server
cd afim_analyzer
python app.py
### 3. Open Browser
[http://127.0.0.1:5000](http://127.0.0.1:5000)
AI Chat — 100% Free (No Credit Card Required)
Go to: https://huggingface.co/settings/tokens

Click "New Token" → Select "Read" type → Copy the Token (starts with hf_)

Paste it into the "HuggingFace Token" field on the AI Analysis page.

Completely free, no banking card needed.

Sources
Fund Data: AFIM Public Investment

AI Model: Google Gemini 1.5 Flash (Free Tier)
Project Structure
```bash
afim_analyzer/
├── app.py              ← Flask backend + metrics calculations
├── requirements.txt    ← Required libraries
└── templates/
    └── index.html      ← Full frontend
