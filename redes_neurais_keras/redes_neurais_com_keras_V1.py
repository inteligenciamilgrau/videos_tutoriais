import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # float `width`
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`
print(width, height)

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(height, width, 3)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(100, activation="sigmoid", name="perceptron_1"),
    tf.keras.layers.Dense(100, activation="sigmoid", name="perceptron_2"),
    tf.keras.layers.Dense(100, activation="sigmoid", name="perceptron_3"),
    tf.keras.layers.Dense(100, activation="sigmoid", name="perceptron_4"),
    tf.keras.layers.Dense(100, activation="sigmoid", name="perceptron_5"),
    #tf.keras.layers.Dense(100, activation="sigmoid", name="perceptron_6"),
    #tf.keras.layers.Dense(100, activation="sigmoid", name="perceptron_7"),
    #tf.keras.layers.Dense(100, activation="sigmoid", name="perceptron_8"),
    #tf.keras.layers.Dense(100, activation="sigmoid", name="perceptron_9"),
    #tf.keras.layers.Dense(100, activation="sigmoid", name="perceptron_10"),
    #tf.keras.layers.Dense(1, activation="sigmoid", name="output")
    tf.keras.layers.Dense(2, activation="softmax", name="output")
])

model.build()
print(model.summary())

model.compile(optimizer=tf.optimizers.Adam(lr=0.001),
              loss={'output': 'mse'},
              metrics={'output': 'accuracy'})

initial_class = [1.0, 0.0]
#initial_class = [1.0]

X = []
y = []
images = []

# construct the training image generator for data augmentation
aug = ImageDataGenerator(rotation_range=1, zoom_range=0.0,
                             width_shift_range=0.1, height_shift_range=0.05, shear_range=0.15,
                             horizontal_flip=False, fill_mode="constant", validation_split=0.30)

EPOCHS = 100
BS = 8

while True:
    ret, frame = cap.read()
    cv2.imshow("Video", frame)

    k = cv2.waitKey(1) & 0xff

    grab_image = False
    if k == 27 or k == ord("q"):
        break
    # select classes
    elif k == ord('1'):
        initial_class = [1.0, 0.0]
        #initial_class = [1.0]
        grab_image = True
    elif k == ord('2'):
        initial_class = [0.0, 1.0]
        #initial_class = [0.0]
        grab_image = True

    elif k == ord('t'):
        model.fit(np.array(images), np.array(y), epochs=EPOCHS, shuffle=True, batch_size=BS, validation_split=0.3)

    if k == ord("p"):
        predict = model.predict(np.array([frame]))
        predict_label = list(np.where(predict[0] >= 0.5, 1, 0))
        max_value = max(predict_label)
        max_index = predict_label.index(max_value)
        labels = ["Inteligencia Mil Grau - LOGO", "DEV FEST 2018"]
        print("Predict Label", labels[max_index])
        print("predict", predict)

    preview_gen = False
    if preview_gen:
        img = aug.flow(np.array([frame]), np.array([initial_class]), batch_size=BS)
        cv2.imshow("grab", img[0][0][0].astype(np.uint8))

    if grab_image:
        print("Class selected to train ########## ", initial_class)

        images.append(frame)
        y.append(initial_class)

        for i in range(0):
            img = aug.flow(np.array([frame]), np.array([initial_class]), batch_size=BS)

            images.append(img[0][0][0].astype(np.uint8))
            y.append(initial_class)

        print(initial_class)
        print("y", y)

cap.release()
cv2.destroyAllWindows()
