import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# Configure API key from environment variable
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# Free-tier model
MODEL = "models/text-bison-001"

@app.route("/")
def index():
    return render_template("index.html")  # Frontend HTML file

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
        # Generate response
        resp = genai.generate_text(model=MODEL, prompt=prompt)
        return jsonify({"result": resp.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
