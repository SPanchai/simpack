#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class TurtleBot:
    def __init__(self):
        rospy.init_node('turtlebot_subscriber')
        self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.cmd_vel = Twist()

        # Subscribe to the topic where the words are published
        rospy.Subscriber('turtlebot_words', String, self.words_callback)

        # Subscribe to the laser scan topic to detect obstacles
        rospy.Subscriber('scan', LaserScan, self.laser_callback)

        # Initialize the rotation state and obstacle state of the robot
        self.rotation_done = True
        self.obstacle_detected = False

    def words_callback(self, data):
        # Check if the word is "run"
        if data.data == 'run':
            # Set the linear speed of the robot to maximum
            self.cmd_vel.linear.x = 0.5  # Maximum linear speed is 0.5 m/s
            self.cmd_vel.linear.y = 0
            self.cmd_vel.linear.z = 0

            # Set the angular speed of the robot to zero
            self.cmd_vel.angular.x = 0
            self.cmd_vel.angular.y = 0
            self.cmd_vel.angular.z = 0

            # Reset the rotation state and obstacle state of the robot
            self.rotation_done = True
            self.obstacle_detected = False

        # Publish the velocity command to move the robot forward
        self.velocity_publisher.publish(self.cmd_vel)

    def laser_callback(self, data):
        # Check if an obstacle is detected within a certain range
        obstacle_range = 0.5  # Set the maximum range to detect an obstacle
        if min(data.ranges) < obstacle_range:
            # Stop the robot and set the obstacle state to true
            self.cmd_vel.linear.x = 0
            self.velocity_publisher.publish(self.cmd_vel)
            self.obstacle_detected = True

    def run(self):
        # Start the ROS spin loop
        while not rospy.is_shutdown():
            # Check if the robot has detected an obstacle
            if self.obstacle_detected:
                # Rotate the robot 180 degrees and set the obstacle state to false
                self.cmd_vel.angular.z = 1.57  # 180 degrees is pi radians
                self.velocity_publisher.publish(self.cmd_vel)
                self.obstacle_detected = False

            # Check if the robot is moving forward
            if self.cmd_vel.linear.x > 0:
                # Check if the robot has completed its rotation
                if self.cmd_vel.angular.z != 0:
                    self.cmd_vel.angular.z = 0
                    self.rotation_done = True

                # Check if the robot has detected an obstacle
                if not self.obstacle_detected:
                    # Publish the velocity command to move the robot forward
                    self.velocity_publisher.publish(self.cmd_vel)

if __name__ == '__main__':
    try:
        bot = TurtleBot()
        bot.run()
    except rospy.ROSInterruptException:
        pass

