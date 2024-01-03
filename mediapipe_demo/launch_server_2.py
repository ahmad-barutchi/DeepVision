import cv2
import numpy as np
import mediapipe as mp
import os
import pyttsx3
import math

import base64
import os
from io import BytesIO

from PIL import Image
from flask import Flask, request, Response

from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
new_humain = True

# Make sure the images directory exists
if not os.path.exists('images'):
    os.makedirs('images')


@app.route('/video_feed', methods=['POST'])
@cross_origin()
def video_feed():
    # image = request.json['image']
    # Get the base64-encoded image data from the request JSON
    server()
    data_url = request.json.get('image')

    # Extract the base64 data from the data URL
    header, encoded = data_url.split(",", 1)
    image_data = base64.b64decode(encoded)

    # Load the image from the decoded base64 data
    img = Image.open(BytesIO(image_data))

    # Save the image as a JPEG file in the images directory
    img_path = os.path.join('images', 'myimage1.png')
    img.save(img_path)
    return Response(get_video_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')


def get_video_feed():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def search_human(path_name):
    if not (os.path.exists(path_name)):
        return False

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_holistic = mp.solutions.holistic

    # For static images:
    with mp_holistic.Holistic(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=True,
            refine_face_landmarks=True) as holistic:
        image = cv2.imread(path_name)
        image_height, image_width, _ = image.shape
        # Convert the BGR image to RGB before processing.
        results = holistic.process(image)

    return bool(results.pose_landmarks)


def msg():
    engine = pyttsx3.init()
    engine.say("There is an human.")
    engine.runAndWait()


def server():
    global new_humain
    is_human = search_human('images/myimage.png')
    if not is_human:
        new_humain = True
    if is_human and new_humain:
        # msg()
        print("Humain")
        msg()
        new_humain = False


if __name__ == '__main__':
    app.run(debug=True, port=5000)
