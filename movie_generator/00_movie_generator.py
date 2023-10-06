print("Fazendo uma automação para criar vídeos e 7 etapas")

### 1) PyTube - Download do Audio do Video
### 2) Whisper - Transcrição do Audio
### 3) ChatGPT - Tradução, Melhorias, Resumo, Descrição da Imagem e Título
### 4) Dall-E - Geração da Imagem
### 5) Requests - Baixar imagem gerada
### 6) PyTTSx3 - Criar som (pode ser feito tbm com a API da ElevenLabs)
### 7) MoviePY - Criar vídeo juntando imagem e som

chave = "sua-api-key-da-openai"
YTvideo = 'https://www.youtube.com/watch?v=gNrLWUDOAH4'

# todo gerar um vídeo com uma musica e uma imagem

### 1) PyTube
# baixar um audio de um video do yt
print("#### 1) PyTube - Baixando Audio")
from pytube import YouTube
yt = YouTube(YTvideo)
print(yt.title)
streams = yt.streams.filter(only_audio=True)
for stream in streams:
    print("streams", stream)
download = True
if download:
    stream = yt.streams.get_by_itag(140)
    downloaded_file = stream.download(output_path="./", filename="01_audio_original.mp4")

### 2) Whisper
# fazer a transcrição do audio
print("\n#### 2) Whisper - Transcrevendo")
import whisper
'''
Size	Parameters	English-only model	Multilingual model	Required VRAM	Relative speed
tiny	39 M	tiny.en	tiny	~1 GB	~32x
base	74 M	base.en	base	~1 GB	~16x
small	244 M	small.en	small	~2 GB	~6x
medium	769 M	medium.en	medium	~5 GB	~2x
large	1550 M	N/A	large	~10 GB	1x
'''
model = whisper.load_model("medium")
transcricao = model.transcribe("./01_audio_original.mp4")
print("Transcrição", transcricao["text"])

### 3) ChatGPT
# fazer a tradução
print("\n#### 3) ChatGPT - Traduzindo")
import openai

# Initialize the API key
openai.api_key = chave

def generate_answer(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", ##
        messages=[
            {"role": "user", "content": question}
            ],
        temperature=0,
    )
    return response['choices'][0]['message']['content']

texto_em_pt = generate_answer("Traduza para o português: '''" + transcricao["text"] + "'''")
print("Tradução:", texto_em_pt)

# fazer uma melhoria na traducao
texto_em_pt_qualidade = generate_answer("Melhore a qualidade deste texto: '''" + texto_em_pt + "'''")
print("Melhoria:", texto_em_pt_qualidade)

# resumir o texto
resumo_do_texto = generate_answer("Faça um resumo em primeira pessoa deste texto: '''" + texto_em_pt_qualidade + "'''")
print("Resumo:", resumo_do_texto)

# gerar descrição de uma imagem
descricao_imagem = generate_answer("Faça uma descrição de uma imagem. Use palavras amigáveis. Sem citar nomes de pessoas famosas. Com apenas uma frase a partir do resumo: '''" + resumo_do_texto + "'''")
print("Descrição da Imagem:", descricao_imagem)

# gerando um título
titulo = generate_answer("Faça um título a partir deste texto: '''" + resumo_do_texto + "'''")
print("Titulo:", titulo)

### 4) DALL-E
# gerar uma imagem relativa ao tema
print("\n#### 4) DALL-E - Gerando imagem")
response = openai.Image.create(
  prompt=descricao_imagem,
  n=1,
  size="1024x1024"
)
image_url = response['data'][0]['url']

### 5) requests
# Baixando a imagem
print("\n#### 5) requests Baixando imagem")
import requests
img_data = requests.get(image_url).content

with open('03_imagem_gerada.jpg', 'wb') as handler:
    handler.write(img_data)

### 6) PyTTSx3
print("\n#### 6) PyTTSx3 gerando texto falado")
# gerar um audio com o texto
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 150) # velocidade 120 = lento
for indice, vozes in enumerate(voices): # listar vozes
    print(indice, vozes.name)
voz = 1
engine.setProperty('voice', voices[voz].id)
engine.save_to_file(resumo_do_texto, '02_audio_traduzido.mp3')
engine.runAndWait()

### 7) MoviePY
print("\n#### 7) MoviePY - Transformando Foto e Audio em Video")
# Criando Clips
from moviepy.editor import *
image_clip = ImageClip("03_imagem_gerada.jpg")
audio_clip = AudioFileClip("02_audio_traduzido.mp3")

# fazer um video juntando imagem e texto
print("\n#### Gerando video")
video_clip = image_clip.set_audio(audio_clip)

print("Duracao", audio_clip.duration)
video_clip.duration = audio_clip.duration
video_clip.fps = 1

video_clip.write_videofile("./04_video_gerado.mp4", codec="mpeg4")

print("Finalizado")
