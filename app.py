import os
from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# OpenRouter API key from environment variable
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

# Free-tier supported model
MODEL = "openrouter/auto"  # Works on free-tier

@app.route("/")
def index():
    return render_template("index.html")  # Your frontend HTML

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    topic = data.get("topic")
    action = data.get("action")

    if not topic or not action:
        return jsonify({"error": "Missing topic or action"}), 400

    # Prepare prompt based on action
    if action == "explanation":
        prompt = f"Explain in simple language: {topic}"
    elif action == "quiz":
        prompt = f"Create a 5-question multiple-choice quiz about: {topic}"
    else:
        return jsonify({"error": "Invalid action"}), 400

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500
        }
        response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                                 json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        # OpenRouter returns text inside: result['choices'][0]['message']['content']
        text = result['choices'][0]['message']['content']
        return jsonify({"result": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
