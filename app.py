import os
from flask import Flask, request, jsonify, render_template
from openai import OpenAI

# -----------------------
# App Init
# -----------------------
app = Flask(__name__)

# -----------------------
# OpenAI Client
# -----------------------
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# -----------------------
# Home Page (UI)
# -----------------------
@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>FutureGuard AI</title>
        <style>
            body {
                font-family: Arial;
                background: #0f172a;
                color: white;
                text-align: center;
                padding: 50px;
            }
            textarea {
                width: 80%;
                height: 120px;
                border-radius: 8px;
                padding: 10px;
            }
            button {
                margin-top: 20px;
                padding: 12px 30px;
                background: #22c55e;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
            }
            pre {
                text-align: left;
                background: #020617;
                padding: 20px;
                border-radius: 8px;
                margin-top: 30px;
                white-space: pre-wrap;
            }
        </style>
    </head>
    <body>
        <h1>🚀 FutureGuard AI</h1>
        <p>Enterprise Risk & Decision Intelligence</p>

        <textarea id="input" placeholder="Enter business situation / risk / problem..."></textarea><br>
        <button onclick="analyze()">Analyze</button>

        <pre id="result"></pre>

        <script>
            async function analyze() {
                const text = document.getElementById("input").value;
                const res = await fetch("/analyze", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({input: text})
                });
                const data = await res.json();
                document.getElementById("result").innerText = data.result;
            }
        </script>
    </body>
    </html>
    """

# -----------------------
# AI Brain Endpoint
# -----------------------
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    user_input = data.get("input", "")

    if not user_input:
        return jsonify({"error": "No input provided"})

    prompt = f"""
You are FutureGuard AI, an enterprise-grade AI system.

TASK:
1. Identify business risks
2. Predict future impact
3. Give clear warnings
4. Suggest actionable steps

INPUT:
{user_input}

OUTPUT FORMAT:
- Risk Level:
- Key Threats:
- Future Prediction:
- Recommended Actions:
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a high-level enterprise AI strategist."},
                {"role": "user", "content": prompt}
            ]
        )

        result = response.choices[0].message.content

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)})

# -----------------------
# Run Local
# -----------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
