import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plot
import sklearn.model_selection
import time

nome = "seno-{}".format(int(time.time()))
#tensorboard = tf.keras.callbacks.TensorBoard(log_dir='./logs/{}'.format(nome))

# Get x values of the sine wave
time = np.arange(0, 10, 0.01);

# Amplitude of the sine wave is sine of a variable like time
amplitude = np.sin(time)

# limpa plots antigos
plot.cla()

# Plot a sine wave using time and amplitude obtained for the sine wave
plot.scatter(time, amplitude, s = 10, c = 'b')

# Give a title for the sine wave plot
plot.title('Sine wave')

# Give x axis label for the sine wave plot
plot.xlabel('Time')

# Give y axis label for the sine wave plot
plot.ylabel('Amplitude = sin(time)')
plot.grid(True, which='both')
plot.axhline(y=0, color='k')
# imprime sem ruido
#plot.show()

#ruido branco
mean = 0
std = 0.06
num_samples = len(amplitude)
samples = np.random.normal(mean, std, size=num_samples)

plot.scatter(time, amplitude + samples, s = 10, c = 'g')

# Display the sine wave
# imprime com ruido
#plot.show()

entradas = np.array(amplitude)

X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(time, amplitude, test_size=0.33)

model = tf.keras.models.Sequential([
  tf.keras.layers.Dense(60, input_shape=(1,), activation=tf.nn.sigmoid),
  tf.keras.layers.Dense(30, activation=tf.nn.sigmoid),
  tf.keras.layers.Dense(1)
])

#sgd = tf.keras.optimizers.SGD(lr=0.1, momentum = 0.9)
sgd = tf.keras.optimizers.SGD(learning_rate=0.1)
#model.compile(optimizer='adam',
#              loss='sparse_categorical_crossentropy',
#              metrics=['accuracy'])
model.compile(loss='mean_squared_error', optimizer=sgd, metrics=['mean_squared_error'])

#plot.scatter(X_train,y_train,s = 10, c = 'r')
#model.fit(X_train, y_train, epochs=300, callbacks=[tensorboard], validation_split=0.3)
model.fit(X_train, y_train, epochs=300, validation_split=0.3)
print(model.evaluate(X_test, y_test))

predicao = model.predict(X_test)

plot.scatter(X_test,predicao,s = 10, c = 'r')
#imprime apos o treino
plot.show()
