from flask import Flask, render_template

app = Flask(__name__)

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Login page
@app.route("/login")
def login():
    return "<h1>Login page coming soon</h1>"

# Dashboard page
@app.route("/dashboard")
def dashboard():
    return "<h1>Dashboard coming soon</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
