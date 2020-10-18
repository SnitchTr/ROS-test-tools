#!/usr/bin/env python3
import rospy
# import our new fizzbuzz message type
from std_msgs.msg import Float32
from test_msgs.msg import test
from std_msgs.msg import Empty
from std_msgs.msg import Int8

class MotorDriverNode:
    def __init__(self):
        rospy.loginfo("Starting Motor Driver")
        self.step = 0
        # create a publisher object to send dat

        PUBLISH_RATE = 10.0 # 10 Hz
        # create a timer that calls the timer_callback function at
        # the specified rate
        self.arduino = rospy.Publisher("dir", Int8, queue_size=10)
        rospy.Subscriber("distance", Float32, self.finish_check)
        rospy.Subscriber("instructions", test, self.get_instructions)
        rospy.Subscriber("emergency",Empty,self.emergency_stop)
    def get_instructions(self, msg):
        self.step = 0
        self.stop = False
        self.directions = msg.direction
        self.distance_to_compleat = msg.distance
        arduino_msg = self.directions[self.step]
        self.arduino.publish(arduino_msg)
        rospy.loginfo(arduino_msg)
    def finish_check(self,msg):
        if self.stop == False:
            if msg.data >= self.distance_to_compleat[self.step]:
                self.step = self.step + 1
            arduino_msg = self.directions[self.step]
            self.arduino.publish(arduino_msg)
    def emergency_stop(self, event):
        self.arduino.publish(0)
        self.stop = True

if __name__ == "__main__":
    rospy.init_node("motordriver")
    node = MotorDriverNode()
    rospy.spin()
