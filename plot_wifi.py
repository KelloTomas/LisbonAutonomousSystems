import matplotlib.pyplot as plt
import numpy as np
import time
import sys

def ReadWifiFromFile(rFile):
	wifi = dict()
	while(True):
		data = rFile.readline().split()
		if (len(data) == 1):
			return wifi
		if(len(data) == 0):
			return wifi
		wifi[data[0]] = data[1]
if (len(sys.argv) == 1):
	print("Define filename as argument")
	exit()
rFile = open(sys.argv[1],"r")
wifis = dict()
count = 0
while (rFile.readline() == "next\n"):
	for key, value in ReadWifiFromFile(rFile).iteritems():
		if key not in wifis:
			wifis[key] = list()
		while (len(wifis[key]) < count):
			wifis[key].append(0)
		wifis[key].append(float(value))
	count += 1
for key, value in wifis.iteritems():
	count = 0
	x = list()
	y = list()
	for v in value:
		if (v != 0):
			x.append(count)
			y.append(v)
		count +=1
	plt.plot(x,y, label=key, marker='o')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()
