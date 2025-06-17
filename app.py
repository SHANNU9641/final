from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")  # Now uses environment variable
TOGETHER_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message", "")
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}"
    }
    json_data = {
        "model": TOGETHER_MODEL,
        "prompt": f"You are an educational chatbot. Answer clearly:\n\n{user_input}\n\nAnswer:",
        "max_tokens": 200,
        "temperature": 0.7
    }
    res = requests.post("https://api.together.ai/v1/completions", headers=headers, json=json_data)

    if res.status_code == 200:
        reply = res.json().get("choices", [{}])[0].get("text", "Sorry, no response.")
    else:
        reply = f"Error: {res.status_code}"

    return jsonify({"response": reply.strip()})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Use Render's assigned port
    app.run(host="0.0.0.0", port=port)
