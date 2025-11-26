from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# Set your API key (make sure you have set this in Render as an environment variable)
genai.api_key = os.environ.get("GENAI_API_KEY")

# Use the free-tier model directly
MODEL = "gemini-2.5-flash"

@app.route("/")
def home():
    return "IB Project backend is running!"

@app.route("/explanation", methods=["POST"])
def generate_explanation():
    data = request.get_json()
    topic = data.get("topic", "")

    if not topic:
        return jsonify({"error": "No topic provided"}), 400

    try:
        response = genai.generate_text(
            model=MODEL,
            prompt=f"Explain the following topic clearly for a 9th grader: {topic}",
            temperature=0.7,
            max_output_tokens=500
        )
        explanation = response.result
        return jsonify({"explanation": explanation})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/quiz", methods=["POST"])
def generate_quiz():
    data = request.get_json()
    topic = data.get("topic", "")

    if not topic:
        return jsonify({"error": "No topic provided"}), 400

    try:
        response = genai.generate_text(
            model=MODEL,
            prompt=f"Create a 5-question multiple-choice quiz about: {topic}",
            temperature=0.7,
            max_output_tokens=500
        )
        quiz = response.result
        return jsonify({"quiz": quiz})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
