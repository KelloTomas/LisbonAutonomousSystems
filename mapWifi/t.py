#!/usr/bin/env python  
from threading import Thread
import roslib

import rospy
import tf

def createNode(name, x, y):
    rospy.init_node(name+'node')
    br = tf.TransformBroadcaster()
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        br.sendTransform((x, y, 0.0),(0.0, 0.0, 0.0, 1.0),rospy.Time.now(),
                         "WifiBase",name)
        rate.sleep()

if __name__ == '__main__':
    rospy.init_node('node1')
    br1 = tf.TransformBroadcaster()
    br2 = tf.TransformBroadcaster()
    
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        br1.sendTransform((2.0, 3.0, 0.0),(0.0, 0.0, 0.0, 1.0),rospy.Time.now(),
                         "WifiBase","afsa")
        br2.sendTransform((2.0, 3.0, 0.0),(0.0, 0.0, 0.0, 1.0),rospy.Time.now(),
                         "WifiBase","afasdsa")
        rate.sleep()


