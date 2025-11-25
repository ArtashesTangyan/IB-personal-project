from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure API key
genai.configure(api_key=os.getenv("API_KEY"))

# Load correct model
model = genai.GenerativeModel("gemini-1.5-flash-latest")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/explain", methods=["POST"])
def explain():
    data = request.get_json()
    topic = data.get("topic", "")

    try:
        response = model.generate_content(
            f"Explain the following World War 1 topic in a simple way for a 15-year-old student: {topic}"
        )
        return jsonify({"text": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/quiz", methods=["POST"])
def quiz():
    data = request.get_json()
    topic = data.get("topic", "")

    try:
        response = model.generate_content(
            f"Create a 5-question multiple-choice quiz about this World War 1 topic. Include answers: {topic}"
        )
        return jsonify({"text": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
