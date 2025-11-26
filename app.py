import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Configure API Key
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/explain", methods=["POST"])
def explain():
    try:
        data = request.json
        text = data.get("text", "")
        
        response = model.generate_content(
            f"Explain the following IB topic in simple language:\n\n{text}"
        )

        return jsonify({"explanation": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/quiz", methods=["POST"])
def quiz():
    try:
        data = request.json
        text = data.get("text", "")

        response = model.generate_content(
            f"Create a 5-question quiz with answers based on this IB topic:\n\n{text}"
        )

        return jsonify({"quiz": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
    return "IB Project backend is running!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
