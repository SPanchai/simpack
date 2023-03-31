#!/usr/bin/env python3
import cv2
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from proj_state_smach.srv import truefalse, truefalseResponse
import numpy as np
from openpose import pyopenpose as op
import time
from sensor_msgs.msg import Image
import cv2
import mediapipe as mp
import math


class OpenCVROS(object):
    def __init__(self) -> None:
        rospy.init_node("opencv_ros", anonymous=True)
        self.img_sub = rospy.Subscriber("/camera/rgb/image_color", Image, callback = self.image_callback)
        self.find_lug = rospy.Service('honda_wave', truefalse, self.server_callback)
        self.pub = rospy.Publisher('image_topic', Image, queue_size=10)
        self.bridge = CvBridge()
        self.image = None
        self.res = truefalseResponse()
        rospy.loginfo("Waiting ")
    
    def image_callback(self, data):
        self.image = self.bridge.imgmsg_to_cv2(data, desired_encoding="bgr8")

    def server_callback(self, req):
        # Create a hands object
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

        # Define a variable to store the number of frames in which the hand is waving
        waving_frames = 0

        # Define a drawing object
        mp_drawing = mp.solutions.drawing_utils


        state = 0 
        count = 0



        while not rospy.is_shutdown():
            # Read frame from video capture
            img = self.image 
            
            # Convert the frame to RGB
            img_rgb = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
            
            # Detect hands in the frame
            results = hands.process(img_rgb)
            
            # Check if any hands are detected
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw the hand landmarks on the frame
                    mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    
                    # Get the index finger and middle finger landmarks
                    index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    middle_finger = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

                    # # Calculate the distance between the index finger and middle finger landmarks
                    
                    angle =  (180 / 3.141592) * math.atan2(middle_finger.y - wrist.y, middle_finger.x - wrist.x) + 180
                        # If the angle is greater than a threshold value, the hand is considered to be waving

                    cv2.putText(img, '{}'.format(angle), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                        
                    


                    if angle < 90 and state == 1:
                        state = 0
                        count += 1
                    elif angle  > 90 and state == 0:
                        state = 1
                        count += 1

                    if count > 4:
                        print("wave")
                        count = 0
                        cv2.putText(img, 'wave' ,(120, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                        self.res.success=True
                        return self.res
                        # break

                    else:
                        print("just Hand ")
                    cv2.putText(img, '{}'.format(count) ,(80, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    # distance = ((index_finger.x - middle_finger.x)**2 + (index_finger.y - middle_finger.y)**2)**0.5
                    
                    # Check if the hand is waving
                    # if distance > 0.1:
                    #     waving_frames += 1
                    #     if waving_frames > 5:  # if hand has been waving for more than 10 frames
                    #         print("Hand is waving!")
                    # else:
                    #     waving_frames = 0
                    #     print("just Hand ")
            else:
                print("no hand")
            # Display the frame
            # cv2.imshow("Image", img)
            cv_image=img
            ros_image = self.bridge.cv2_to_imgmsg(cv_image, encoding='bgr8')
            self.pub.publish(ros_image)

            # Check for key press and exit if 'q' is pressed
            # if cv2.waitKey(1) == ord('q'):
            #     break
        
        # return self.res

if __name__ == "__main__":
    opencv_ros = OpenCVROS()
    # opencv_ros.main()
    rospy.spin()