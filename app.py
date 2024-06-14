"use client"

from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS
import main
import os

app = Flask(__name__, static_folder='out')
CORS(app, origins=["http://containerwordsearch.pythonanywhere.com"])

lt = main.create_letter_tree()

@app.route('/api/search', methods=['POST'])
def search():
    # prompt = request.form.get('prompt')
    if not request.is_json:
        return jsonify({'error': 'Only JSON format is supported'}), 415
    prompt = request.json.get('prompt')
    if prompt:
        prompt = prompt.strip().upper()
        solves = lt.get_solves(prompt)
        desired_solves = main.get_desired_solves(solves, 0)
        return jsonify(desired_solves)
    else:
        return jsonify({"Error": "No prompt provided"}), 400
    

# Serve the index.html for the root route
@app.route('/')
def serve_index():
    return send_file(os.path.join(app.static_folder, 'index.html'))

# Serve static files from the out directory
@app.route('/<path:path>')
def serve_static_files(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_file(os.path.join(app.static_folder, 'index.html'))

if __name__ == '__main__':
    app.run(debug=True)