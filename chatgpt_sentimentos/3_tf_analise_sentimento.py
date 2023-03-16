import pandas as pd
import tensorflow as tf
import numpy as np

#configuracoes
vocab_size = 10000
embedding_dim = 16
max_length = 100
trunc_type='post'
padding_type='post'
oov_tok = "<OOV>"

print("### Etapa 1 - Carregar dados e organizar")

# carrega arquivo com as avaliacoes
sentimento_df = pd.read_csv("reviews.csv")

print(sentimento_df.info())
print(sentimento_df.head())
print(sentimento_df['content'].head())
print(sentimento_df['score'].head())

# Converte notas de 1 a 5 em 0 e 1
def to_sentiment(rating):
  rating = int(rating)
  if rating <= 2:
    return 0
  else:
    return 1

sentimento_df['sentiment'] = sentimento_df.score.apply(to_sentiment)

# Organiza os dados em Treino e Teste
training_size = 7000
training_sentences = sentimento_df['content'].iloc[0:training_size].copy()
testing_sentences = sentimento_df['content'].iloc[training_size:].copy()
print(training_sentences.info())
print(training_sentences.head())

training_labels = sentimento_df['sentiment'].iloc[0:training_size].copy()
testing_labels = sentimento_df['sentiment'].iloc[training_size:].copy()

print("### Etapa 2 - Converter palavras em numeros")
from tensorflow.keras.preprocessing.text import Tokenizer
tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_tok)
tokenizer.fit_on_texts(training_sentences)
word_index = tokenizer.word_index

print("### Etapa 3 - Criar as frases/sequencias")
from tensorflow.keras.preprocessing.sequence import pad_sequences
sequencias_treinamento = tokenizer.texts_to_sequences(training_sentences)
padded_treinamento = pad_sequences(sequencias_treinamento, maxlen=max_length, padding=padding_type, truncating=trunc_type)
sequencias_teste = tokenizer.texts_to_sequences(testing_sentences)
padded_teste = pad_sequences(sequencias_teste, maxlen=max_length, padding=padding_type, truncating=trunc_type)

print("### Etapa 4 - Criando a rede neural")
model = tf.keras.Sequential([
  tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
  tf.keras.layers.GlobalAveragePooling1D(),
  tf.keras.layers.Dense(24, activation="relu"),
  tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

print("### Etapa 5 - Treinando a rede")
num_epochs = 30
history = model.fit(padded_treinamento, training_labels, epochs=num_epochs,
                    validation_data=(padded_teste, testing_labels), verbose=2)

print("### Etapa 6 - Final - Testando com uma nova frase")

frases_avaliacao = ["Eu não gostei de nada disso", "Estava excelente, principalmente o hamburguer", "Nem tão bom, nem tão ruim"]

sequencia = tokenizer.texts_to_sequences(frases_avaliacao)
padded = pad_sequences(sequencia, maxlen=max_length, padding=padding_type, truncating=trunc_type)

probs = model.predict(padded)

class_names = ['Negativo:', 'Positivo:']
for index, frase in enumerate(frases_avaliacao):
  print(class_names[round(probs[index][0])], probs[index], frase)
