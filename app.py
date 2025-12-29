from flask import Flask, request, jsonify, render_template, send_file
import openai
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """
You are FutureGuard AI, a professional enterprise risk intelligence system.

Your responsibilities:
- Analyze business problems clearly
- Predict risks
- Provide warnings
- Suggest actionable solutions

Output format:

RISK LEVEL: HIGH / MEDIUM / LOW

KEY ISSUES:
- Bullet points

WARNINGS:
- Predict near-future risks

RECOMMENDED ACTIONS:
- Clear, practical actions

Be confident, professional, and concise.
Never say you are an AI model.
"""

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    problem = request.form.get("problem")

    if not problem:
        return jsonify({"error": "No problem provided"})

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


@app.route("/download-pdf", methods=["POST"])
def download_pdf():
    problem = request.form.get("problem")
    result = request.form.get("result")

    filename = "FutureGuard_AI_Report.pdf"
    path = f"/tmp/{filename}"

    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "FutureGuard AI – Risk Analysis Report")

    y -= 30
    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Generated on: {datetime.now().strftime('%d %b %Y')}")

    y -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Business Problem:")

    y -= 20
    c.setFont("Helvetica", 11)
    c.drawString(50, y, problem)

    y -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "AI Analysis:")

    y -= 20
    c.setFont("Helvetica", 11)

    for line in result.split("\n"):
        c.drawString(50, y, line)
        y -= 15
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()

    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
