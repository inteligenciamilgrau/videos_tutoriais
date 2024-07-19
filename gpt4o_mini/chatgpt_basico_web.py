import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, send_file
import tempfile

# Load the API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_VOICE = "alloy"

app = Flask(__name__)
def list_models():
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}"
        }
        response = requests.get(f"{BASE_URL}/models", headers=headers)
        response.raise_for_status()
        models = response.json()
        return [model['id'] for model in models['data']]
    except requests.RequestException as e:
        print(f"An error occurred while listing models: {e}")
        return []

def chat_with_model(model, user_input, conversation_history):
    conversation_history.append({"role": "user", "content": user_input})
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": conversation_history
        }
        response = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        assistant_response = response.json()['choices'][0]['message']['content']
        conversation_history.append({"role": "assistant", "content": assistant_response})
        return assistant_response, conversation_history
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return "Desculpe, ocorreu um erro ao processar sua solicitação.", conversation_history

def text_to_speech(text, voice=DEFAULT_VOICE):
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "tts-1",
            "input": text,
            "voice": voice
        }
        response = requests.post(f"{BASE_URL}/audio/speech", headers=headers, json=data)
        response.raise_for_status()
        
        # Save the audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_file.write(response.content)
            temp_file_path = temp_file.name
        
        return temp_file_path
    except requests.RequestException as e:
        print(f"An error occurred while generating speech: {e}")
        return None
@app.route('/')
def index():
    models = list_models()
    return render_template('index.html', models=models, default_model=DEFAULT_MODEL)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    model = data.get('model', DEFAULT_MODEL)
    user_input = data.get('user_input', '')
    conversation_history = data.get('conversation_history', [])
    
    response, updated_history = chat_with_model(model, user_input, conversation_history)
    
    # Generate speech from the response
    audio_file_path = text_to_speech(response)
    return jsonify({
        'response': response,
        'conversation_history': updated_history,
        'audio_file': audio_file_path
    })

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_file(filename, mimetype="audio/mpeg")
if __name__ == '__main__':
    app.run(debug=True)
