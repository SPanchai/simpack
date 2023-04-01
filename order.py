#!/usr/bin/env python3

import rospy
import time
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from gtts import gTTS
import os


class TurtleBot:
    def __init__(self):
        rospy.init_node('turtlebot_subscriber')
        self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.cmd_vel = Twist()
        
        rospy.Subscriber('chatter', String, self.words_callback)
        
        
    def words_callback(self, data):
        # Check if the word is "run"
        
        self.cmd_vel.linear.x = 0
        mytext = data.data       

        if mytext == 'order':
            # Set the linear speed of the robot to maximum
            self.cmd_vel.linear.x = 0.2  # linear speed is 0.2 m/s
            # Set the angular speed of the robot to zero
            self.cmd_vel.angular.z = 0
            mytext = "What's order"
            
            
            
            
        elif mytext != 'order':
            # Set the linear speed of the robot to maximum
            self.cmd_vel.linear.x = -0.2  # linear speed is 0.2 m/s
            # Set the angular speed of the robot to zero
            self.cmd_vel.angular.z = 0            
        language = 'en'
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("welcome.mp3")      
        
           
            


    def run(self):
    	while not rospy.is_shutdown():
	    	start_time = rospy.Time.now()
	    	cv = self.velocity_publisher.publish(self.cmd_vel)   	
	   	
	    	if cv != 0:	    	   	
	    		while (rospy.Time.now() - start_time).to_sec() < 5.0:
	    			self.velocity_publisher.publish(self.cmd_vel)
	    		self.cmd_vel.linear.x = 0
	    		self.velocity_publisher.publish(self.cmd_vel)
	    		
	    	os.system("mpg123 welcome.mp3")
	    		
	    		



if __name__ == '__main__':
    try:
        bot = TurtleBot()
        bot.run()
    except rospy.ROSInterruptException:
        pass

