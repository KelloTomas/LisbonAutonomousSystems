#!/usr/bin/env python
import subprocess
import thread
from time import sleep

def publishWifi(id):
    subprocess.call("rosrun tf static_transform_publisher " + str(id) + " -5 0 0 0 0 map wifi" + str(id) + " 50", shell=True)
    #subprocess.call("rosrun tf static_transform_publisher 3 -5 0 0 0 0 map wifi40 50", shell=True)
    #subprocess.call("ls", shell=True)

try:
    for x in xrange(1,10):
        thread.start_new_thread( publishWifi, ( x*2, ) )
except:
   print "Error: unable to start thread"
while True:
    print("OK")
    sleep(100)
