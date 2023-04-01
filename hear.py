#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from gtts import gTTS
import os

def callback(data):
    mytext = data.data
    language = 'en'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("welcome.mp3")    
    rospy.loginfo("%s",mytext)

def listener():
    # Initialize the ROS node
    rospy.init_node('listener', anonymous=True)

    # Set up the ROS subscriber for the topic
    rospy.Subscriber("chatter", String, callback)

    # Spin until the node is shutdown
    rospy.spin()

if __name__ == '__main__':
    listener()

