from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Set your API key in environment variable GOOGLE_API_KEY
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

MODEL = "models/text-bison-001"  # Free-tier model

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    topic = data.get("topic")
    action = data.get("action")  # 'explanation' or 'quiz'

    if not topic or not action:
        return jsonify({"error": "Topic and action are required"}), 400

    prompt = ""
    if action == "explanation":
        prompt = f"Write a clear B2-level explanation of the topic: {topic}."
    elif action == "quiz":
        prompt = f"Create a short quiz (5 questions) about the topic: {topic}."
    else:
        return jsonify({"error": "Invalid action"}), 400

    try:
        response = genai.generate_text(
            model=MODEL,
            prompt=prompt,
            temperature=0.7,
            max_output_tokens=500
        )
        return jsonify({"result": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
