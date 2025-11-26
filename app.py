import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Configure Gemini API Key
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        topic = data.get("topic", "")

        # Generate explanation
        explanation_resp = model.generate_content(
            f"Explain the following IB topic in simple language:\n\n{topic}"
        )

        # Generate quiz
        quiz_resp = model.generate_content(
            f"Create a 5-question quiz with answers based on this IB topic:\n\n{topic}"
        )

        return jsonify({
            "explanation": explanation_resp.text,
            "quiz": quiz_resp.text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "IB Project backend is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
