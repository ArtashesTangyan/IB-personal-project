import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# Load API key
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY is not set!")
genai.configure(api_key=API_KEY)

# Create model
model = genai.GenerativeModel("gemini-1.5-flash")


def generate_explanation(topic):
    try:
        response = model.generate_content(
            f"Explain this topic in simple terms for a student: {topic}"
        )
        return response.text
    except Exception as e:
        return f"Error generating explanation: {e}"


def generate_quiz(topic):
    try:
        response = model.generate_content(
            f"Create a 5-question quiz about {topic}. Only output the questions."
        )
        return response.text
    except Exception as e:
        return f"Error generating quiz: {e}"


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    topic = data.get("topic", "")
    explanation = generate_explanation(topic)
    quiz = generate_quiz(topic)
    return jsonify({"explanation": explanation, "quiz": quiz})


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
