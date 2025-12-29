from flask import Flask, request, jsonify, render_template
import os
import openai

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """
You are FutureGuard AI, an enterprise-grade Business Risk & Decision Intelligence System.

Your responsibilities:
1. Detect the user's language automatically and reply in the SAME language.
2. Detect business size automatically (Small Business, Startup, or Large Enterprise).
3. Analyze the business problem deeply.
4. Output in the following structured format:

RISK LEVEL: LOW / MEDIUM / HIGH (with emoji)

KEY ISSUES:
- Bullet points

WARNINGS:
⚠️ Predict near-future risks if no action is taken.

RECOMMENDED ACTIONS:
1. Clear, practical actions.

DECISION PRIORITY:
🔥 Immediate / ⏳ Short-term / 📅 Long-term

Tone rules:
- Small business → simple & practical
- Startup → growth, runway, scalability
- Enterprise → executive, strategic, governance-level

Never say you are an AI model.
Never ask unnecessary questions.
Be confident, clear, and professional.
"""

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        problem = request.form.get("problem")
        if not problem:
            return jsonify({"error": "No input provided"}), 400

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": problem}
            ],
            temperature=0.4
        )

        result = response["choices"][0]["message"]["content"]
        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()
