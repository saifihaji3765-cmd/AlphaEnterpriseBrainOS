from flask import Flask, render_template, request, redirect, session, jsonify

app = Flask(__name__)
app.secret_key = "futureguard_login_secret"

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")

        # SIMPLE PAID LOGIC
        # (future me payment ke baad true hoga)
        if email.endswith("@company.com"):
            session["paid"] = True
        else:
            session["paid"] = False

        session["user"] = email
        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ---------------- HOME ----------------
@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")

    return render_template("index.html", paid=session.get("paid", False))


# ---------------- ANALYZE API ----------------
@app.route("/analyze", methods=["POST"])
def analyze():
    if "user" not in session:
        return jsonify({"result": "Please login first."})

    problem = request.form.get("problem", "")
    paid = session.get("paid", False)

    if paid:
        level = "HIGH"
        extra = "- Detailed strategic actions included."
    else:
        level = "MEDIUM"
        extra = "- Upgrade to PRO for detailed insights."

    result = f"""
RISK LEVEL: {level}

KEY ISSUES:
- Cost pressure and efficiency gaps.
- Competitive and operational risks.

WARNINGS:
- Delayed action may increase losses.

RECOMMENDED ACTIONS:
- Immediate cost review.
- Process optimization.
{extra}

ANALYZED PROBLEM:
{problem}
"""

    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True)
