from flask import Flask, request, jsonify
import openai
from datetime import datetime
import logging
from flask_cors import CORS

# Initialize the Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# OpenAI API Key configuration (replace 'your-api-key' with your actual key)
openai.api_key = 'your-api-key'

# Helper function to query OpenAI
def query_openai(prompt, max_tokens=150, temperature=0.7):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can switch to gpt-4 if available
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].text.strip()
    except Exception as e:
        logging.error(f"OpenAI query failed: {e}")
        return f"Error: {str(e)}"

# Route: Home Page
@app.route('/', methods=['GET'])
def home():
    return "Welcome to ChatIntel! Use the /api/ask endpoint to interact."

# Route: API Endpoint for Queries
@app.route('/api/ask', methods=['POST'])
def ask():
    try:
        # Get user input from JSON payload
        data = request.json
        user_query = data.get("query")
        mode = data.get("mode", "general")

        # Ensure query is provided
        if not user_query:
            return jsonify({"error": "Query is required."}), 400

        # Generate prompt based on mode
        if mode == "creative":
            prompt = f"You are a creative assistant. {user_query}"
        elif mode == "professional":
            prompt = f"You are a professional assistant. {user_query}"
        elif mode == "analytical":
            prompt = f"You are an analytical assistant. {user_query}"
        else:
            prompt = f"You are a helpful assistant. {user_query}"

        # Query OpenAI
        response = query_openai(prompt)

        # Log the interaction
        logging.info(f"User query: {user_query}, Mode: {mode}, Response: {response}")

        # Return the response
        return jsonify({
            "query": user_query,
            "response": response,
            "mode": mode,
            "timestamp": datetime.utcnow().isoformat()
        })

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

# Route: Health Check
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "timestamp": datetime.utcnow().isoformat()})

# Route: Feedback
@app.route('/api/feedback', methods=['POST'])
def feedback():
    try:
        # Get feedback from JSON payload
        data = request.json
        user_feedback = data.get("feedback")

        if not user_feedback:
            return jsonify({"error": "Feedback is required."}), 400

        # Log feedback for analysis
        logging.info(f"User feedback received: {user_feedback}")

        return jsonify({"message": "Thank you for your feedback!"})

    except Exception as e:
        logging.error(f"Error processing feedback: {e}")
        return jsonify({"error": str(e)}), 500

# Route: Multilingual Support
@app.route('/api/translate', methods=['POST'])
def translate():
    try:
        # Get translation request
        data = request.json
        text = data.get("text")
        language = data.get("language", "en")

        if not text:
            return jsonify({"error": "Text is required."}), 400

        # Generate translation prompt
        prompt = f"Translate the following text to {language}: {text}"

        # Query OpenAI for translation
        translation = query_openai(prompt)

        # Log translation
        logging.info(f"Translation requested: {text} -> {language}, Result: {translation}")

        return jsonify({
            "original_text": text,
            "translated_text": translation,
            "language": language
        })

    except Exception as e:
        logging.error(f"Error processing translation: {e}")
        return jsonify({"error": str(e)}), 500

# Route: Personalized Modes
@app.route('/api/modes', methods=['GET'])
def available_modes():
    modes = ["creative", "professional", "analytical", "general"]
    return jsonify({"available_modes": modes})

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
