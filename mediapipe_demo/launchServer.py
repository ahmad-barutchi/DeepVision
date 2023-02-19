import cv2
import mediapipe as mp
import pyttsx3
import math


def msg():
    engine = pyttsx3.init()
    engine.say("There is an human.")
    engine.runAndWait()


def server():
    drawing = mp.solutions.drawing_utils
    humanPose = mp.solutions.pose

    count: int = 100
    averageSize = 1, 75

    captureVid = cv2.VideoCapture(0)
    """frame_width  = 640 #captureVid.get(3)   # float `width` 640
    frame_height = 480 #captureVid.get(4)  # float `height` 480
    focale = 1.40625
    dX = 11.7"""
    # print(width)
    # print(height)
    with humanPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while (captureVid.isOpened()):
            suc, img = captureVid.read()
            if not suc:  # données de la caméra vide
                continue
            img = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
            img.flags.writeable = False
            res = pose.process(img)
            if (res.pose_landmarks):
                if (count == 100):
                    # leftEye = res.pose_landmarks.landmark[2]
                    # rightEye = res.pose_landmarks.landmark[5]
                    msg()
                    count = 0
                else:
                    count += 1
            else:
                count = 100
            img.flags.writeable = True
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            drawing.draw_landmarks(img, res.pose_landmarks, humanPose.POSE_CONNECTIONS)
            cv2.imshow("MediaPipe human pose", img)
            if cv2.waitKey(5) & 0xFF == 27:
                break
        captureVid.release()


if __name__ == "__main__":
    server()
