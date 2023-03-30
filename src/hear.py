#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

def listener():
    # Initialize the ROS node
    rospy.init_node('listener', anonymous=True)

    # Set up the ROS subscriber for the topic
    rospy.Subscriber("chatter", String, callback)

    # Spin until the node is shutdown
    rospy.spin()

if __name__ == '__main__':
    listener()

