from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Objeto VideoCapture do OpenCV
cap = cv2.VideoCapture(0)


def gerar_frames():
    while True:
        # Ler um frame da webcam
        sucesso, frame = cap.read()
        if not sucesso:
            break

        # Codificar o frame como JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            break

        # Converter o frame para bytes
        frame_bytes = buffer.tobytes()

        # Retornar os bytes do frame para streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')


@app.route('/')
def index():
    return render_template('index_cam.html')


@app.route('/video_feed')
def video_feed():
    return Response(gerar_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
