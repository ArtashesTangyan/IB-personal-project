import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Configure Gemini API Key
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Serve HTML interface
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# Generate explanation + quiz
@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        topic = data.get("topic", "")

        explanation_resp = model.generate_content(
            f"Explain the following IB topic in simple language:\n\n{topic}"
        )

        quiz_resp = model.generate_content(
            f"Create a 5-question quiz with answers based on this IB topic:\n\n{topic}"
        )

        return jsonify({
            "explanation": explanation_resp.text,
            "quiz": quiz_resp.text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
