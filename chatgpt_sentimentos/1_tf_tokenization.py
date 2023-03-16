from tensorflow.keras.preprocessing.text import Tokenizer

frases = ['eu amo meu cachorro',
          'Eu amo meu gato']

tokenizer = Tokenizer(num_words=100)  # num_words igual a 100 significa 100 palavras mais relevantes
tokenizer.fit_on_texts(frases)
word_index = tokenizer.word_index

print(word_index)
