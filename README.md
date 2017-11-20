# SAutLisboaErasmus
ROS project

rostopic list

rostopic pub /RosAria/cmd_vel  geometry_msgs/Twist "linear:  x: 0.0  y: 0.0  z: 0.0 angular:  x: 0.0  y: 0.0  z: 0.1" 

rosrun map_server map_server map1.yaml
rosrun tf static_transform_publher -1 0 0 0 0 0 map odom 50
roslaunch hokuyo_driver hokuyo_driver.launch
rosrun rviz rviz

# working
roscore
rosparam set RosAria/port /dev/pioneer/usb_to_serial_port && rosrun rosaria RosAria
rostopic pub -r 10 /RosAria/cmd_vel geometry_ms/Twist "{linear: {x: 0.1, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"

rostopic pub /RosAria/cmd_vel geometry_msgs/Twist "{linear: {x: -0.1, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
rostopic pub /RosAria/cmd_vel geometry_msgs/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.1}}"
rostopic pub /RosAria/cmd_vel geometry_msgs/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"

#WIFI
sudo iwlist wlp2s0 scan | grep -e 'Signal level' -e Address
sudo iwlist wlp2s0 scan | grep -oP -e "Signal level=\K.*"
List only MAC address and Signal strength
sudo iwlist wlp2s0 scan | grep -oP '(Address: |Signal level=)\K\S*'
