from flask import Flask, render_template, request, jsonify, send_file
import os
from supabase import create_client
import openai
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import datetime

app = Flask(__name__)

# =========================
# ENV VARIABLES
# =========================
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

# =========================
# SYSTEM PROMPT
# =========================
SYSTEM_PROMPT = """
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

# =========================
# ROUTES
# =========================

@app.route("/")
def home():
    return render_template("index.html")

# ---------- AUTH ----------
@app.route("/auth", methods=["POST"])
def auth():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    action = data.get("action")

    if not email or not password:
        return jsonify({"error": "Email & password required"}), 400

    try:
        if action == "signup":
            supabase.auth.admin.create_user({
                "email": email,
                "password": password,
                "email_confirm": True
            })
            return jsonify({"success": True, "message": "User created"})

        if action == "login":
            res = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return jsonify(res)

        return jsonify({"error": "Invalid action"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------- AI ANALYSIS ----------
@app.route("/analyze", methods=["POST"])
def analyze():
    problem = request.form.get("problem")

    if not problem:
        return jsonify({"error": "No problem provided"}), 400

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

# ---------- PDF DOWNLOAD ----------
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
    c.drawString(50, y, "FutureGuard AI - Risk Analysis Report")
    y -= 30

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Generated on: {datetime.datetime.now()}")
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

# =========================
if __name__ == "__main__":
    app.run(debug=True)
