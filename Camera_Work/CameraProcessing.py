import cv2
import mediapipe as mp

# Funtion to detect jumps
def detect_jumps(landmarks, prev_left_foot_y, prev_right_foot_y, jump_threshold):
    left_foot_y = landmarks[28].y  # Adjust landmark IDs if needed
    right_foot_y = landmarks[29].y  # Adjust landmark IDs if needed

    if prev_left_foot_y is not None and prev_right_foot_y is not None:
        # Calculate the vertical movement of both feet
        left_foot_move = left_foot_y - prev_left_foot_y
        right_foot_move = right_foot_y - prev_right_foot_y

        if left_foot_move > jump_threshold and right_foot_move > jump_threshold:
            return True  # Jump detected

    return False  # Jump not detected

# Function to detect walks
def detect_walks(landmarks, prev_left_foot_y, prev_right_foot_y, walk_threshold):
    left_foot_y = landmarks[28].y  # Adjust landmark IDs if needed
    right_foot_y = landmarks[29].y  # Adjust landmark IDs if needed

    if prev_left_foot_y is not None and prev_right_foot_y is not None:
        # Calculate the vertical movement of both feet
        left_foot_move = left_foot_y - prev_left_foot_y
        right_foot_move = right_foot_y - prev_right_foot_y

        # Define a threshold for detecting walking (you can adjust this value)
        if abs(left_foot_move) > walk_threshold or abs(right_foot_move) > walk_threshold:
            return True  # Walking detected
        
    return False

def display_camera():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    cap = cv2.VideoCapture(0)

    # Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        prev_left_foot_y = None  # Initialize previous left foot position
        prev_right_foot_y = None  # Initialize previous right foot position
        jump_detected = False  # Initialize jump detection flag
        walking_detected = False  # Initialize walking detection flag

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

                # Define a threshold for detecting a jump 
                jump_threshold = 0.06  # Adjust based on sensitivity

                # Define a threshold for detecting walking in place
                walk_threshold = 0.03  # Adjust based on sensitivity

                # Detect Jumps
                if detect_jumps(landmarks, prev_left_foot_y, prev_right_foot_y, jump_threshold):
                    if not jump_detected:
                        print("Jump")
                        jump_detected = True
                else:
                    jump_detected = False

                # Detect Walking   
                if not jump_detected:
                    if detect_walks(landmarks, prev_left_foot_y, prev_right_foot_y, walk_threshold):
                        if not walking_detected:
                            print("Walking")
                            walking_detected = True
                    else:
                        walking_detected = False

                # Updating previous position
                prev_left_foot_y = landmarks[28].y
                prev_right_foot_y = landmarks[29].y

            except:
                pass

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

if __name__ == '__main__':
    display_camera()
