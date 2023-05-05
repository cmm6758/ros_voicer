#! /usr/bin/env python
import sys, roslaunch, copy, rospy, subprocess
from std_msgs.msg import Float64
import numpy as np

#subprocess.run(["python","launching.py"])

#Talker node - will publish joint position commands when necessary.
def talker():
    pub1 = rospy.Publisher('/arm_shoulder_pan_joint/command', Float64, queue_size=10)
    pub2 = rospy.Publisher('/arm_shoulder_lift_joint/command', Float64, queue_size=10)
    pub3 = rospy.Publisher('/arm_elbow_flex_joint/command', Float64, queue_size=10)
    pub4 = rospy.Publisher('/arm_wrist_flex_joint/command', Float64, queue_size=10)
    pub5 = rospy.Publisher('/gripper_joint/command', Float64, queue_size=10)
    
    rospy.init_node('PicoPublisher', anonymous=True)
    rate = rospy.Rate(0.2) # 1/2 hz
    while not rospy.is_shutdown():
  # Neutral State
  
        state = np.array([-1.8,-1.4,-1,1.5,0])
        rospy.loginfo("Moving to 'NEUTRAL' state...")
        pub1.publish(state[0])
        pub2.publish(state[1])
        pub3.publish(state[2])
        pub4.publish(state[3])
        pub5.publish(state[4])
        rospy.loginfo("Joint Angle is: [%1.2f %1.2f %1.2f %1.2f %1.2f] ",state[0],state[1],state[2],state[3],state[4])
        rate.sleep()
  # Up State
        state = np.array([-1.8,0,1.5,1.5,0])
        rospy.loginfo("Moving to 'UP' state...")
        pub1.publish(state[0])
        pub2.publish(state[1])
        pub3.publish(state[2])
        pub4.publish(state[3])
        pub5.publish(state[4])
        rospy.loginfo("Joint Angle is: [%1.2f %1.2f %1.2f %1.2f %1.2f] ",state[0],state[1],state[2],state[3],state[4])
        rate.sleep()
  #Down State
        state = np.array([-1.8,-1.7,1.5,1.5,0])
        rospy.loginfo("Moving to 'DOWN' state...")
        pub1.publish(state[0])
        pub2.publish(state[1])
        pub3.publish(state[2])
        pub4.publish(state[3])
        pub5.publish(state[4])
        rospy.loginfo("Joint Angle is: [%1.2f %1.2f %1.2f %1.2f %1.2f] ",state[0],state[1],state[2],state[3],state[4])
        rate.sleep()
  #left State
        state = np.array([-1,-1.4,-1,1.5,0])
        rospy.loginfo("Moving to 'LEFT' state...")
        pub3.publish(state[2])
        rate.sleep()
        pub1.publish(state[0])
        pub2.publish(state[1])
        pub4.publish(state[3])
        pub5.publish(state[4])
        rospy.loginfo("Joint Angle is: [%1.2f %1.2f %1.2f %1.2f %1.2f] ",state[0],state[1],state[2],state[3],state[4])
        rate.sleep()
  #Right State
        state = np.array([-2.6,-1.4,-1,1.5,0])
        rospy.loginfo("Moving to 'RIGHT' state...")
        pub1.publish(state[0])
        pub2.publish(state[1])
        pub3.publish(state[2])
        pub4.publish(state[3])
        pub5.publish(state[4])
        rospy.loginfo("Joint Angle is: [%1.2f %1.2f %1.2f %1.2f %1.2f] ",state[0],state[1],state[2],state[3],state[4])
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass






