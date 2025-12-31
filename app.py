from flask import Flask, request, jsonify, render_template, send_file
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
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# =========================
# SYSTEM PROMPT
# =========================
SYSTEM_PROMPT = """
You are FutureGuard AI.

Your responsibilities:
- Analyze business problems clearly
- Predict risks
- Provide warnings
- Suggest practical solutions

Output format:

RISK LEVEL: HIGH / MEDIUM / LOW

KEY ISSUES:
- Bullet points

WARNINGS:
- Near-future risks

RECOMMENDED ACTIONS:
- Clear steps

Be professional and concise.
"""

# =========================
# ROUTES
# =========================

@app.route("/")
def home():
    return "Backend is running successfully 🚀"

# =========================
# AUTH (SIGNUP / LOGIN)
# =========================
@app.route("/auth", methods=["POST"])
def auth():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    action = data.get("action")  # signup | login

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    try:
        if action == "signup":
            res = supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            return jsonify({"success": True, "message": "User created"})

        if action == "login":
            res = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return jsonify({
                "success": True,
                "user": res.user.email,
                "access_token": res.session.access_token
            })

        return jsonify({"error": "Invalid action"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =========================
# AI ANALYSIS
# =========================
@app.route("/analyze", methods=["POST"])
def analyze():
    problem = request.json.get("problem")

    if not problem:
        return jsonify({"error": "Problem required"}), 400

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

# =========================
# PDF DOWNLOAD
# =========================
@app.route("/download-pdf", methods=["POST"])
def download_pdf():
    problem = request.json.get("problem")
    result = request.json.get("result")

    filename = "FutureGuard_AI_Report.pdf"
    path = f"/tmp/{filename}"

    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "FutureGuard AI Risk Analysis Report")
    y -= 30

    c.setFont("Helvetica", 10)
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
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)
