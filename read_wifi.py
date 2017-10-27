import os
os.system("sudo iwlist wlp2s0 scan | grep -oP '(Address: |Signal level=)\K\S*'")

