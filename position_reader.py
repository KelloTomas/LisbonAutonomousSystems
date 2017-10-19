#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry

def callback(data):
    print("\n\r\n\rPosition")
    print(data.pose.pose.position.x)
    print(data.pose.pose.position.y)
    print("Orientation")
    print(data.pose.pose.orientation.z)
    print(data.pose.pose.orientation.w)

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/RosAria/pose", Odometry, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
