"use client"

from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS
import main
import os
import requests

app = Flask(__name__, static_folder='out')
CORS(app, origins=["http://127.0.0.1:5000"])
""" CORS(app, origins=["https://containerwordsearch.pythonanywhere.com",
                   "http://containerwordsearch.pythonanywhere.com", 
                   "http://127.0.0.1:5000", 
                   "http://localhost:3000"]) """

lt = main.create_letter_tree("english.txt") # containerwordsearch/

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
    if not word:
        return jsonify({"Error": "No word provided"}), 400
    word = str(word).lower()
    try:
        url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        definition = data[0]['meanings'][0]['definitions'][0]['definition']
        return jsonify({'definition': definition})
    except requests.exceptions.RequestException as e: # word not found in dictionaryapi
        # return jsonify({"Error": f"Word not found in dictionary API: {e}"}), 404 
        url = "https://scripai.com/api/getGPT" # https://corsproxy.io/?
        headers = {
            'Content-Type': 'application/json',
        }
        payload = {
            'prompt': {
                'title': f'In less than 70 tokens, {word}',
                'language': "English",
                'tone': "Informative"
            },
            'slug': "definition"
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            definition = data.get('result')
            if definition:
                return jsonify({'definition': definition})
            else:
                return jsonify({'definition': 'Error generating definition'})
        except requests.exceptions.RequestException as error:
            return jsonify({'definition': 'Error fetching resource'})
    """ try:
        url = f'https://wordsapiv1.p.mashape.com/words/{word}/definitions'
        response = requests.get(url,
                                headers={
                                    "X-Mashape-Key": "<required>", # https://rapidapi.com/dpventures/api/wordsapi/pricing # $0.004 per request over 2500 a day
                                    "Accept": "application/json"
                                })
        response.raise_for_status()
        data = response.json()
        definition = data['definitions'][0]['definition']
        return jsonify({'definition': definition})
    except requests.exceptions.RequestException as e: # word not found in dictionaryapi
        return jsonify({"Error": f"Word not found in any APIs: {e}"}), 404  """
    # try:
        # TODO: first try wordnik api https://www.wordnik.com/users/dc369868/API

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