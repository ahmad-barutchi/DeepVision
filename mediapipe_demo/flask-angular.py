import base64
import os
from io import BytesIO

from PIL import Image
from flask import Flask, request, Response

from flask_cors import CORS, cross_origin
import cv2
from werkzeug.utils import secure_filename

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Make sure the images directory exists
if not os.path.exists('images'):
    os.makedirs('images')


@app.route('/video_feed', methods=['POST'])
@cross_origin()
def video_feed():
    # image = request.json['image']
    # Get the base64-encoded image data from the request JSON
    data_url = request.json.get('image')

    # Extract the base64 data from the data URL
    header, encoded = data_url.split(",", 1)
    image_data = base64.b64decode(encoded)

    # Load the image from the decoded base64 data
    img = Image.open(BytesIO(image_data))

    # Save the image as a JPEG file in the images directory
    img_path = os.path.join('images', 'myimage.png')
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


if __name__ == '__main__':
    app.run(debug=True, port=5000)
