Terminal 1 - Git Checkout & Simulation:
source /opt/ros/noetic/setup.bash
cd ~/simulation_ws/src/tortoisebot_waypoints
git checkout task1
source ~/simulation_ws/devel/setup.bash
roslaunch tortoisebot_gazebo tortoisebot_playground.launch
Abort and Re-Launch Gazebo if there are any issues. Use kill -9 <gazebo_pid>.

Terminal 2 - ROS1 Test:
source /opt/ros/noetic/setup.bash
cd ~/simulation_ws && catkin_make && source devel/setup.bash
rostest tortoisebot_waypoints waypoints_test.test --reuse-master

For SUCCESS:
rostest tortoisebot_waypoints waypoints_test.test --reuse-master x:=0.5 y:=0.5 tolerance:=0.1
For FAILURE:
rostest tortoisebot_waypoints waypoints_test.test --reuse-master x:=1.0 y:=0.5 tolerance:=0.1
