#!/usr/bin/env python
import rospy
import tf.msg
import time
from nav_msgs.msg import Odometry
import tf2_ros
import geometry_msgs.msg

def talker():
    br = tf.TransformBroadcaster()
    br.sendTransform((5, 5, 0),
                     tf.transformations.quaternion_from_euler(0, 0, 0),
                     rospy.Time.now(),
                     "turtlename",
                     "world")

if __name__ == '__main__':
    rospy.init_node('my_static_tf2_broadcaster')
    broadcaster = tf2_ros.StaticTransformBroadcaster()
    static_transformStamped = geometry_msgs.msg.TransformStamped()
  
    static_transformStamped.header.stamp = rospy.Time.now()
    static_transformStamped.header.frame_id = "world"
    static_transformStamped.child_frame_id = "a5"
  
    static_transformStamped.transform.translation.x = 5
    static_transformStamped.transform.translation.y = 4
    static_transformStamped.transform.translation.z = 0
  
    quat = tf.transformations.quaternion_from_euler(0,0,0)
    static_transformStamped.transform.rotation.x = quat[0]
    static_transformStamped.transform.rotation.y = quat[1]
    static_transformStamped.transform.rotation.z = quat[2]
    static_transformStamped.transform.rotation.w = quat[3]
 
    broadcaster.sendTransform(static_transformStamped)
    i = 0
    while(True):
        print("ahoj")
        i = i+1
        static_transformStamped.transform.translation.x = i
        broadcaster.sendTransform(static_transformStamped)
        time.sleep(2)