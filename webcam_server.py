import cv2
import gunicorn
from flask import Flask, Response
import datetime

app = Flask(__name__)

def generate_frames():
    camera = cv2.VideoCapture(0)

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            font = cv2.FONT_HERSHEY_SIMPLEX
            text = "CCTV Camera"
            date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            frame = cv2.putText(frame, text, (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
            frame = cv2.putText(frame, date_time, (10, 60), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

            ret, buffer = cv2.imencode('.jpg', frame)
            if ret:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    camera.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
