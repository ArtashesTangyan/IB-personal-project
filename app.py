import os
from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Your existing model (works!)
MODEL = "openrouter/auto"

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    topic = data.get("topic")
    action = data.get("action")

    if not topic or not action:
        return jsonify({"error": "Missing topic or action"}), 400

    if action == "explanation":
        prompt = f"Explain this topic in simple language: {topic}"
    elif action == "quiz":
        prompt = (
            f"Create a 5-question multiple-choice quiz about: {topic}.\n"
            f"Each question must have A, B, C, D options and show the correct answer."
        )
    else:
        return jsonify({"error": "Invalid action"}), 400

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost",      # REQUIRED for OpenRouter
        "X-Title": "AI Study Helper",            # Recommended
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=payload,
            headers=headers
        )
        response.raise_for_status()

        data = response.json()

        text = data.get("choices", [{}])[0].get("message", {}).get("content", "")

        return jsonify({"result": text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
