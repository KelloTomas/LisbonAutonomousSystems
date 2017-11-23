#!/usr/bin/env python

from subprocess import call
from thread import start_new_thread
from sys import argv
from time import sleep

PRINT_OUTPUT = False
SHOW_GMAP = True

class WifiRecord:
	"""class to store wifi measurement with position"""
	def __init__(self, poseX, poseY, wifiData):
		self.X = poseX
		self.Y = poseY
		self.data = wifiData

def RunCommand(command):
    call(command, shell=True)

def PublishWifi(x, y, name):
    RunCommand("rosrun tf static_transform_publisher " + str(x) + " " + str(y) + " 0 0 0 0 wifi_base wifi" + str(name) + " 50")
    #rosrun tf static_transform_publisher 0 0 0 0 0 0 odom map" + str(name) + " 50

def ReadWifiFromFile(rFile):
	wifi = dict()
	while(True):
		data = rFile.readline().split()
		if (len(data) == 1):
			return wifi
		if(len(data) == 0):
			return wifi
		wifi[data[0]] = data[1]

def ReadWifiData(filename):
	rFile = open(filename,"r")
	data = list()
	while (rFile.readline() == "NEXT\n"):
		position = rFile.readline().split(',')
		data.append(WifiRecord(float(position[0]), float(position[1]), ReadWifiFromFile(rFile)))
	return data



if (len(argv) == 1):
	print("Define filename as argument")
	exit()
w = ReadWifiData(argv[1])
PRINT_OUTPUT = False

if(PRINT_OUTPUT):
    print("\nmeasurement 0")
    print(w[0].X)
    print(w[0].Y)
    
    print("\nmeasurement 1")
    print(w[1].X)
    print(w[1].Y)
    print("\nmeasurement 1 - all wifi data in python dictionary")
    print(w[1].data)
    print("\n0 measure wifi SSID")
    print(w[1].data.items()[0][0])
    print("\n0 measure wifi signal")
    print(w[1].data.items()[0][1])
    
    print("\n1 measure wifi SSID")
    print(w[1].data.items()[1][0])
    print("\n1 measure wifi signal")
    print(w[1].data.items()[1][1])
    
    #print(w[1].data.iteritems().next()[1])
    
    print(len(w))
i = 0.0
start_new_thread( RunCommand, ( "rosrun map_server map_server map_lab.yaml", ))
start_new_thread( RunCommand, ( "rosrun tf static_transform_publisher 9.5 9 0 0.035 0 0 map wifi_base 50", ))

for x in w:
    start_new_thread( PublishWifi, ( x.X, x.Y, i, ) )
    i+=1.0
while True:
    pass
