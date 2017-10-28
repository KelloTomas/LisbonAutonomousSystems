#!/usr/bin/python
import subprocess
import time

def ReadWifiFromFile(rFile):
	wifi = dict()
	while(True):
		data = rFile.readline().split()
		if (len(data) == 1):
			time.sleep(float(data[0]))
			return wifi
		if(len(data) == 0):
			return wifi
		wifi[data[0]] = data[1]


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

WriteToFile = False
ReadFromFile = True
if (WriteToFile and ReadFromFile):
	print("Cant read and write from file together")
	exit()
count = 1

if (WriteToFile):
	wFile = open("data_wifi.txt","w")
if (ReadFromFile):
	rFile = open("data_wifi.txt","r")
while True:
	s = time.time()
	if (ReadFromFile):
		w = ReadWifiFromFile(rFile)
	else:
		w = ReadWifi()
	f = time.time()

	#process data
	for key, value in w.iteritems():
		if (WriteToFile):
			wFile.write(key + " " + value + "\n")
		else:
			print ("SSID: " + key + " signal: " + value +    " db")
	if (WriteToFile):
		wFile.write("{0:.2f}".format(f-s) + "\n")
	print(str(count) + ". reading for: " + "{0:.2f}".format(f-s) + "sec");
	count += 1
	time.sleep(2)
