#!/usr/bin/env python
import rospy
import tf.msg
import subprocess
import time
import sys

from nav_msgs.msg import Odometry

wifis = dict()
x = 0
y = 0

def ReadWifi():
	wifi = dict()
	data = subprocess.check_output("sudo iwlist wlp2s0 scan | grep -oP '(Address: |Signal level=)\K\S*'", shell=True)
	key = ""
	for line in data.splitlines():
		if(key == ""):
			key = line
		else:
			wifi[key] = line
			key = ""
	return wifi

def callbackPose(data):
	d = data.pose.pose
	global y
	global x
	x = d.position.x
	y = d.position.y
	return x
	return y
	#print("\n\nPose Position\n" + str(d.position.x) + "\n" + str(d.position.y) + "\nPose Orientation\n" + str(d.orientation.z) + "\n" + str(d.orientation.w))

def listener():

	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber("/RosAria/pose", Odometry, callbackPose)
	#rospy.spin()

def GetAvgWifi():
	count = 0
	while True:
	        time.sleep(2)
		if count == 5:
			return
		print("reading " + str(count)+"\n")
		try:
			w = ReadWifi()
		except:
			continue
	
		for key, value in w.iteritems():

			if key not in wifis:
				wifis[key] = list()
			wifis[key].append(value)
		count += 1

if __name__ == '__main__':
	if (len(sys.argv) != 2):
		print("Define filename as argument")
		exit()
	listener()
	GetAvgWifi()
	wFile = open(sys.argv[1],"w")
	wFile.write("NEXT\n")
	wFile.write(str(x) + "," + str(y)+"\n")
	for key, value in wifis.iteritems():
		s = 0.0
		for v in value:
			s = s+float(v)
		wFile.write(key + " " + str(s/len(value)) + "\n")
	wFile.write("END\n")

