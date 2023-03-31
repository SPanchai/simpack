#!/usr/bin/env python3
import roslaunch
import rospy
import smach
import smach_ros
import actionlib
from std_srvs.srv import *
from skuba_ahr_msgs.msg import *
from skuba_ahr_msgs.srv import *
from proj_state_smach.srv import *
# from your_smach.srv import GoToPosition, GoToPositionRequest

class find_wave_hand(smach.State):
    def __init__(self, outcomes=['found', 'fail']):
        super().__init__(outcomes)
        self.find_wave_hand = rospy.ServiceProxy('honda_wave', truefalse )
    
    def execute(self, ud):
        rospy.loginfo("Executing state find_wave_hand")

        req= truefalseRequest()
        req.action = True

        self.find_wave_hand(req)
        result = self.find_wave_hand()
        
        print(result)
        
        if result.success == True:
            return 'found'

class follow_and_listen(smach.State):
    def __init__(self, outcomes=['success', 'fail']):
        super().__init__(outcomes)
        # self.following = rospy.ServiceProxy('follow', follow_Command)
        
        # self.listening = actionlib.SimpleActionClient('/basil/speech/listen_action',ListenCommand)
        self.listen_sentence = ListenActionCommandGoal(["stop"])
        self.listen_result = ListenActionCommandResult()
        self.listen_client = actionlib.SimpleActionClient('/basil/speech/listen_action', ListenActionCommandAction)
        self.listen_result.success  = False

    def callback_done(self, state, result):
        self.listen_result = result
        rospy.logdebug("Action server is done. State: %s, result: %s" % (str(state), str(result)))

    def callback_feedback(self, feedback):
        rospy.logdebug("Feedback:%s" % str(feedback))
    
    def execute(self, ud):
        # self.listen_result = ListenActionCommandResult()
        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        roslaunch.configure_logging(uuid)
        follower = roslaunch.parent.ROSLaunchParent(uuid, ["/home/okmee/skuba_ws/src/turtlebot_apps/turtlebot_follower/launch/follower.launch"])
        follower.start()

        self.listen_client.send_goal(self.listen_sentence,
                    feedback_cb=self.callback_feedback,
                    done_cb=self.callback_done)
        
        # while not rospy.is_shutdown() and self.listen_result.success == False:
        while self.listen_result.success == False:
                # self.listen_client.cancel_all_goals()
                if self.listen_result.success == True:
                    break
            

        print("ohm")
        print(self.listen_result)
        if self.listen_result.success == True:
            follower.shutdown()
            return 'success'

        # print("kuy")
        # return 'success' 

class RobotState(object):
    def __init__(self) -> None:
        rospy.init_node('robot_state', anonymous=True)
        sm = smach.StateMachine(outcomes=['---finish---'])

        with sm:
            smach.StateMachine.add('find_wave_hand', find_wave_hand(), 
                               transitions={'found':'follow_and_listen', 'fail':'find_wave_hand'})
            # smach.StateMachine.add('Gotoposition', GoToPosition(), 
            #                     transitions={'success':'DoSth2', 'fail':'Gotoposition'})
            smach.StateMachine.add('follow_and_listen', follow_and_listen(), 
                               transitions={'success':'---finish---', 'fail':'follow_and_listen'})
        outcome = sm.execute()

if __name__ == "__main__":
    RobotState()