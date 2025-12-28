from flask import Flask, request, jsonify, render_template_string
import os
import openai

# Flask app
app = Flask(__name__)

# OpenAI Key from Vercel Environment Variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# ---------- HOME PAGE ----------
@app.route("/")
def home():
    return render_template_string("""
    <html>
    <head>
        <title>FutureGuard AI</title>
        <style>
            body {
                background:#0f172a;
                color:white;
                font-family:Arial;
                text-align:center;
                padding-top:80px;
            }
            button {
                padding:12px 20px;
                background:#22c55e;
                border:none;
                border-radius:6px;
                font-size:16px;
                cursor:pointer;
            }
        </style>
    </head>
    <body>
        <h1>🚀 FutureGuard AI</h1>
        <p>Predict Risks • Get Warnings • Take Action</p>
        <button onclick="alert('API Ready. Use /analyze endpoint')">
            System Ready
        </button>
    </body>
    </html>
    """)

# ---------- HEALTH CHECK ----------
@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "system": "FutureGuard AI",
        "engine": "running"
    })

# ---------- CORE AI ENDPOINT ----------
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json

    if not data or "problem" not in data:
        return jsonify({"error": "Problem description required"}), 400

    problem = data["problem"]

    prompt = f"""
You are a senior AI business doctor.

Company Problem:
{problem}

Your task:
1. Identify future risks
2. Predict what can go wrong soon
3. Give clear warning signals
4. Provide step-by-step actions to fix it

Answer in simple, professional language.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are FutureGuard AI."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        result = response.choices[0].message.content

        return jsonify({
            "input_problem": problem,
            "future_analysis": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)
