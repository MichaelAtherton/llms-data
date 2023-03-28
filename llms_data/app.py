# Import required libraries
import json
from flask import Flask, request, jsonify, render_template
from googletrans import Translator
from langdetect import detect

# Create a Flask app instance
app = Flask(__name__)

# Define a route for the root URL ('/') that renders the index.html template
@app.route('/')
def index():
    return render_template('index.html')

# Define a route for the '/translate_query' URL that accepts POST requests
@app.route('/translate_query', methods=['POST'])
def translate_query():
    try:
        # Get the JSON data from the POST request
        data = request.json
        # Extract the 'query' and 'target_language' fields from the JSON data
        query = data['query']
        target_language = data['target_language']

        # Detect the language of the query
        detected_lang = detect(query)

        # Translate the query using the detected language as the source language and the selected language as the target
        translator = Translator()
        translated_query = translator.translate(query, src=detected_lang, dest=target_language).text

        # Create a JSON response containing the translated query and detected language
        response = {
            'translated_query': translated_query,
            'detected_language': detected_lang
        }
        # Return the JSON response
        return jsonify(response)

    except Exception as e:
        # If there's an error, return a JSON response with the error message and a 400 status code
        return jsonify({"error": str(e)}), 400

# Start the Flask app with debug mode enabled and listening on port 5001
if __name__ == '__main__':
    app.run(debug=True, port=5001)
