import os
import requests
from dotenv import load_dotenv

# Load the API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-4o-mini"

def list_models():
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}"
        }
        response = requests.get(f"{BASE_URL}/models", headers=headers)
        response.raise_for_status()
        models = response.json()
        print("Available models:")
        for model in models['data']:
            print(f"- {model['id']}")
    except requests.RequestException as e:
        print(f"An error occurred while listing models: {e}")

def chat_with_model(model):
    conversation_history = [
        {"role": "system", "content": "Você é um assistente atencioso."}
    ]

    print(f"\nBem-vindo ao chat! Usando o modelo: {model}")
    print("Digite 'sair' para encerrar a conversa.")

    while True:
        user_input = input("\nVocê: ")
        if user_input.lower() == 'sair':
            print("Obrigado por conversar comigo. Até a próxima!")
            break

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
            
            print(f"\nAssistente: {assistant_response}")
            
            conversation_history.append({"role": "assistant", "content": assistant_response})
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
def main():
    # 1) List available models
    list_models()

    # 2) Choose a model and start the chat
    chosen_model = input(f"\nDigite o nome do modelo que você quer usar (ou pressione Enter para usar o padrão: {DEFAULT_MODEL}): ")
    if not chosen_model:
        chosen_model = DEFAULT_MODEL
        print(f"Nenhum modelo escolhido. Usando o modelo padrão: {DEFAULT_MODEL}")

    chat_with_model(chosen_model)
if __name__ == "__main__":
    main()
