import os
from flask import Flask, request, jsonify, render_template
import google.genai as genai

app = Flask(__name__)

# --- Get API key from environment variable ---
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("Please set the GOOGLE_API_KEY environment variable in Render or locally.")

# --- Initialize Google AI client ---
client = genai.Client(api_key=API_KEY)

# --- Generate explanation ---
def generate_explanation(topic):
    try:
        response = client.generate_text(
            model="text-bison-001",
            prompt=f"Explain this topic in simple terms: {topic}"
        )
        return response.text
    except Exception as e:
        return f"Error generating explanation: {e}"

# --- Generate quiz ---
def generate_quiz(topic):
    try:
        response = client.generate_text(
            model="text-bison-001",
            prompt=f"Create a 5-question quiz about: {topic}. Only output the questions."
        )
        return response.text
    except Exception as e:
        return f"Error generating quiz: {e}"

# --- API endpoint ---
@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    topic = data.get("topic", "")
    explanation = generate_explanation(topic)
    quiz = generate_quiz(topic)
    return jsonify({"explanation": explanation, "quiz": quiz})

# --- Serve index.html from templates folder ---
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
