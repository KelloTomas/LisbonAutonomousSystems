#----------------------------------------------------#
#             Kalman filter 3.0
#
#
#----------------------------------------------------#
import math
from numpy import identity
from numpy import array
from numpy import vstack
from numpy import random
import numpy as np
from zconvert import zconverter
import sys
import time
import rospy
import tf.msg
import time
from nav_msgs.msg import Odometry
import tf2_ros
import geometry_msgs.msg
import subprocess 
from thread import start_new_thread

from ekfilter import ekf
from jacobmat import jacobmat

import matplotlib.pyplot as plt
ReadFromFile = False
ReadFromFile2 = True
ReadOdometry = False
robotX = 0
robotY = 0
def callbackPose(data):
  d = data.pose.pose
  global robotY
  global robotX
  robotX = d.position.x
  robotY = d.position.y
  return robotX
  return robotY
  #print("\n\nPose Position\n" + str(d.position.x) + "\n" + str(d.position.y) + "\nPose Orientation\n" + str(d.orientation.z) + "\n" + str(d.orientation.w))

def listener():
  #rospy.init_node('listener', anonymous=True)
  rospy.Subscriber("/RosAria/pose", Odometry, callbackPose)
  #rospy.spin()


#h = lambda x: np.array([[0.75*x[0,0]]])
#f = lambda x: np.array([[x[0,0] * np.cos(x[0,0]*2*pi/N)+2], [x[1,0] * np.cos(x[1,0]*2*pi/N)+2 ]])

#h = lambda x: np.array([[0.75*x[0,0]]]);
#f = lambda x: np.array([[x[0,0] + 1], [x[1,0] + 1]]);

#h = lambda x: np.array([[x[0,0]]]);
#f = lambda x: np.array([[x[0,0] +3/N], [x[1,0] + 3/N]]);

def ReadWifi2(rFile):
  if (ReadFromFile2):
    wifi = dict()
    robotod = dict()
    if (rFile.readline() != "NEXT\n"):
      return wifi, robotod
    robotod = rFile.readline().split(',')
    while(True):
      data = rFile.readline().split()
      if (len(data) == 0):
        return wifi, robotod
      if (len(data) == 1):
        return wifi, robotod
      wifi[data[0]] = data[1]


def ReadWifi():
  if (ReadFromFile):
    rFile = open('signal2.txt','r')
    wifi = dict()
    if (rFile.readline() != "NEXT\n"):
      return wifi
    while(True):
      data = rFile.readline().split()
      if (len(data) == 1):
        return wifi
      if(len(data) == 0):
        return wifi
      wifi[data[0]] = data[1]
  else:
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


def RunCommand(command):
    subprocess.call(command, shell=True)

h = lambda x,odom: np.array([[x[0,0]], [x[1,0]]]);
f = lambda x,odom: np.array([[x[0,0]+odom[0,0]], [x[1,0]+odom[1,0]]]);


def rand_norm():
  t = random.standard_normal([1,]);
  return t

n = 2; # dimension (x and y = 2)
                    #number of state
q = 1;                 #standard deviation of the process 
r = 2;                 #standard deviation of the measurement
Q = q**2 * identity(n);   #covariance of the process
R = r**2; 
               #covariance of the measurement  
P = identity(n);            # initial state covraiance
pi = math.pi;

#-----------------------------------------------------------------#
#   Creating the dataset and measurement

s = np.zeros((2,1));

delta = np.zeros((2,1));
odom = np.zeros((2,1));
x = np.array([[14.366],[0.374]]);


#init transform
rospy.init_node('my_static_broadcast')
broadcaster = tf2_ros.StaticTransformBroadcaster()
static_transformStamped = geometry_msgs.msg.TransformStamped()
static_transformStamped.header.stamp = rospy.Time.now()
static_transformStamped.header.frame_id = "wifi_base"
static_transformStamped.child_frame_id = "odom"
static_transformStamped.transform.translation.x = 0
static_transformStamped.transform.translation.y = 0
static_transformStamped.transform.translation.z = 0
quat = tf.transformations.quaternion_from_euler(0,0,0)
static_transformStamped.transform.rotation.x = quat[0]
static_transformStamped.transform.rotation.y = quat[1]
static_transformStamped.transform.rotation.z = quat[2]
static_transformStamped.transform.rotation.w = quat[3]

# PUBLIS MAP to RVIZ
start_new_thread( RunCommand, ( "rosrun map_server map_server map_lab.yaml > /dev/null 2> /dev/null", ))
start_new_thread( RunCommand, ( "rosrun tf static_transform_publisher 9.5 9 0 0.035 0 0 map wifi_base 50", ))

#-----------------------------------------------------------------#
#   Running the Kalman filter function
count = 0
wifiDB = open('wifi_map_lab.txt', 'r').readlines()
if(ReadOdometry):
  listener()
lastRobotX = 0
lastRobotY = 0

if (len(sys.argv) != 2):
  print("Define filename as argument")
  exit()
wFile = open(sys.argv[1],"a")

if (ReadFromFile2):
  rFile = open('ninfrontOfToalte.txt', 'r')

while(True):
  #simulate movement
  count = count + 1
  print("reading: " + str(count))

  #Odometry
  odom[0,0] = robotX - lastRobotX 
  odom[1,0] = robotY - lastRobotY
  lastRobotX = robotX
  lastRobotY = robotY
  print(robotX)
  print(robotY)

  #WiFi transform to coordinates
  #try:
  #  w = ReadWifi()
  if (ReadFromFile2):
    w, robotod = ReadWifi2(rFile)
    robotX = float(robotod[0])
    robotY = float(robotod[1])
  else:
    w = ReadWifi() 
  #except Exception as e:
  #  continue
  wFile.write("NEXT\n")
  wFile.write(str(robotX) + "," + str(robotY)+"\n")
  for key, value in w.iteritems():
    wFile.write(key + " " + value + "\n")
  wFile.write("END\n")

  z = zconverter(w,wifiDB);
  print(z)

  # run EKF
  [x, P] = ekf(f,x,P,h,z,Q,R,n,odom);

  # broadcast transform  
  #static_transformStamped.transform.translation.x = float(x[0,0]);
  static_transformStamped.transform.translation.x = float(x[0,0] - robotX);
  #static_transformStamped.transform.translation.y = float(x[1,0]);
  static_transformStamped.transform.translation.y = float(x[1,0] - robotY);
  broadcaster.sendTransform(static_transformStamped)
  
  time.sleep(1)

exit()

