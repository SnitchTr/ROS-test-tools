#!/usr/bin/env python3

import rospy
import numpy

# import the ROS String message type
from std_msgs.msg import Int8
from std_msgs.msg import String
from std_msgs.msg import Empty
from test_msgs.msg import test

class KeyboardPublisherNode:
    def __init__(self):
        rospy.loginfo("Starting keyboard")

        # create a publisher object to send dat

        PUBLISH_RATE = 10.0 # 10 Hz
        # create a timer that calls the timer_callback function at
        # the specified rate
        rospy.Timer(rospy.Duration(1.0/PUBLISH_RATE), self.get_input)
        self.stable = False
        self.array = False
    def get_input(self, event):
        # this function is called by the timer
        str = input('Enter message:')
        if str == 'instructions':
            instructions = test()
            self.topic = 'instructions'
            rospy.loginfo('now you will be asked for directions(0 stop,1 foward,2 back,3 right,4 left) type "done" when finished')
            instructions.direction = self.get_array();
            rospy.loginfo('now you will be asked for distance in mm of the directions type "done" when finished')
            instructions.distance = self.get_array();
            rospy.Publisher(self.topic, test, queue_size=10).publish(instructions)
            return
        if str == 'empty':
            self.topic = input('Enter topic:')
            rospy.Publisher(self.topic, Empty, queue_size=10).publish()
            return

        if str == 'change':
            self.stable = False
            str = input('Enter message:')
        if self.stable == False:
            self.topic = input('Enter topic:')
            if self.topic == 'keep':
                self.topic = input('this will make the topic unchangable write "cancel" to cancel: ')
                if self.topic == 'cancel':
                    self.topic = input('Enter topic:')
                else:
                    self.stable = True
        # loginfo to print the string to the terminal
        try:
            num = int(str)
            rospy.loginfo(num)
            rospy.Publisher(self.topic, Int8, queue_size=10).publish(num)

        # publish the string message
        except:
            rospy.loginfo(str)
            rospy.Publisher(self.topic, String, queue_size=10).publish(str)

    def get_array(self):
        x = [1]
        while 1:
            inp = input('Enter number:')
            if inp == 'done':
                return x
            try:
                inta = int(inp)
            except:
                rospy.loginfo('Invalid number try again')
                continue
            x.append(inta)

if __name__ == "__main__":
    rospy.init_node("keyboard")
    node = KeyboardPublisherNode()
    rospy.spin()
