# SAutLisboaErasmus
ROS project

## Run programs
roscore
rostopic list
rosparam set RosAria/port /dev/pioneer/usb_to_serial_port && rosrun rosaria RosAria
rosrun map_server map_server map1.yaml
rosrun tf static_transform_publisher -1 0 0 0 0 0 map odom 50
roslaunch hokuyo_driver hokuyo_driver.launch
rostopic echo /RosAria/pose
rosrun rviz rviz

rosrun teleop_twist_keyboard teleop_twist_keyboard.py cmd_vel:=/RosAria/cmd_vel

## Show wifi on map
cd LisbonAutonomousSystems/map
python show_wifi_measure_on_map.py wifi_map_lab.txt

## Robot moving
rostopic pub /RosAria/cmd_vel  geometry_msgs/Twist "linear:  x: 0.0  y: 0.0  z: 0.0 angular:  x: 0.0  y: 0.0  z: 0.1" 
rostopic pub -r 10 /RosAria/cmd_vel geometry_ms/Twist "{linear: {x: 0.1, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
rostopic pub /RosAria/cmd_vel geometry_msgs/Twist "{linear: {x: -0.1, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
rostopic pub /RosAria/cmd_vel geometry_msgs/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.1}}"
rostopic pub /RosAria/cmd_vel geometry_msgs/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"

# Read WIFI
sudo iwlist wlp2s0 scan | grep -oP '(Address: |Signal level=)\K\S*'
