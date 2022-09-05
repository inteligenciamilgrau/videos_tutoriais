import cv2
import numpy as np
import tensorflow as tf

captura = cv2.VideoCapture(2, cv2.CAP_DSHOW)
width  = int(captura.get(cv2.CAP_PROP_FRAME_WIDTH))  # float `width`
height = int(captura.get(cv2.CAP_PROP_FRAME_HEIGHT)) # float `height`
print(width, height)

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(height,width, 3)),
    tf.keras.layers.Flatten(),
    #tf.keras.layers.Flatten(input_shape=(height,width)),
    #tf.keras.layers.Dense(5, activation="sigmoid", name="perceptron_1", use_bias=True),
    tf.keras.layers.Dense(10, activation="sigmoid", name="perceptron_2", use_bias=True),
    tf.keras.layers.Dense(10, activation="sigmoid", name="perceptron_3", use_bias=True),
    #tf.keras.layers.Dense(2, activation="softmax", name="output")
    tf.keras.layers.Dense(1, activation="sigmoid", name="output")
    ])

model.build()
print(model.summary())


model.compile(optimizer=tf.optimizers.Adam(lr=0.005),
                      loss={'output': 'mse'},
                      metrics={'output': 'accuracy'})

#initial_class = [1, 0]#None#np.array([1.0, 0.0])
initial_class = [1]

X = [] #np.array([])
y = []
images = []

while (1):
    ret, frame = captura.read()

    #pre processing
    #img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #img_gray_pre = [img_gray]
    img_gray_np = np.array([frame])#.reshape(-1, height, width, 1)







    # predicts
    predict = model.predict(img_gray_np)
    print("predict", predict)

    cv2.imshow("Video", frame)

    k = cv2.waitKey(0) & 0xff
    if k == 27 or k == ord("q"):
        break
    # select classes
    elif k == ord('1'):
        #initial_class = [1, 0]
        initial_class = [1]
        #if initial_class is None:
        #    initial_class = np.array([1.0, 0.0])
        #else:
        #    initial_class = np.concatenate((initial_class, [1.0, 0.0]))
    elif k == ord('2'):
        #initial_class = [0, 1]
        initial_class = [0]
        #if initial_class is None:
        #    initial_class = np.array([0.0, 1.0])
        #else:
        #    initial_class = np.concatenate((initial_class, [0.0, 1.0]))

    elif k == ord('t'):
        model.fit(X, np.array(y), epochs=1, shuffle=True)
    print("Class selected to train ########## ", initial_class)



    #train
    #model.fit(img_gray_np, np.array(initial_class), epochs=1)
    #print("X", X)

    #model.fit(X, y, epochs=1)
    #model.fit(np.array(X).reshape(-1, height, width, 1), np.array(y), epochs=1)
    if not k == ord("n") and not k == ord("t"):
        images.append(frame)
        print("len", len(images))
        X = np.array(images)#.reshape(-1, height, width, 1)
        #np.insert(X, -1, img_gray_np, axis=1)
        y.append(initial_class)

        #train_dataset = tf.data.Dataset.from_tensor_slices((X, y))

        ##BATCH_SIZE = 64
        #SHUFFLE_BUFFER_SIZE = 100

        #train_dataset = train_dataset.shuffle(SHUFFLE_BUFFER_SIZE)#.batch(BATCH_SIZE)

        #for i in range(1):
         #   for j in range(1):#len(X)):
           #     print("i", j, y[j])
                #model.fit(np.array(X[i]).reshape(-1, height, width, 1), np.array(y[i]), epochs=1)
                #model.fit(X[j], np.array(y[j]), epochs=1)
                #model.fit([img_gray_np], [[1]], epochs=1)
        #model.fit(train_dataset, epochs=1000)
        model.fit(X,np.array(y), epochs=1)
        print(initial_class)
        #model.fit(X, [initial_class], epochs=100)
        print("Treinei")
    print("y", y)



captura.release()
cv2.destroyAllWindows()

