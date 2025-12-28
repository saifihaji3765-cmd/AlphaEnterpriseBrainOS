from flask import Flask, request, render_template, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    user_input = request.form.get("text")

    if not user_input:
        return "No input provided", 400

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are FutureGuard AI, a business risk analysis assistant."},
            {"role": "user", "content": user_input}
        ]
    )

    ai_reply = response.choices[0].message.content

    return render_template("index.html", result=ai_reply)

# Vercel needs this
app = app
