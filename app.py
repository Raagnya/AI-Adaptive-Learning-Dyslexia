from flask import Flask, render_template, request, jsonify
from services.generator import generate_sentence
from services.ocr_service import preprocess_image, extract_text
from services.evaluator import evaluate_response
from services.adaptive import update_difficulty

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}
    difficulty = data.get("difficulty", "easy")
    topic = data.get("topic", "everyday life")
    sentence = generate_sentence(difficulty, topic)
    return jsonify({"sentence": sentence, "difficulty": difficulty})

@app.route("/evaluate", methods=["POST"])
def evaluate():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    expected = request.form.get("expected", "").strip()
    difficulty = request.form.get("difficulty", "easy")
    image = request.files["image"]

    processed = preprocess_image(image)
    extracted = extract_text(processed)

    result = evaluate_response(expected, extracted)
    new_difficulty = update_difficulty(difficulty, result["score"])

    return jsonify({
        "expected": expected,
        "extracted": extracted,
        "score": result["score"],
        "feedback": result["feedback"],
        "new_difficulty": new_difficulty
    })

if __name__ == "__main__":
    app.run(debug=True)
