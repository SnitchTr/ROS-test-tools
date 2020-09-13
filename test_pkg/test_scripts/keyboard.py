#!/usr/bin/env python3

import rospy

# import the ROS String message type
from std_msgs.msg import UInt16
from std_msgs.msg import String
from std_msgs.msg import Empty

class KeyboardPublisherNode:
    def __init__(self):
        rospy.loginfo("Starting keyboard")

        # create a publisher object to send dat

        PUBLISH_RATE = 10.0 # 10 Hz
        # create a timer that calls the timer_callback function at
        # the specified rate
        rospy.Timer(rospy.Duration(1.0/PUBLISH_RATE), self.get_input)
        self.stable = False
    def get_input(self, event):
        # this function is called by the timer
        str = input('Enter message:')
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
            rospy.Publisher(self.topic, UInt16, queue_size=10).publish(num)

        # publish the string message
        except:
            rospy.loginfo(str)
            rospy.Publisher(self.topic, String, queue_size=10).publish(str)


if __name__ == "__main__":
    rospy.init_node("keyboard")
    node = KeyboardPublisherNode()
    rospy.spin()
