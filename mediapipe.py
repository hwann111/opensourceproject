import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

turtle = None
twist = None
roundshoulder = None
cap = cv2.VideoCapture(0)

#선의 중점과 점의 거리
def lineDistance(a,b,c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    
    linedist = np.linalg.norm(c - b)
    line = [(b[0]-c[0])/2,b[1]-c[1]/2]

    dist = np.linalg.norm(line-a)

    return dist
#두점의 거리
def dotDistance(a,b):
    a = np.array(a)
    b = np.array(b)

    dist = np.linalg.norm(b-a)

    return dist


#어깨의 틀어진 각도
def shouderAngle(a,b):
    a = np.array(a)
    b = np.array(b)

    radians = np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

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
            nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x,
                    landmarks[mp_pose.PoseLandmark.NOSE.value].y]
            left = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            right = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            lmouth = [landmarks[mp_pose.PoseLandmark.MOUTH_LEFT.value].x,
                          landmarks[mp_pose.PoseLandmark.MOUTH_LEFT.value].y]
            rmouth = [landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT.value].x,
                          landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT.value].y]

            #코와 어깨의 거리
            dist_sh= lineDistance(nose,left,right)
            #코와 입술사이의 거리
            dist_mouth = lineDistance(nose,lmouth,rmouth)

            dist = dist_sh/dist_mouth




            #어깨사이의 거리
            round = dotDistance(left,right)

            #어깨 틀어진 정도
            angle = shouderAngle(left,right)




            #수치 출력
            cv2.putText(image, str(dist),
                        (200, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.putText(image, str(int(angle)),
                        (200, 160),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.putText(image, str(round),
                        (200, 260),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.putText(image, str(dist_mouth),
                        (200, 360),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)




            # Curl counter logic
            if dist >0.32:
                turtle = "Turtle"
            else:
                turtle = "Good"

            if angle > 10:
                twist = "Twist"
            else:
                twist = "Good"



        except:
            pass

        #상태 출력
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