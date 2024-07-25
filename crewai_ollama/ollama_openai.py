from openai import OpenAI # pip install openai

client = OpenAI(api_key="nada", base_url="http://localhost:11434/v1/")

responde = client.chat.completions.create(
    model="llama3.1",
    messages=[
        {"role": "user", "content": "Qual a capital do Brasil?"}
    ],
    stream=False
)

print(responde.choices[0].message.content)
