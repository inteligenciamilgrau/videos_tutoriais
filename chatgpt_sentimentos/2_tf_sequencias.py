from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

frases = ['eu amo meu cachorro',
          'Eu amo meu gato',
          'você ama meu cachorro!',
          'você acha meu cachorro incrível?']

#tokenizer = Tokenizer(num_words=100)  # num_words igual a 100 significa 100 palavras mais relevantes
tokenizer = Tokenizer(num_words=100, oov_token="<OOV>")  # oov = out of vocabulary
tokenizer.fit_on_texts(frases)
word_index = tokenizer.word_index

sequencias = tokenizer.texts_to_sequences(frases)

sequencias_preenchidas = pad_sequences(sequencias, padding='post'
                       , truncating='post', maxlen=6, value=0)  # pad = preencher  # truncate = cortar # pre ou post

print("word_index", word_index)
print("sequencias", sequencias)
print("sequencias_preenchidas", sequencias_preenchidas)

testando = ['eu realmente amo meu cachorro',
            'meu cachorro ama atum']

testando_sequencias = tokenizer.texts_to_sequences(testando)
print("testando_sequencias", testando_sequencias)