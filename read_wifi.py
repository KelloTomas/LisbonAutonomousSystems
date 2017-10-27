import subprocess
data = subprocess.check_output("sudo iwlist wlp2s0 scan | grep -oP '(Address: |Signal level=)\K\S*'", shell=True)
#data = os.system("sudo iwlist wlp2s0 scan | grep -oP '(Address: |Signal level=)\K\S*'")

wifi = dict()
key = ""
for line in data.splitlines():
  if(key == ""):
    key = line
  else:
    wifi[key] = line
    key = ""

for key, value in wifi.iteritems():
  print ("SSID: " + key + " signal: " + value +    " db")
