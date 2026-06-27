import os
import json
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder="", static_url_path="")
CORS(app)


def load_candidates():
    with open(os.path.join(BASE_DIR, "sample_candidates.json"), "r", encoding="utf-8") as file:
        return json.load(file)


@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/candidates", methods=["GET"])
def get_candidates():
    candidates = load_candidates()
    return jsonify(candidates)


@app.route("/candidate/<candidate_id>", methods=["GET"])
def get_candidate(candidate_id):
    candidates = load_candidates()

    for candidate in candidates:
        if candidate["candidate_id"] == candidate_id:
            return jsonify(candidate)

    return jsonify({
        "error": "Candidate not found"
    }), 404


@app.route("/<path:filename>")
def serve_frontend(filename):
    file_path = os.path.join(BASE_DIR, filename)
    if os.path.isfile(file_path):
        return send_from_directory(BASE_DIR, filename)

    return jsonify({
        "error": "Page not found"
    }), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)