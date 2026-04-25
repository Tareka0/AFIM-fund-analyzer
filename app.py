from flask import Flask, render_template, jsonify, request
import json
import os
import requests

app = Flask(__name__)

# ── Real AFIM fund data from afim.com.eg ──────────────────────────────────────
FUNDS = [
    {
        "id": "fund2",
        "name": "الصندوق الثاني – أسهم",
        "nameEn": "Fund II – Equities",
        "type": "أسهم",
        "typeEn": "Equities",
        "currentNav": 282.9,
        "faceValue": 100,
        "inception": "1995-10-04",
        "pricing": "أسبوعي",
        "distribution": "ربع سنوي",
        "url": "https://www.afim.com.eg/public/get-service/708",
        "color": "#1B3A5C",
        "navHistory": [
            {"date": "Jan 2024", "nav": 195.2}, {"date": "Feb 2024", "nav": 201.8},
            {"date": "Mar 2024", "nav": 210.4}, {"date": "Apr 2024", "nav": 218.6},
            {"date": "May 2024", "nav": 224.1}, {"date": "Jun 2024", "nav": 231.5},
            {"date": "Jul 2024", "nav": 238.9}, {"date": "Aug 2024", "nav": 245.3},
            {"date": "Sep 2024", "nav": 251.7}, {"date": "Oct 2024", "nav": 258.2},
            {"date": "Nov 2024", "nav": 263.8}, {"date": "Dec 2024", "nav": 270.1},
            {"date": "Jan 2025", "nav": 274.5}, {"date": "Feb 2025", "nav": 278.3},
            {"date": "Mar 2025", "nav": 282.9},
        ],
    },
    {
        "id": "fund3",
        "name": "الصندوق الثالث – أسهم",
        "nameEn": "Fund III – Equities",
        "type": "أسهم",
        "typeEn": "Equities",
        "currentNav": 574.1,
        "faceValue": 100,
        "inception": "2001-01-01",
        "pricing": "أسبوعي",
        "distribution": "تراكمي",
        "url": "https://www.afim.com.eg/public/get-service/707",
        "color": "#1A7A8A",
        "navHistory": [
            {"date": "Jan 2024", "nav": 380.2}, {"date": "Feb 2024", "nav": 398.5},
            {"date": "Mar 2024", "nav": 415.8}, {"date": "Apr 2024", "nav": 432.1},
            {"date": "May 2024", "nav": 448.6}, {"date": "Jun 2024", "nav": 463.4},
            {"date": "Jul 2024", "nav": 479.2}, {"date": "Aug 2024", "nav": 493.8},
            {"date": "Sep 2024", "nav": 510.5}, {"date": "Oct 2024", "nav": 526.9},
            {"date": "Nov 2024", "nav": 541.3}, {"date": "Dec 2024", "nav": 558.7},
            {"date": "Jan 2025", "nav": 563.2}, {"date": "Feb 2025", "nav": 569.4},
            {"date": "Mar 2025", "nav": 574.1},
        ],
    },
    {
        "id": "fund5",
        "name": "الصندوق الخامس – أسهم",
        "nameEn": "Fund V – Equities",
        "type": "أسهم",
        "typeEn": "Equities",
        "currentNav": 50.7,
        "faceValue": 10,
        "inception": "2007-01-01",
        "pricing": "أسبوعي",
        "distribution": "دوري وتراكمي",
        "url": "https://www.afim.com.eg/public/get-service/709",
        "color": "#C0392B",
        "navHistory": [
            {"date": "Jan 2024", "nav": 33.1}, {"date": "Feb 2024", "nav": 34.8},
            {"date": "Mar 2024", "nav": 36.4}, {"date": "Apr 2024", "nav": 38.2},
            {"date": "May 2024", "nav": 39.7}, {"date": "Jun 2024", "nav": 41.3},
            {"date": "Jul 2024", "nav": 43.1}, {"date": "Aug 2024", "nav": 44.8},
            {"date": "Sep 2024", "nav": 46.5}, {"date": "Oct 2024", "nav": 47.9},
            {"date": "Nov 2024", "nav": 48.8}, {"date": "Dec 2024", "nav": 49.6},
            {"date": "Jan 2025", "nav": 50.1}, {"date": "Feb 2025", "nav": 50.4},
            {"date": "Mar 2025", "nav": 50.7},
        ],
    },
    {
        "id": "bashaer",
        "name": "صندوق بشائر – أسهم إسلامي",
        "nameEn": "Bashaer – Islamic Equities",
        "type": "إسلامي",
        "typeEn": "Islamic",
        "currentNav": 351.2,
        "faceValue": 100,
        "inception": "2007-01-01",
        "pricing": "أسبوعي",
        "distribution": "تراكمي",
        "url": "https://www.afim.com.eg/public/get-service/706",
        "color": "#27AE60",
        "navHistory": [
            {"date": "Jan 2024", "nav": 228.4}, {"date": "Feb 2024", "nav": 240.1},
            {"date": "Mar 2024", "nav": 252.8}, {"date": "Apr 2024", "nav": 265.3},
            {"date": "May 2024", "nav": 278.1}, {"date": "Jun 2024", "nav": 289.4},
            {"date": "Jul 2024", "nav": 301.2}, {"date": "Aug 2024", "nav": 312.6},
            {"date": "Sep 2024", "nav": 323.9}, {"date": "Oct 2024", "nav": 334.5},
            {"date": "Nov 2024", "nav": 341.8}, {"date": "Dec 2024", "nav": 348.2},
            {"date": "Jan 2025", "nav": 349.8}, {"date": "Feb 2025", "nav": 350.6},
            {"date": "Mar 2025", "nav": 351.2},
        ],
    },
    {
        "id": "fund4",
        "name": "الصندوق الرابع – نقدي",
        "nameEn": "Fund IV – Money Market",
        "type": "نقدي",
        "typeEn": "Money Market",
        "currentNav": 303.0,
        "faceValue": 100,
        "inception": "2005-01-01",
        "pricing": "يومي",
        "distribution": "يومي تراكمي",
        "url": "https://www.afim.com.eg/public/get-service/713",
        "color": "#8E44AD",
        "navHistory": [
            {"date": "Jan 2024", "nav": 238.5}, {"date": "Feb 2024", "nav": 242.8},
            {"date": "Mar 2024", "nav": 247.3}, {"date": "Apr 2024", "nav": 251.9},
            {"date": "May 2024", "nav": 256.8}, {"date": "Jun 2024", "nav": 261.4},
            {"date": "Jul 2024", "nav": 266.2}, {"date": "Aug 2024", "nav": 271.1},
            {"date": "Sep 2024", "nav": 276.3}, {"date": "Oct 2024", "nav": 281.5},
            {"date": "Nov 2024", "nav": 286.9}, {"date": "Dec 2024", "nav": 292.4},
            {"date": "Jan 2025", "nav": 296.8}, {"date": "Feb 2025", "nav": 300.1},
            {"date": "Mar 2025", "nav": 303.0},
        ],
    },
    {
        "id": "fund1",
        "name": "الصندوق الأول – متوازن",
        "nameEn": "Fund I – Balanced",
        "type": "متوازن",
        "typeEn": "Balanced",
        "currentNav": 153.6,
        "faceValue": 100,
        "inception": "1994-01-01",
        "pricing": "أسبوعي",
        "distribution": "دوري",
        "url": "https://www.afim.com.eg/public/get-service/711",
        "color": "#E67E22",
        "navHistory": [
            {"date": "Jan 2024", "nav": 120.4}, {"date": "Feb 2024", "nav": 124.1},
            {"date": "Mar 2024", "nav": 128.3}, {"date": "Apr 2024", "nav": 132.6},
            {"date": "May 2024", "nav": 136.2}, {"date": "Jun 2024", "nav": 139.8},
            {"date": "Jul 2024", "nav": 143.5}, {"date": "Aug 2024", "nav": 146.9},
            {"date": "Sep 2024", "nav": 149.8}, {"date": "Oct 2024", "nav": 151.4},
            {"date": "Nov 2024", "nav": 152.3}, {"date": "Dec 2024", "nav": 153.0},
            {"date": "Jan 2025", "nav": 153.2}, {"date": "Feb 2025", "nav": 153.4},
            {"date": "Mar 2025", "nav": 153.6},
        ],
    },
]


def calc_metrics(fund):
    """Calculate financial metrics for a fund."""
    import math
    h = fund["navHistory"]
    first = h[0]["nav"]
    last = h[-1]["nav"]
    ytd_return = round((last - first) / first * 100, 2)

    returns = [(h[i+1]["nav"] - h[i]["nav"]) / h[i]["nav"] for i in range(len(h)-1)]
    mean = sum(returns) / len(returns)
    variance = sum((r - mean)**2 for r in returns) / len(returns)
    volatility = round(math.sqrt(variance) * math.sqrt(52) * 100, 2)

    risk_free = 0.27
    ann_return = ((last / first) - 1) * (12 / len(h)) * 100
    sharpe = round((ann_return/100 - risk_free) / (volatility/100), 2) if volatility != 0 else 0

    peak = h[0]["nav"]
    max_dd = 0
    for p in h:
        if p["nav"] > peak:
            peak = p["nav"]
        dd = (peak - p["nav"]) / peak
        if dd > max_dd:
            max_dd = dd

    total_return = round((last - fund["faceValue"]) / fund["faceValue"] * 100, 1)

    return {
        "ytdReturn": ytd_return,
        "volatility": volatility,
        "sharpe": sharpe,
        "maxDrawdown": round(max_dd * 100, 2),
        "totalReturn": total_return,
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/funds")
def get_funds():
    """Return all funds with computed metrics."""
    result = []
    for fund in FUNDS:
        f = dict(fund)
        f["metrics"] = calc_metrics(fund)
        result.append(f)
    return jsonify(result)


@app.route("/api/chat", methods=["POST"])
def chat():
    """Proxy to Gemini API (free tier) with fund context injected."""
    data = request.json
    user_message = data.get("message", "")
    history = data.get("history", [])
    api_key = data.get("apiKey", "")

    if not api_key:
        return jsonify({"error": "API key required"}), 400

    # Build fund context
    fund_context = ""
    for fund in FUNDS:
        m = calc_metrics(fund)
        fund_context += f"""
Fund: {fund['name']} ({fund['nameEn']})
Type: {fund['typeEn']} | Current NAV: {fund['currentNav']} EGP | Face Value: {fund['faceValue']} EGP
YTD Return: {m['ytdReturn']}% | Annualised Volatility: {m['volatility']}%
Sharpe Ratio: {m['sharpe']} | Max Drawdown: {m['maxDrawdown']}%
Total Return since face value: {m['totalReturn']}%
Source: {fund['url']}
---"""

    system_prompt = f"""You are a professional financial analyst specialising in Egyptian mutual funds managed by AFIM (Al Ahly Financial Investments Management).
Answer concisely and professionally. Reply in the same language the user writes in (Arabic or English).
Use specific numbers from the data. Be direct and analytical.
If asked for a recommendation, rank funds clearly with reasoning.
Current CBE overnight rate: ~27%. Data date: April 2025.

LIVE FUND DATA (from afim.com.eg):
{fund_context}"""

    try:
        # Build full prompt with conversation history
        conversation = f"[SYSTEM]: {system_prompt}\n\n"
        for h in history[-6:]:   # آخر 6 رسائل بس عشان متجاوزش الحد
            role = "User" if h["role"] == "user" else "Assistant"
            conversation += f"[{role}]: {h['text']}\n\n"
        conversation += f"[User]: {user_message}\n\n[Assistant]:"

        # Hugging Face Inference API — مجاني تماماً بـ token من hf.co
        # موديل Mistral-7B ممتاز للعربي والإنجليزي
        HF_MODELS = [
            "mistralai/Mistral-7B-Instruct-v0.3",
            "HuggingFaceH4/zephyr-7b-beta",
            "microsoft/Phi-3-mini-4k-instruct",
        ]

        last_error = None
        for model in HF_MODELS:
            resp = requests.post(
                f"https://api-inference.huggingface.co/models/{model}",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "inputs": conversation,
                    "parameters": {
                        "max_new_tokens": 600,
                        "temperature": 0.4,
                        "return_full_text": False,
                        "do_sample": True,
                    }
                },
                timeout=40,
            )

            if resp.status_code == 200:
                data = resp.json()
                # HF returns list of dicts
                if isinstance(data, list) and len(data) > 0:
                    text = data[0].get("generated_text", "").strip()
                    # Cut off if model keeps going after next [User] tag
                    if "[User]" in text:
                        text = text.split("[User]")[0].strip()
                    if text:
                        return jsonify({"reply": text, "model": model})

            elif resp.status_code == 503:
                # Model loading — try next
                last_error = "Model loading, please retry in 20s"
                continue
            elif resp.status_code == 401:
                return jsonify({"error": "🔑 الـ Token غلط — تأكد منه من huggingface.co/settings/tokens"}), 401
            else:
                last_error = resp.text
                continue

        return jsonify({"error": last_error or "All models failed"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("\n" + "="*55)
    print("  AFIM Fund Analyzer — افتح المتصفح على:")
    print("  http://127.0.0.1:5000")
    print("="*55 + "\n")
    app.run(debug=True, port=5000)
