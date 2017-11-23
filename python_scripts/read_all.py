#!/usr/bin/env python
import rospy
import tf.msg
from nav_msgs.msg import Odometry

def callbackTF(data):
    t = data.transforms[0].transform
    print("\n\nTF Position\n" + str(t.translation.x) + "\n" + str(t.translation.y) + "\nTF Orientation\n" + str(t.rotation.z) + "\n" + str(t.rotation.w))

def callbackPose(data):
    d = data.pose.pose
    print("\n\nPose Position\n" + str(d.position.x) + "\n" + str(d.position.y) + "\nPose Orientation\n" + str(d.orientation.z) + "\n" + str(d.orientation.w))

def listener():

    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/tf", tf.msg.tfMessage, callbackTF)
    rospy.Subscriber("/RosAria/pose", Odometry, callbackPose)
    rospy.spin()

if __name__ == '__main__':
    listener()

