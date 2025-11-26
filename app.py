import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Configure API Key
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Please set the GOOGLE_API_KEY environment variable")
genai.configure(api_key=api_key)

# Use default free-tier model
model = genai.get_default_model()  # Automatically uses available free-tier model

@app.route("/")
def home():
    return render_template("index.html")

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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
