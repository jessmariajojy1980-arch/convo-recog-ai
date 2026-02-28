from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter

# Ensure NLTK data is downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

app = Flask(__name__)
CORS(app)

# Common filler words for analysis
FILLER_WORDS = [
    "um", "uh", "like", "actually", "basically", 
    "literally", "so", "well", "okay", "right", "you know"
]

@app.route("/")
def home():
    # This looks for index.html inside the 'templates' folder
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    raw_text = data.get("text", "").lower()
    
    # Tokenize and clean punctuation
    tokens = [word for word in word_tokenize(raw_text) if word.isalpha()]
    total_words = len(tokens)

    # Count filler words based on exact token matches
    filler_count = {filler: tokens.count(filler) for filler in FILLER_WORDS}

    # Count word frequencies
    word_counts = Counter(tokens)
    
    # Identify words repeated more than 2 times (excluding filler words)
    repeated_words = {
        word: count for word, count in word_counts.items() 
        if count > 2 and word not in FILLER_WORDS
    }

    return jsonify({
        "total_words": total_words,
        "filler_words": filler_count,
        "repeated_words": repeated_words
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)