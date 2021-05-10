#!/usr/bin/env python3

import rospy
import numpy
class KeyboardPublisherNode:
    def __init__(self):
        rospy.loginfo("Starting keyboard")

        rospy.loginfo('Starting keyboard... \nFor intructions on how to use the keyboard node type "help"')
        self.supported_msgs=['Bool','Empty','String','ColorRGBA','Int8','Int16','Int32','Int64','UInt8','UInt16','UInt32','UInt64','Float32','Float64']#,'Int8MultiArray','Int16MultiArray','Int32MultiArray','Int64MultiArray','UInt8MultiArray','UInt16MultiArray','UInt32MultiArray','UInt64MultiArray','Float32MultiArray','Float64MultiArray']
        self.int_msgs=['Int16','Int32','Int64','Int8','UInt16','UInt32','UInt64','UInt8']
        self.float_msgs=['Float32','Float64']
        self.float_array_msgs=['Float32MultiArray','Float64MultiArray']
        self.int_array_msgs=['Int16MultiArray','Int32MultiArray','Int64MultiArray','Int8MultiArray','UInt16MultiArray','UInt32MultiArray','UInt64MultiArray','UInt8MultiArray']
        self.stable = False
        self.publishable = True

        PUBLISH_RATE = 10.0 #10hz
        rospy.Timer(rospy.Duration(1.0/PUBLISH_RATE), self.get_input)
    def get_input(self, event):
        if not self.stable:
            self.data = self.get_data()
            self.topic = self.get_topic()
        message = self.get_message(data=self.data)
        if self.publishable:
            info = 'Data:' + self.data + ' Topic:' + self.topic + ' Message:' + str(message)
            rospy.loginfo(info)
            rospy.Publisher(self.topic, self.imported, queue_size=10).publish(message)
        self.publishable = True

    def get_data(self):
        print("Now you'll be asked to enter a message type. If this is a part of the std_msgs pkg enter the message type direcly otherwise type "+'"other".If you want to keep the message type type "keep" first\nFor help on data types type "help"')
        while 1:
            data_type = input('Enter message type:')
            package = 'std_msgs.msg'
            if data_type == 'keep':
                self.stable = True
                continue
            if data_type == 'help':
                for type in self.supported_msgs:
                    print(type)
                print('For message definitions go to http://wiki.ros.org/std_msgs')
                continue
            if data_type == 'other':
                package = input('Enter pkg name where the msg is stored:') + '.msg'
                data_type = input('Enter message type:')
            if data_type in self.supported_msgs:
                self.imported = getattr(__import__ (package,fromlist=[data_type]),data_type)
                data = data_type
                return data
            else:
                print('Enter a valid type')
    def get_topic(self):
        print("Now you'll be asked to enter a topic to publish your message to."+'If you want to keep the topic type "keep" first')
        while 1:
            topic = input('Enter topic:')
            if topic == 'keep':
                self.stable = True
                continue
            else:
                return topic
    def get_message(self,data):
        while 1:
            if data in self.float_array_msgs or data in self.int_array_msgs:
                print("You'll be asked to enter a number to add to the array." + ' Type "done" when finished. The minimum amount of values on the array is 1')
            if data == 'Empty':
                print("The empty message doesn't contain any data so you can write whatever you can")
            if data == 'ColorRGBA':
                print("You'll be asked to enter 4 float values corresponding to the Red, Green, Blue and Alpha chanel values in this order")
            if data == 'Bool':
                print('For the Bool message write 0 for False and 1 for True')
            msg = input('Enter message:')
            if msg == 'change':
                self.stable = False
                self.publishable = False
                return
            if data == 'String':
                return msg
            if data in self.int_msgs:
                try:
                    num = int(msg)
                    return num
                except:
                    print('Enter a valid message')
            if data in self.float_msgs:
                try:
                    num = float(msg)
                    return num
                except:
                    print('Enter a valid message')
                    continue
            if data in self.float_array_msgs:
                x = [1]
                try:
                    inta = float(msg)
                except:
                    rospy.loginfo('Invalid number try again')
                    continue
                x.append(inta)
                while 1:
                    inp = input('Enter number:')
                    if inp == 'done':
                        return x
                    try:
                        inta = float(inp)
                    except:
                        rospy.loginfo('Invalid number try again')
                        continue
                    x.append(inta)
            if data in self.int_array_msgs:
                x = [1]
                try:
                    inta = int(msg)
                except:
                    rospy.loginfo('Invalid number try again')
                    continue
                x.append(inta)
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
            if data == 'Bool':
                if msg == '0' or msg== '1':
                    boolean = bool(int(msg))
                    return boolean
                else:
                    print('Enter a valid message')
                    continue
            if data == 'ColorRGBA':
                color = self.imported()
                try:
                    num = float(msg)
                except:
                    print('Enter a valid message')
                color.r = num
                msg = input('Enter message:')
                try:
                    num = float(msg)
                except:
                    print('Enter a valid message')
                color.g = num
                msg = input('Enter message:')
                try:
                    num = float(msg)
                except:
                    print('Enter a valid message')
                color.b = num
                msg = input('Enter message:')
                try:
                    num = float(msg)
                except:
                    print('Enter a valid message')
                color.a = num
                return color
            else:
                print('unexpected error not available data type and topic change it by typing "change"')
                continue
if __name__ == "__main__":
    rospy.init_node("keyboard")
    node = KeyboardPublisherNode()
    rospy.spin()
