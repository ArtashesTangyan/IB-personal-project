from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# --- CONFIG ---
os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY_HERE"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")


@app.route("/explain", methods=["POST"])
def explain():
    try:
        data = request.get_json()
        text = data.get("text", "")

        response = model.generate_content(
            f"Explain this text clearly for a student: {text}"
        )

        return jsonify({"result": response.text})

    except Exception as e:
        return jsonify({"error": f"Error generating explanation: {str(e)}"}), 500


@app.route("/quiz", methods=["POST"])
def quiz():
    try:
        data = request.get_json()
        text = data.get("text", "")

        response = model.generate_content(
            f"Create a 5-question quiz based on this text. Make questions short: {text}"
        )

        return jsonify({"result": response.text})

    except Exception as e:
        return jsonify({"error": f"Error generating quiz: {str(e)}"}), 500


@app.route("/")
def home():
    return "API is running!"

if __name__ == "__main__":
    app.run(debug=True)
