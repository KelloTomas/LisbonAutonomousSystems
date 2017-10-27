# SAutLisboaErasmus
ROS project

rostopic list

rostopic pub /RosAria/cmd_vel  geometry_msgs/Twist "linear:  x: 0.0  y: 0.0  z: 0.0 angular:  x: 0.0  y: 0.0  z: 0.1" 

# working
roscore
rosparam set RosAria/port /dev/pioneer/usb_to_serial_port && rosrun rosaria RosAria
rostopic pub -r 10 /RosAria/cmd_vel geometry_ms/Twist "{linear: {x: 0.1, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"

rostopic pub /RosAria/cmd_vel geometry_msgs/Twist "{linear: {x: -0.1, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
rostopic pub /RosAria/cmd_vel geometry_msgs/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.1}}"
rostopic pub /RosAria/cmd_vel geometry_msgs/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"

