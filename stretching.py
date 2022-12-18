import cv2
import mediapipe as mp
import numpy as np
from time import sleep
# from PIL import ImageFont, ImageDraw, Image

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

msg = None
s=0
d=0

# 선의 중점과 점의 거리
def lineDistance(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    linedist = np.linalg.norm(c - b)  # 점 b와 c사이의 거리
    center = [(b[0] - c[0]) / 2, b[1] - c[1] / 2]  # b와 c의 중점

    dist = np.linalg.norm(center - a)  # b와 c의 중점과 a의 거리

    return dist



#ab와 bc의 각도
def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle


## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates
            # 코 좌표 받기
            nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x,
                    landmarks[mp_pose.PoseLandmark.NOSE.value].y]
            # 왼쪽 어깨 좌표 받기
            left = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

            # 오른쪽 어깨 좌표 받기
            right = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

            #왼쪽 손목 좌표 받기
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            #오른쪽 손목 좌표 받기
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            #왼쪽 팔꿈치 좌표 받기
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]


            #오른쪽 팔꿈치 좌표 받기
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

            left_eye= [landmarks[mp_pose.PoseLandmark.LEFT_EYE.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_EYE.value].y]

            right_eye= [[landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value].y]]

            left_mouth=[landmarks[mp_pose.PoseLandmark.MOUTH_LEFT.value].x,
                           landmarks[mp_pose.PoseLandmark.MOUTH_LEFT.value].y]
            right_mouth = [landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT.value].x,
                           landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT.value].y]

            l_y = left[1]
            r_y = right[1]


            # 위로 팔 펴는 스트레칭시작
            if cv2.waitKey(10) & 0xFF == ord('s'):
                msg = "step1"
                s=1

            # 목 스트레칭 시작
            if cv2.waitKey(10) & 0xFF == ord('d'):
                msg = "step1"
                d=1

            # 팔꿈치 펴짐 각도
            l_arm = calculate_angle(left_wrist,left_elbow,left)
            r_arm = calculate_angle(right_wrist,right_elbow,right)

            #좌우 손목의 높이와 코의 높이의 차
            height_l = left_wrist[1] - nose[1]
            height_r = right_wrist[1] - nose[1]

            if s: #s버튼을 누르면
                if height_l < 0 and height_r < 0:
                    msg = "step2"

                    if l_arm >160 and r_arm>160:
                        sleep(5)
                        msg = "finish"
                        s=0
            if d: #d버튼 누르면
                if left_mouth[1] < right_eye[1]:
                    msg="step2"
                    sleep(5)
                    #5초간 유지후 왼쪽으로

                    if right_mouth[1] < left_eye[1]:
                        msg="step3"
                        sleep(5)
                        msg="finish"
                        d=0

        except:
            pass

        # 상태 출력
        cv2.putText(image, msg, (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                  )

        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()