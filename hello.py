#!/usr/bin/env python

import rospy
import speech_recognition as sr
from std_msgs.msg import String

class SpeechToText:
    def __init__(self):
        rospy.init_node('talker',anonymous=True)

        # Create a publisher to publish the speech to text conversion
        self.pub = rospy.Publisher('chatter', String, queue_size=10)
        

        # Initialize the speech recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def run(self):
        # Start the ROS spin loop
        while not rospy.is_shutdown():
            with self.microphone as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source)

                # Listen for speech
                audio = self.recognizer.listen(source)

                # Convert speech to text using Google Speech Recognition
                try:
                    text = self.recognizer.recognize_google(audio)
                    # Publish the speech to text conversion to the topic
                    self.pub.publish(text)
                except sr.UnknownValueError:
                    rospy.logwarn("Speech recognition could not understand audio")
                except sr.RequestError as e:
                    rospy.logwarn("Could not request results from Google Speech Recognition service; {0}".format(e))

if __name__ == '__main__':
    try:
        stt = SpeechToText()
        stt.run()
    except rospy.ROSInterruptException:
        pass

