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

from ekfilter import ekf
from jacobmat import jacobmat

import matplotlib.pyplot as plt

#h = lambda x: np.array([[0.75*x[0,0]]])
#f = lambda x: np.array([[x[0,0] * np.cos(x[0,0]*2*pi/N)+2], [x[1,0] * np.cos(x[1,0]*2*pi/N)+2 ]])

#h = lambda x: np.array([[0.75*x[0,0]]]);
#f = lambda x: np.array([[x[0,0] + 1], [x[1,0] + 1]]);

#h = lambda x: np.array([[x[0,0]]]);
#f = lambda x: np.array([[x[0,0] +3/N], [x[1,0] + 3/N]]);

def ReadWifiFromFile(rFile):
  wifi = dict()
  if (rFile.readline() != "NEXT\n"):
    #print("End of input file")
    return wifi
  while(True):
    data = rFile.readline().split()
    if (len(data) == 1):
      return wifi
    if(len(data) == 0):
      return wifi
    wifi[data[0]] = data[1]

h = lambda x,odom: np.array([[x[0,0]], [x[1,0]]]);
f = lambda x,odom: np.array([[x[0,0]+odom[0,0]], [x[1,0]+odom[1,0]]]);


def rand_norm():
  t = random.standard_normal([1,]);
  return t

def v_rand(n):
  #Setting the initial state of x to the initial input signal + random noise
  v = random.standard_normal([1,]);
  v = np.array(v);

  for i in range (0,n-1):
    v = vstack([v, rand_norm()])
  return v



N = 20;                   #total dynamic steps
n = 2;
                    #number of state
q = 1;                 #standard deviation of the process 
r = 2;                 #standard deviation of the measurement
Q = q**2 * identity(n);   #covariance of the process
R = r**2; 
               #covariance of the measurement  
P = identity(n);            # initial state covraiance
pi = math.pi;


#-----------------------------------------------------------------#
#Allocate memory
xVector = np.zeros((n,N));          #estmate
sVector = np.zeros((n,N));          #actual
zVector = np.zeros((n,N));
oVector = np.zeros((n,N));
#-----------------------------------------------------------------#

#-----------------------------------------------------------------#
#   Creating the dataset and measurement

v = v_rand(n);
s = np.zeros((2,1));

delta = np.zeros((2,1));
odom = np.zeros((2,1));
x = np.array([[14.366],[0.374]]);


#init transform

rospy.init_node('my_static_tf2_broadcaster')
broadcaster = tf2_ros.StaticTransformBroadcaster()
static_transformStamped = geometry_msgs.msg.TransformStamped()
static_transformStamped.header.stamp = rospy.Time.now()
static_transformStamped.header.frame_id = "wifibase"
static_transformStamped.child_frame_id = "robotbase"
static_transformStamped.transform.translation.x = 0
static_transformStamped.transform.translation.y = 0
static_transformStamped.transform.translation.z = 0
static_transformStamped.transform.rotation.x = 0
static_transformStamped.transform.rotation.y = 0
static_transformStamped.transform.rotation.z = 0
static_transformStamped.transform.rotation.w = 0
#-----------------------------------------------------------------#
#   Running the Kalman filter function
for k in range (0,N):
  #State vector
  s[0,0] = 14.366 + k/10;
  s[1,0] = 1.63;
  sVector[:,k] = s[:,0];

  #Odometry
  if k > 0:
    odom[:,0] = sVector[:,k] - sVector[:,k-1]
    oVector[:,k] = odom[:,0];

  #Signal
  mapp1 = open('wifi_map_lab.txt', 'r')
  mapp = mapp1.readlines()

  rFile = open('signal2.txt','r')
  w = ReadWifiFromFile(rFile)

  z = zconverter(w,mapp);
  zVector[:,k] = z[:,0]

  [x, P] = ekf(f,x,P,h,z,Q,R,n,odom);
  for kk in range (0,n):
    xVector[kk,k] = x[kk,0];
  
  static_transformStamped.transform.translation.x = x[0,0] -s[0,0];
  static_transformStamped.transform.translation.y = x[1,0] -s[1,0];
  broadcaster.sendTransform(static_transformStamped)
  
  time.sleep(2)






plt.figure(1)
plt.subplot(211)
plt.plot(sVector[0,:], label='Odometry')
plt.plot(xVector[0,:], label='Filtered signal', c='b', lw=2)
plt.plot(zVector[0,:], '.', label='Wifi signal')
plt.legend(loc='best');
plt.axis([0,N,10,17])
plt.subplot(212)
plt.plot(sVector[1,:], label='Odometry')
plt.plot(xVector[1,:], label='Filtered signal', c='b', lw=2)
plt.plot(zVector[1,:], '.', label='Wifi signal')
plt.legend(loc='best');
plt.axis([0,N,0,3])
plt.show()



print(sVector)
print(xVector)
print(zVector)
print(oVector)

