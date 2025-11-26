from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Set API key from environment variable
genai.api_key = os.getenv("GOOGLE_API_KEY")
MODEL = "gemini-2.5-flash"  # Your free-tier model

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    topic = data.get("topic", "")

    if not topic:
        return jsonify({"error": "No topic provided"}), 400

    try:
        response = genai.generate_text(
            model=MODEL,
            prompt=f"Explain {topic} in simple terms and provide a short quiz."
        )
        text_output = response.text
        return jsonify({"result": text_output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
