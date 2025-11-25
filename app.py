from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

app = Flask(__name__)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash-latest")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/explanation", methods=["POST"])
def explanation():
    try:
        topic = request.json.get("topic", "")

        response = model.generate_content(f"Explain this topic simply: {topic}")

        return jsonify({"result": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/quiz", methods=["POST"])
def quiz():
    try:
        topic = request.json.get("topic", "")

        response = model.generate_content(
            f"Create a 5-question quiz on this topic: {topic}"
        )

        return jsonify({"result": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
