# Instrucoes
# instalar openai com "pip install openai"
# criar uma chave "API key" no site da OpenAI
# substituir a sua chave no codigo

import openai

# Initialize the API key
openai.api_key = "sua_key_string"

def gerar_resposta(messages):
    #response = openai.ChatCompletion.create( ## Api antiga
    response = openai.chat.completions.create( ## API nova
        model="gpt-3.5-turbo", 
        messages=messages,
        temperature=0.5
    )
    return [response.choices[0].message.content, response.usage]

mensagens = [{"role": "system", "content": "Você é um assistente gente boa."}]

while True:
    # Ask a question
    question = input("Perguntar pro ChatGPT (\"sair\"): ")

    if question == "sair" or question == "":
        print("saindo")
        break
    else:
        mensagens.append({"role": "user", "content": str(question)})

        answer = gerar_resposta(mensagens)
        print("Nóis:", question)
        print("ChatGPT:", answer[0], "\nCusto:\n", answer[1])
        mensagens.append({"role": "assistant", "content": answer[0]})

    debugar = False
    if debugar:
        print("Mensagens", mensagens, type(mensagens))
