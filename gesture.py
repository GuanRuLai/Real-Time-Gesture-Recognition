import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands 
mp_drawing = mp.solutions.drawing_utils 
mp_drawing_styles = mp.solutions.drawing_styles

# define a fuction to calculate the angle based on the coordinates of two points
def vector_2d_angle(v1, v2):
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    try:
        # calculate the angle between two vectors and convert the result from radians to degrees
        angle_= math.degrees(math.acos((v1_x * v2_x + v1_y * v2_y) / (((v1_x ** 2 + v1_y ** 2) ** 0.5) * ((v2_x ** 2 + v2_y ** 2) ** 0.5))))
    except:
        angle_ = 180
    return angle_
    
# define a function to get the angle of the finger based on the 21 node coordinates passed in
def hand_angle(hand_):
    angle_list = []
    # thumb angle
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[2][0])), (int(hand_[0][1]) - int(hand_[2][1]))),
        ((int(hand_[3][0]) - int(hand_[4][0])), (int(hand_[3][1]) - int(hand_[4][1])))
        )
    angle_list.append(angle_)
    # index angle
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[6][0])), (int(hand_[0][1]) - int(hand_[6][1]))),
        ((int(hand_[7][0]) - int(hand_[8][0])), (int(hand_[7][1]) - int(hand_[8][1])))
        )
    angle_list.append(angle_)
    # middle angle
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[10][0])), (int(hand_[0][1]) - int(hand_[10][1]))),
        ((int(hand_[11][0]) - int(hand_[12][0])), (int(hand_[11][1]) - int(hand_[12][1])))
        )
    angle_list.append(angle_)
    # ring angle
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[14][0])), (int(hand_[0][1]) - int(hand_[14][1]))),
        ((int(hand_[15][0]) - int(hand_[16][0])), (int(hand_[15][1]) - int(hand_[16][1])))
        )
    angle_list.append(angle_)
    # pink angle
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[18][0])), (int(hand_[0][1]) - int(hand_[18][1]))),
        ((int(hand_[19][0]) - int(hand_[20][0])), (int(hand_[19][1]) - int(hand_[20][1])))
        )
    angle_list.append(angle_)
    return angle_list   
    
# define a function to return the corresponding gesture name based on the list of the finger angle
def hand_pos(finger_angle):
    f1 = finger_angle[0] # thumb angle
    f2 = finger_angle[1] # index angle  
    f3 = finger_angle[2] # middle angle  
    f4 = finger_angle[3] # ring angle  
    f5 = finger_angle[4] # pink angle 

    # Angle > 50 means the fingers are straight, and <= 50 means the fingers are curled.
    if f1 < 50 and f2 >= 50 and f3 >= 50 and f4 >= 50 and f5 >= 50:
        return "good"
    elif f1 >= 50 and f2 >= 50 and f3 < 50 and f4 >= 50 and f5 >= 50:
        return "no!!!"
    elif f1 < 50 and f2 < 50 and f3 >= 50 and f4 >= 50 and f5 < 50:
        return "ROCK!"
    elif f1 >= 50 and f2 >= 50 and f3 >= 50 and f4 >= 50 and f5 >= 50:
        return "0"
    elif f1 >= 50 and f2 >= 50 and f3 >= 50 and f4 >= 50 and f5 < 50:
        return "weak"
    elif f1 >= 50 and f2 < 50 and f3 >= 50 and f4 >= 50 and f5 >= 50:
        return "1"
    elif f1 >= 50 and f2 < 50 and f3 < 50 and f4 >= 50 and f5 >= 50:
        return "2"
    elif f1 >= 50 and f2 >= 50 and f3 < 50 and f4 < 50 and f5 < 50:
        return "ok"
    elif f1 < 50 and f2 >= 50 and f3 < 50 and f4 < 50 and f5 < 50:
        return "ok"
    elif f1 >= 50 and f2 < 50 and f3 < 50 and f4 < 50 and f5 > 50:
        return "3"
    elif f1 >= 50 and f2 < 50 and f3 < 50 and f4 < 50 and f5 < 50:
        return "4"
    elif f1 < 50 and f2 < 50 and f3 < 50 and f4 < 50 and f5 < 50:
        return "5"
    elif f1 < 50 and f2 >= 50 and f3 >= 50 and f4 >= 50 and f5 < 50:
        return "6"
    elif f1 < 50 and f2 < 50 and f3 >= 50 and f4 >= 50 and f5 >= 50:
        return "7"
    elif f1 < 50 and f2 < 50 and f3 < 50 and f4 >= 50 and f5 >= 50:
        return "8"
    elif f1 < 50 and f2 < 50 and f3 < 50 and f4 < 50 and f5 >= 50:
        return "9"
    else:
        return ""
        
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)          
fontFace = cv2.FONT_HERSHEY_SIMPLEX  
lineType = cv2.LINE_AA              

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:    
    
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
        
    w, h = 540, 310
        
    while True:
        ret, img = cap.read()
        img = cv2.resize(img, (w, h)) 
        if not ret:
            print("Cannot receive frame")
            break      
            
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img2)  

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                finger_points = [] # record the finger node coordinates                 
                for i in hand_landmarks.landmark:
                    # convert 21 nodes into coordinates and record them to the list
                    x = i.x * w
                    y = i.y * h
                    finger_points.append((x, y))
                
                if finger_points:
                    finger_angle = hand_angle(finger_points) # calculate the finger angle and return a list 
                    # print(finger_angle)                     
                    text = hand_pos(finger_angle) # get corresponding gesture          
                    cv2.putText(img, text, (30, 120), fontFace, 5, (0, 0, 0), 10, lineType) 
                    			  
            cv2.imshow("Gesture result", img)
            if cv2.waitKey(5) == ord("q"):
                break   

cap.release()
cv2.destroyAllWindows() 
