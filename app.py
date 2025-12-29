from flask import Flask, request, jsonify, render_template
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are FutureGuard AI, a multilingual enterprise risk and decision assistant.

Your responsibilities:
1. Detect the user's language automatically and reply in the same language.
2. Detect business size (small business / startup / enterprise).
3. Analyze the business problem deeply.
4. Give structured output:

RISK LEVEL: LOW / MEDIUM / HIGH

KEY ISSUES:
- Bullet points

WARNINGS:
- Predict near-future risks if no action is taken

RECOMMENDED ACTIONS:
- Clear, practical actions

DECISION PRIORITY:
- Immediate / Short-term / Long-term

Rules:
- Never say you are an AI model.
- Be confident, professional, and practical.
"""

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        problem = request.form.get("problem")

        if not problem:
            return jsonify({"error": "No input provided"})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": problem}
            ],
            temperature=0.4
        )

        result = response.choices[0].message.content
        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
