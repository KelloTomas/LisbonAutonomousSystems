#!/usr/bin/python
import subprocess
import time
import sys

def ReadWifiFromFile(rFile):
	wifi = dict()
	while(True):
		data = rFile.readline().split()
		if (len(data) == 1):
			if (EnableTiming):
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
ReadFromFile = False
EnableTiming = True
if (WriteToFile or ReadFromFile):
	if (len(sys.argv) == 1):
		print("Define filename as argument")
		exit()

if (WriteToFile and ReadFromFile):
	print("Cant read and write from file together")
	exit()
count = 1

if (WriteToFile):
	wFile = open(sys.argv[1],"w")
if (ReadFromFile):
	rFile = open(sys.argv[1],"r")
while True:
	if (EnableTiming):
		time.sleep(2)
	s = time.time()
	if (ReadFromFile):
		if (rFile.readline() != "next\n"):
			print("End of input file")
			break
		w = ReadWifiFromFile(rFile)
	else:
		try:
			w = ReadWifi()
		except:
			continue
	f = time.time()

	#process data
	if(WriteToFile):
		wFile.write("next\n")
	for key, value in w.iteritems():
		if (WriteToFile):
			wFile.write(key + " " + value + "\n")
		else:
			print ("SSID: " + key + " signal: " + value +    " db")
	if (WriteToFile):
		wFile.write("{0:.2f}".format(f-s) + "\n")
	print(str(count) + ". reading for: " + "{0:.2f}".format(f-s) + "sec");
	count += 1
