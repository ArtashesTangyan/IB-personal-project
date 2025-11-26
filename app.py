import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Try multiple env var names so it's flexible
API_KEY = os.getenv("API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError(
        "Please set an environment variable named API_KEY or GOOGLE_API_KEY (your Gemini API key)."
    )

# Configure the library
genai.configure(api_key=API_KEY)

# Use a current model name
MODEL_NAME = "gemini-1.5-flash-latest"
model = genai.GenerativeModel(MODEL_NAME)

@app.route("/")
def index():
    return render_template("index.html")

def safe_generate(prompt: str, purpose: str = "explain"):
    """Call model.generate_content and return text or raise."""
    try:
        resp = model.generate_content(prompt)
        # resp.text contains the generated string
        return resp.text
    except Exception as e:
        # Print full exception to stdout so Render runtime logs capture it
        print(f"[ERROR] generate_content ({purpose}) failed:", repr(e))
        raise

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}
    topic = data.get("topic", "").strip()
    if not topic:
        return jsonify({"explanation": "No topic provided.", "quiz": "No topic provided."}), 400

    # Build prompts
    explain_prompt = f"Explain this topic in clear simple terms suitable for a 14-16 year old student: {topic}"
    quiz_prompt = (
        f"Create a 5-question quiz about the topic '{topic}'. Provide questions only, numbered 1–5."
    )

    try:
        explanation = safe_generate(explain_prompt, "explanation")
    except Exception as e:
        explanation = f"Error generating explanation: {e}"

    try:
        quiz = safe_generate(quiz_prompt, "quiz")
    except Exception as e:
        quiz = f"Error generating quiz: {e}"

    return jsonify({"explanation": explanation, "quiz": quiz})

if __name__ == "__main__":
    # For local testing only — Render will use gunicorn via Procfile
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
