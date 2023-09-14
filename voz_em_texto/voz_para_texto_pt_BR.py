from huggingsound import SpeechRecognitionModel
import speech_recognition as sr # pip install SpeechRecognition

model = SpeechRecognitionModel("jonatasgrosman/wav2vec2-xls-r-1b-portuguese")

r = sr.Recognizer()

mic = sr.Microphone()

def transcrever(audio):
    return model.transcribe(audio)


ouvindo = True
while ouvindo:
    with mic as fonte:
        r.adjust_for_ambient_noise(fonte)
        print("Fale alguma coisa")
        audio = r.listen(fonte)
        print("Enviando para reconhecimento")
        try:
            #text = r.recognize_google(audio, language= "pt-BR")
            #print("Você disse: {}".format(text))
            with open("microphone-results.wav", "wb") as f:
                f.write(audio.get_wav_data())
            text = transcrever(["microphone-results.wav"])
            #print("Você disse: {}".text[0]['transcription'])
            print(text[0]['transcription'])
        except Exception as e:
            print("Não entendi o que você disse", e)
            ouvindo = False




