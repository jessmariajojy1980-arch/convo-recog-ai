from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter

# Initialize NLTK silently
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

app = Flask(__name__)
CORS(app)

# Common filler words
FILLER_WORDS = [
    "um", "uh", "like", "you know", "actually",
    "basically", "literally", "so", "well", "okay"
]

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# API to analyze text
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("text", "").lower()

    tokens = word_tokenize(text)
    total_words = len(tokens)

    # Count filler words
    filler_count = {filler: text.count(filler) for filler in FILLER_WORDS}

    # Count repeated words
    word_counts = Counter(tokens)
    repeated_words = {word: count for word, count in word_counts.items() if count > 2}

    # Remove filler words from repetition list
    for filler in FILLER_WORDS:
        repeated_words.pop(filler, None)

    return jsonify({
        "total_words": total_words,
        "filler_words": filler_count,
        "repeated_words": repeated_words
    })

if __name__ == "__main__":
    app.run(debug=True)