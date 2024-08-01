import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
def send_message(prompt, sistema = "", json_format = False):

    api_key = os.getenv("OPENAI_API_KEY")  # Get the API key from the environment
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    formato = "text"
    if json_format:
        formato = "json_object"

    mensagem = []
    if sistema != "":
        mensagem.append({"role": "system", "content": sistema})
    mensagem.append({"role": "user", "content": prompt})

    data = {
        "model": "gpt-4o-mini",  # Ensure to specify the correct model
        "messages": mensagem,
        "max_tokens": 16_384,  # You can adjust this as needed
        "response_format": { "type": formato },
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response_json = response.json()
        if json_format:
            return json.loads(response_json['choices'][0]['message']['content'])
        return response_json['choices'][0]['message']['content']
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None