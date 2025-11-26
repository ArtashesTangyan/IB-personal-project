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

# Use your free-tier model
MODEL = "gemini-2.5-flash"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/explain", methods=["POST"])
def explain():
    try:
        data = request.json
        text = data.get("text", "")

        response = genai.chat(model=MODEL, 
                              messages=[{"role": "user", "content": f"Explain the following IB topic in simple language:\n\n{text}"}])

        return jsonify({"explanation": response.last.message["content"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/quiz", methods=["POST"])
def quiz():
    try:
        data = request.json
        text = data.get("text", "")

        response = genai.chat(model=MODEL, 
                              messages=[{"role": "user", "content": f"Create a 5-question quiz with answers based on this IB topic:\n\n{text}"}])

        return jsonify({"quiz": response.last.message["content"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
