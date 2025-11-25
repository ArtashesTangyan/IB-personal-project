from flask import Flask, request, jsonify, render_template
from google import genai
import os

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.5-flash"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/generate", methods=["POST"])
def generate():
    topic = request.json.get("topic", "")
    try:
        explanation = client.models.generate_content(
            model=MODEL,
            contents=f"Explain {topic} in simple terms."
        ).text

        quiz = client.models.generate_content(
            model=MODEL,
            contents=f"Create a 5-question quiz about {topic}."
        ).text

        return jsonify({
            "explanation": explanation,
            "quiz": quiz
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
