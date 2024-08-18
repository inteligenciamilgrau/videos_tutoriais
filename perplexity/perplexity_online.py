from openai import OpenAI
import os
import json
from dotenv import load_dotenv
load_dotenv()

model = "llama-3.1-sonar-small-128k-online"
#model = "llama-3.1-sonar-large-128k-online"
#model = "llama-3.1-sonar-huge-128k-online"

tema = "olimpíadas 2024 sobre o Brasil"
#tema = "Artificial intelligence at 'https://the-decoder.com'"

messages = [
    {
        "role": "system",
        "content": (
            "You are a helpfull online search assistant who search for websites over the internet"
            #"Você é um assistente de pesquisas online que busca sites pela internet."
        ),
    },
    {
        "role": "user",
        "content": (
            f"""Pesquise sites com videos sobre {tema}.
            Encontre pelo menos 3 videos.
            Diga o título completo do video.
            Escreva o link completo do video.
            Mantenha o link com o texto original sem traduzir.
            Encontre também vídeos do youtube.
            Responda em um JSON como no exemplo:
            [
                {{
                    "titulo/video": "...",
                    "descrição": "...",
                    "link": "..."
                }},
                {{
                    "titulo/video": "...",
                    "descrição": "...",
                    "link": "..."
                }}
            ]
            """
        ),
        "return_citations": True,
        "return_images": False,
        "return_related_questions": True,
        #"search_domain_filter": array, # Defaults to null
        # Given a list of domains, limit the citations
        # used by the online model to URLs from the 
        # specified domains. This feature is in closed beta 
        # access. To gain access, apply at 
        # https://perplexity.typeform.com/to/j50rnNiB
    },
]

client = OpenAI(api_key=os.getenv("PPLX_API_KEY"), base_url="https://api.perplexity.ai")

# chat completion without streaming
response = client.chat.completions.create(
    model=model,
    messages=messages,
)
print("Message", response, "\n")
respostas = response.choices[0].message.content.strip("```").replace("json", "")
print("String", respostas)
respostas_dict = json.loads(respostas)
print("Dict", respostas_dict)

for index, resposta in enumerate(respostas_dict):
    print("")
    print("Resposta", index + 1)
    print("Titulo:", resposta["titulo/video"])
    print("Descrição:", resposta["descrição"])
    print("Link:", resposta["link"])
