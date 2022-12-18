import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

#거북목 정도 변수
turtle = None

#어깨 틀어짐 정도 변수
twist = None

#라운드숄더 변수
roundshoulder = None


cap = cv2.VideoCapture(0)


# 선의 중점과 점의 거리
def lineDistance(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    linedist = np.linalg.norm(c - b) #점 b와 c사이의 거리
    center = [(b[0] - c[0]) / 2, b[1] - c[1] / 2] # b와 c의 중점

    dist = np.linalg.norm(center - a) #b와 c의 중점과 a의 거리

    return dist


# 두점의 거리
def dotDistance(a, b):
    a = np.array(a)
    b = np.array(b)

    dist = np.linalg.norm(b - a) # 점 a와 b사이의 거리

    return dist


# 어깨의 틀어진 각도
def shouderAngle(a, b):
    a = np.array(a)
    b = np.array(b)

    radians = np.arctan2(a[1] - b[1], a[0] - b[0]) # 선 a,b의 각도 라디안 값
    angle = np.abs(radians * 180.0 / np.pi) # 라디안 값에서 도로 변환

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
            #코 좌표 받기
            nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x,
                    landmarks[mp_pose.PoseLandmark.NOSE.value].y]
            #왼쪽 어깨 좌표 받기
            left = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

            #오른쪽 어깨 좌표 받기
            right = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]



            # 어깨너비
            dist_sh = dotDistance(left, right)

            l_y = left[1]
            r_y = right[1]

            # 어깨사이의 거리
            round = dotDistance(left, right)

            # 어깨 틀어진 정도
            angle = shouderAngle(left, right)

            #초기값 입력
            if cv2.waitKey(10) & 0xFF == ord('r'):

                #어깨너비 초기값
                init_sh = dist_sh
                init_ly = l_y
                init_ry = r_y

                # #입술 너비 초기값
                # init_mouth = dist_mouth


            rate_sh = dist_sh / init_sh

            # Curl counter logic
            if rate_sh>1 and init_ly < l_y and init_ry < r_y:
                turtle = "Turtle O"
            elif init_ly < l_y and init_ry < r_y and rate_sh <= 1:
                turtle = "Round and Turtle"
            else:
                turtle = "Turtle X"
            if angle > 10:
                twist = "Twist O"
            else:
                twist = "Twist X"



        except:
            pass

        # 상태 출력
        cv2.putText(image, turtle,
                    (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, twist,
                    (10, 160),
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