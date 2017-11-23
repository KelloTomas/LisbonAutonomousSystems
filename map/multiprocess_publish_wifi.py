#!/usr/bin/env python
import subprocess
import thread
from time import sleep

def publishWifi(x, y, id):
    subprocess.call("rosrun tf static_transform_publisher " + str(x) + " " + str(y) + " 0 0 0 0 map wifi" + str(id) + " 50", shell=True)
    #subprocess.call("rosrun tf static_transform_publisher 3 -5 0 0 0 0 map wifi40 50", shell=True)
    #subprocess.call("ls", shell=True)

try:
    for i in xrange(1,10):
        x = 2*i
        y = 5*i
        thread.start_new_thread( publishWifi, ( x, y, i, ) )
except:
   print "Error: unable to start thread"
while True:
    print("OK")
    sleep(100)
