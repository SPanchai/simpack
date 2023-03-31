#! /usr/bin/env python3

import roslib
roslib.load_manifest('skuba_ahr_speechprocessing')
import rospy
import actionlib
from vosk import Model, KaldiRecognizer
import pyaudio
import json
from skuba_ahr_msgs.msg import ListenActionCommandAction, ListenActionCommandResult, ListenActionCommandFeedback 

class STTServer:


    def __init__(self):
        self.server = actionlib.SimpleActionServer('/basil/speech/listen_action', ListenActionCommandAction, self.execute, False)
        self.server.start()
        self._result = ListenActionCommandResult()
        self._feedback=ListenActionCommandFeedback()
        self.Pid= None
        rospy.loginfo("Waiting ")
        
    
    #compare string that hear and string that want to detect
    def compare_strings(self, long_string, substrings):
        for sub in substrings:
            if sub in long_string:

                return sub
            
        return False


    def execute(self, goal):
        input_list = goal.sentence
        input_string=""
        
        #select your language vvv
        model = Model(lang="en-us")
        rec=KaldiRecognizer(model,16000)
        cap=pyaudio.PyAudio()
        stream=cap.open(format=pyaudio.paInt16,channels=1, rate=16000,input=True ,frames_per_buffer=8192)
        stream.start_stream()
        
        while not rospy.is_shutdown():
            data=stream.read(4096)
            if len(data) == 0:
                break

            if rec.AcceptWaveform(data):
                #print what hearing
                input_string=json.loads(rec.Result())['text']
                print(input_string)
                self._feedback.sentence_received=input_string
                self.server.publish_feedback(self._feedback)
                
            #chack matching words
            check = self.compare_strings(input_string, input_list)
            print(check)
            
            if check:
                print("Match found!")
                self._result.success=True
                self._result.sentence=str(check)
                rospy.loginfo("goal succeeded")
                self.server.set_succeeded(self._result)
                break

            else:
                print("Match not found.")


            if self.server.is_preempt_requested():
                self.server.set_preempted()
                rospy.loginfo("set_preempted")
                break


if __name__ == '__main__':
  rospy.init_node('STT_server')
  server = STTServer()
  rospy.spin()


