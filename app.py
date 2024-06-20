"use client"

from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS
import main
import os
import requests

app = Flask(__name__, static_folder='out')
CORS(app, origins=["http://containerwordsearch.pythonanywhere.com", 
                   "http://127.0.0.1:5000", 
                   "http://localhost:3000"])

lt = main.create_letter_tree("containerwordsearch/english.txt") # 

@app.route('/api/search', methods=['POST'])
def search():
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
    
@app.route('/api/definition', methods=['GET'])
def get_definition():
    word = request.args.get('word')
    word = str(word).lower()
    try:
        url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        definition = data[0]['meanings'][0]['definitions'][0]['definition']
        return jsonify({'definition': definition})
    except requests.exceptions.RequestException as e: # word not found in dictionaryapi
        try:
            # TODO: first try wordnik api
            scripai_url = "https://scripai.com/api/getGPT"
            payload = {'prompt': 
                       {'title': f"In less than 70 tokens, {word}", 
                        'language': "English", 
                        'tone': "Informative"}, 
                        'slug': "definition"}
            headers = {
                'Content-Type': 'application/json',
            }
            response = requests.post(scripai_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            definition = data['result']
            return jsonify({'definition': definition})
        except requests.exceptions.RequestException as e: # scripai failed for some reason
            # definition = main.get_definition(word) # get word definition via AI.
            # return jsonify({'definition': definition})
            return jsonify({"Error": "No definition found"}), 400
    
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