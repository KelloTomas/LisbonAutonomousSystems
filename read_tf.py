#!/usr/bin/env python
import rospy
import tf.msg

def callback(data):
    t = data.transforms[0].transform
    print("\n\r\n\rPosition")
    print(t.translation.x)
    print(t.translation.y)
    print("Orientation")
    print(t.rotation.z)
    print(t.rotation.w)

def listener():

    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/tf", tf.msg.tfMessage, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
