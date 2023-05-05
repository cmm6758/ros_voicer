#Launching.py - Meant to Start Arm's Launch File


#! /usr/bin/env python
import sys
import roslaunch
import copy
import rospy
from std_msgs.msg import String

#initiate ros nodes
rospy.init_node('Launch', anonymous=True)
uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
roslaunch.configure_logging(uuid)

#starting node for arm bringup from launch file
launch = roslaunch.parent.ROSLaunchParent(uuid, ["/home/carlos/catkin_ws/src/pincher_arm/pincher_arm_bringup/launch/arm.launch"])
launch.start()
rospy.loginfo("started")

rospy.sleep(1000)
