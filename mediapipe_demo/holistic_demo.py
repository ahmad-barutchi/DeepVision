import cv2
import mediapipe as mp
import pyttsx3
import threading
from queue import Queue
import face_recognition

word = ""
last_word = ""
engine_initialized = False
engine = pyttsx3.init()

# Message queue for handling text-to-speech messages
message_queue = Queue()

def is_repeat(word):
    global last_word
    if word != last_word:
        if word == "":
            pass
            print(word)
            return True
    return False

def txt(text):
    message_queue.put(text)

def msg():
    global engine_initialized
    global engine
    while True:
        text = message_queue.get()
        repeat = is_repeat(text)
        if repeat:
            if not engine_initialized:
                engine = pyttsx3.init()
                engine_initialized = True
            engine.say(text)
            engine.runAndWait()

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic


mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.2)

prints = False

# For webcam input:
cap = cv2.VideoCapture(0)
frame_width = 1920
frame_height = 1080

cap.set(3, frame_width)  # 3 corresponds to CV_CAP_PROP_FRAME_WIDTH
cap.set(4, frame_height)  # 4 corresponds to CV_CAP_PROP_FRAME_HEIGHT


known_faces_encodings = []

with mp_pose.Pose(
        min_detection_confidence=0.8,
        min_tracking_confidence=0.8) as pose, mp_holistic.Holistic(
        min_detection_confidence=0.8,
        min_tracking_confidence=0.8) as holistic:

    # Start the message processing thread
    message_thread = threading.Thread(target=msg)
    message_thread.daemon = True
    message_thread.start()

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False


        ##############################################################################################
        # Face Recogntion

        # Process the frame with Mediapipe Face Detection
        results = face_detection.process(image)

        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = image.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)

                face_image = image[bbox[1]:bbox[1]+bbox[3], bbox[0]:bbox[0]+bbox[2]]

                # Get face encodings using face_recognition
                face_encoding = face_recognition.face_encodings(image, [(bbox[1], bbox[0], bbox[1]+bbox[3], bbox[0]+bbox[2])])

                # Check if the face matches any known face
                if face_encoding:
                    matches = face_recognition.compare_faces(known_faces_encodings, face_encoding[0])

                    if True in matches:
                        print("Welcome back!")
                    else:
                        print("Hello! What's your name?")
                        # Capture and save the new face encoding
                        known_faces_encodings.append(face_encoding[0])

                # Draw bounding box around the face
                mp_drawing.draw_detection(image, detection)

        cv2.imshow('Face Recognition', image)

        ##############################################################################################

        # Process pose
        pose_results = pose.process(image)
        if pose_results.pose_landmarks:
            if prints:
                print("y a quelqu'un")
        
        # Process holistic
        holistic_results = holistic.process(image)
        if holistic_results.face_landmarks:
            if prints:
                print("un visage")

        # Draw landmarks on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Check if hand landmarks are detected
        if holistic_results.left_hand_landmarks and holistic_results.right_hand_landmarks:
            # Define finger landmarks for left and right hands
            left_finger_landmarks = [holistic_results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP],
                                      holistic_results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_TIP],
                                      holistic_results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.RING_FINGER_TIP],
                                      holistic_results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.PINKY_TIP],
                                      holistic_results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.THUMB_TIP]]

            right_finger_landmarks = [holistic_results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP],
                                       holistic_results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_TIP],
                                       holistic_results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.RING_FINGER_TIP],
                                       holistic_results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.PINKY_TIP],
                                       holistic_results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.THUMB_TIP]]

            # Count the number of fingers up for each hand
            left_fingers_up = sum(1 for landmark in left_finger_landmarks if landmark.y < holistic_results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_MCP].y)
            right_fingers_up = sum(1 for landmark in right_finger_landmarks if landmark.y < holistic_results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_MCP].y)

            # Print the number of fingers up for each hand
            word = f"main droite: {left_fingers_up}"
            txt(word)
            word = f"main gauche: {right_fingers_up}"
            txt(word)
            word = ""

        if holistic_results.left_hand_landmarks:
            if holistic_results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP].y > holistic_results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_MCP].y:
                word = "APPUIEZ AVEC L'INDEX DROITE"
                txt(word)

        if holistic_results.right_hand_landmarks:
            if (holistic_results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP].y > holistic_results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_PIP].y 
            and holistic_results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.RING_FINGER_TIP].y > holistic_results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_PIP].y
            and holistic_results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.THUMB_TIP].y > holistic_results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_PIP].y
            and holistic_results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.PINKY_TIP].y > holistic_results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_PIP].y
            and holistic_results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_TIP].y < holistic_results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_MCP].y):
                word = "Fais pas ça frérot"
                txt(word)

        if holistic_results.right_hand_landmarks:
            if (holistic_results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_TIP].y > holistic_results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_MCP].y 
            and holistic_results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.RING_FINGER_TIP].y > holistic_results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_MCP].y
            and holistic_results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.THUMB_TIP].y > holistic_results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.INDEX_FINGER_MCP].y
            and holistic_results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.PINKY_TIP].y > holistic_results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_MCP].y
            and holistic_results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_TIP].y > holistic_results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.MIDDLE_FINGER_MCP].y):
                print("Ta main est fermer")


        # Draw hand landmarks on the image.
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing.draw_landmarks(
            image, holistic_results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        mp_drawing.draw_landmarks(
            image, holistic_results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        mp_drawing.draw_landmarks(
            image, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow('MediaPipe Pose and Holistic', image)

        if cv2.waitKey(200) & 0xFF == 27:
            prints = not prints
            print("Changer manuellement Pause/Play")

        last_word = word

cap.release()
cv2.destroyAllWindows()