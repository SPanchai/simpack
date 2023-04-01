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
	
	#sending a speed value to bot
        self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.cmd_vel = Twist()
        
	#getting an word from topic
        rospy.Subscriber('chatter', String, self.words_callback)
        
        
    def words_callback(self, data):       
        
	#Reset speed, force to stop
        self.cmd_vel.linear.x = 0
	
	#getting an word from topic
        mytext = data.data       

        if mytext == 'order':
            # check if user call for ordering menu
	
            self.cmd_vel.linear.x = 0.2
            self.cmd_vel.angular.z = 0	
            mytext = "What's order"
            # setting speed and word for condition 1 go to table       
                                    
        elif mytext != 'order':
            # check what user order
            self.cmd_vel.linear.x = -0.2
            self.cmd_vel.angular.z = 0 
            # setting speed and word for condition 2 go back to cashier     
        language = 'en'
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("welcome.mp3")
	#save text to sound
        
           
            


    def run(self):
    	while not rospy.is_shutdown():
		
	    	start_time = rospy.Time.now()
	    	cv = self.velocity_publisher.publish(self.cmd_vel) 	
	   	
	    	if cv != 0:
		#check currents velocity, checking bot is moving	    	   	
	    		while (rospy.Time.now() - start_time).to_sec() < 5.0:
	    			self.velocity_publisher.publish(self.cmd_vel)
			#sending speed to move for 5 seconds
			
	    		self.cmd_vel.linear.x = 0
	    		self.velocity_publisher.publish(self.cmd_vel)
	    		#stop bot
	    	os.system("mpg123 welcome.mp3")
		#play last getting sound   		
	    		


if __name__ == '__main__':
    try:
        bot = TurtleBot()
        bot.run()
    except rospy.ROSInterruptException:
        pass

