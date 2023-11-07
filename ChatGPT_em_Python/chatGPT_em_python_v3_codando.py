# para instalar todos os modulos
# pip install -r requirements.txt
import openai # pip install openai
from config_chatkey import sua_key_string
import speech_recognition as sr # pip install SpeechRecognition
import whisper # pip install whisper-openai
import pyttsx3 # pip install pyttsx3
import os
import re

# caso nao queira falar "assistente" ou "Chat GPT"
sem_palavra_ativadora = False
# printa o total de tokens por interacao
debug_custo = False
# print de algumas informacoes para debug
debugar = False
# define qual gerador de texto
# escolher_stt = "whisper"
escolher_stt = "google"
# escolhe entrada por texto ou voz
entrada_por_texto = False
# falar ou nao
falar_resposta = False
# rodar o código automaticamente
rodar = True
# ajusta ruido do ambiente
ajustar_ambiente_noise = True

if entrada_por_texto:
    sem_palavra_ativadora = True
    ajustar_ambiente_noise = False

# Initialize the API key
openai.api_key = sua_key_string

code_block_regex = re.compile(r"```(.*?)```", re.DOTALL)

def generate_answer(messages):

    try:
        #response = openai.ChatCompletion.create( ## Api antiga
        response = openai.chat.completions.create( ## API nova
            model="gpt-3.5-turbo", ##
            #model="gpt-3.5-turbo-0301", ## ateh 1 junho 2023
            messages=messages,
            temperature=0.1
        )
        return [response.choices[0].message.content, response.usage]
    except Exception as e:
        print("Deu ruim", e)
        return ["", ""]


def talk(texto):
    # falando
    engine.say(texto)
    engine.runAndWait()
    engine.stop()

def save_file(dados):
    with open(path + filename, "wb") as f:
        f.write(dados)
        f.flush()

def zerarMensagens():
    return [{"role": "system", "content": "Não explique códigos em python, somente caso seja pedido."}]

def extract_python_code(content):
    code_blocks = code_block_regex.findall(content)
    for indice, codeb in enumerate(code_blocks):
        print(indice, codeb)
        if codeb.startswith("python"):
            print("*** tem python", codeb)
            code_blocks[indice] = codeb[7:]
        if codeb.startswith("\npip install"):
            print("*** tem pip", codeb)
            code_blocks[indice] = "# " + codeb[1:]

    if code_blocks:
        full_code = "\n".join(code_blocks)



        return full_code
    else:
        return None

# reconhecer
r = sr.Recognizer()
mic = sr.Microphone()
model = whisper.load_model("base")

# falar
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 180) # velocidade 120 = lento
for indice, vozes in enumerate(voices): # listar vozes
    print(indice, vozes.name)
voz = 1 # "IVONA_2_Ricardo_OEM"
engine.setProperty('voice', voices[voz].id)

mensagens = zerarMensagens()

path = os.getcwd()
filename = "audio.wav"

print("Speak to Text", escolher_stt)

while True:
    print("###############################")
    text = ""
    question = ""

    if entrada_por_texto:
        question = input("Perguntar pro ChatGPT (\"sair\"): ")
    else:
        # Ask a question
        with mic as fonte:
            if ajustar_ambiente_noise:
                r.adjust_for_ambient_noise(fonte)
                ajustar_ambiente_noise = False
            print("Fale alguma coisa")
            audio = r.listen(fonte)
            print("Enviando para reconhecimento")

            if escolher_stt == "google":
                question = r.recognize_google(audio, language="pt-BR")
            elif escolher_stt == "whisper":
                save_file(audio.get_wav_data())

        if escolher_stt == "whisper":
            text = model.transcribe(path + filename, language='pt', fp16=False)
            question = text["text"]

    sair = {"sair", "Sair", "Desligar", "desligar"}
    zerar = {"zerar mensagens", "limpar mensagens"}
    chamar_assistente = {"Assistente", "assistente", "chat GPT", "GPT"}
    comecar = set()
    comecar.update(sair)
    comecar.update(zerar)
    comecar.update(chamar_assistente)
    comecodafrase = ""
    for espressao in comecar:
        if question.startswith(espressao):
            comecodafrase = espressao

    if comecodafrase in sair:
        print(question, "Saindo.")
        if falar_resposta:
            talk("Desligando")
        break
    elif comecodafrase in zerar:
        mensagens.clear()
        mensagens = zerarMensagens()
        print("zerou", mensagens)
    elif question == "" or question.endswith(("cancela", "cancelar", "Cancelar", "Cancela")):
        print("!!! Sem som, texto ou cancelou !!!", question)
        continue
    elif comecodafrase in chamar_assistente or sem_palavra_ativadora:
        if len(comecodafrase) > 0:
            question = question[len(comecodafrase) + 1:]
        print("Nóis:", question)
        mensagens.append({"role": "user", "content": str(question)})

        answer = generate_answer(mensagens)

        resposta = answer[0]
        preco = answer[1]

        print("ChatGPT:", resposta)

        if debug_custo:
            print("Custo:\n", preco)

        mensagens.append({"role": "assistant", "content": resposta})

        if falar_resposta:
            talk(resposta)

        code = extract_python_code(resposta)
        if code:
            if rodar:
                print("Vou rodar")
                try:
                    print("code", code)
                    print("### RODANDO ###")
                    exec(code)
                except Exception as e:
                    print("Resolve ai:", e)
                print("Done!\n")
    else:
        print("Sem mensagem", question)
        continue

    if debugar:
        print("Mensagens", mensagens, type(mensagens))
print("Ate mais")
