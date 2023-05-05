#Voicetesting.py - tests porcupine wake word and rhino commands
#! /usr/bin/env python
import os
import struct
import wave
from datetime import datetime
import pvporcupine
import pvrhino
from pvrecorder import PvRecorder
import sys, roslaunch, copy, rospy, subprocess
from std_msgs.msg import Float64
import numpy as np

#Talker node - will publish joint position commands when necessary.
    
# Basic wake word script with picovoice​
keyword_paths = ['~/Desktop/Picovoice/Porcupine/Hey-Turtle-bot.ppn']
access_key = 'BKZ6QIyCZPIirHUNrqCmxR8mwVJHIPSGFv22P2/rFGpqJilSGLmf/g=='

porcupine = pvporcupine.create(
            access_key=access_key,
            keyword_paths=['~/Desktop/Picovoice/Porcupine/Hey-Turtle-bot.ppn'],
            ) 
rhino = pvrhino.create(access_key=access_key, context_path="/home/carlos/Desktop/Picovoice/Rhino/Arm.rhn")

print('Porcupine version: %s' % porcupine.version)
print('Rhino version: %s' % rhino.version)
print('Context info: %s' % rhino.context_info)

recorder = PvRecorder(device_index=5, frame_length=porcupine.frame_length)
recorder.start()


keywords = list()
for x in keyword_paths:
    keyword_phrase_part = os.path.basename(x).replace('.ppn', '').split('_')
    if len(keyword_phrase_part) > 6:
        keywords.append(' '.join(keyword_phrase_part[0:-6]))
    else:
        keywords.append(keyword_phrase_part[0])


rospy.init_node('PicoPublisher', anonymous=True)
rate = rospy.Rate(0.5) # 1/2 hz
pub1 = rospy.Publisher('/arm_shoulder_pan_joint/command', Float64, queue_size=10)
pub2 = rospy.Publisher('/arm_shoulder_lift_joint/command', Float64, queue_size=10)
pub3 = rospy.Publisher('/arm_elbow_flex_joint/command', Float64, queue_size=10)
pub4 = rospy.Publisher('/arm_wrist_flex_joint/command', Float64, queue_size=10)
pub5 = rospy.Publisher('/gripper_joint/command', Float64, queue_size=10)


wav_file = wave.open('wave.wav', "w")
wav_file.setnchannels(1)
wav_file.setsampwidth(2)
wav_file.setframerate(16000)
print('Using device: %s' %recorder.selected_device)
print('Listening ... (press Ctrl+C to exit)')


if __name__ == '__main__':
    try:
        while True:
            pcm = recorder.read()
            result = porcupine.process(pcm)
            is_finalized = rhino.process(pcm)

            if wav_file is not None:
                wav_file.writeframes(struct.pack("h" * len(pcm), *pcm))

        
            if is_finalized:
                inference = rhino.get_inference()
                if inference.is_understood:
                    print("  intent : '%s'" % inference.intent)
                    for slot, value in inference.slots.items():
                        print("  %s : '%s'" % (slot, value))
                        direction = value
                        
                    #stop recorder to prevent overflow error    
                    recorder.stop()
                    
                    if inference.intent == 'move':
                        #move to Up state
                        if direction =='up':
                            state = np.array([-1.8,0,1.5,1.5,0])
                            rospy.loginfo("Moving to 'UP' state...")
                            pub3.publish(state[2])
                            pub2.publish(state[1])
                            pub1.publish(state[0])
                            pub4.publish(state[3])
                            pub5.publish(state[4])
                            rate.sleep()
                            rospy.loginfo("Joint Angle is: [%1.2f %1.2f %1.2f %1.2f %1.2f] ",
                                           state[0],state[1],state[2],state[3],state[4])
                        #move to Down state
                        elif direction =='down':
                            state = np.array([-1.8,-1.7,1.5,1.5,0])
                            rospy.loginfo("Moving to 'DOWN' state...")
                            pub3.publish(state[2])
                            pub2.publish(state[1])
                            pub1.publish(state[0])
                            pub4.publish(state[3])
                            pub5.publish(state[4])
                            rate.sleep()
                            rospy.loginfo("Joint Angle is: [%1.2f %1.2f %1.2f %1.2f %1.2f] ",
                                           state[0],state[1],state[2],state[3],state[4])
                        #move to Left state
                        elif direction =='left':
                            state = np.array([-1,-1.4,-1,1.5,0])
                            rospy.loginfo("Moving to 'LEFT' state...")
                            pub3.publish(state[2])
                            rate.sleep()
                            rate.sleep()
                            pub2.publish(state[1])
                            pub1.publish(state[0])
                            pub4.publish(state[3])
                            pub5.publish(state[4])
                            rate.sleep()
                            rospy.loginfo("Joint Angle is: [%1.2f %1.2f %1.2f %1.2f %1.2f] ",
                                           state[0],state[1],state[2],state[3],state[4])
                        #move to Right state
                        elif direction =='right':
                            state = np.array([-2.6,-1.4,-1,1.5,0])
                            rospy.loginfo("Moving to 'RIGHT' state...")
                            pub3.publish(state[2])
                            pub2.publish(state[1])
                            pub1.publish(state[0])
                            pub4.publish(state[3])
                            pub5.publish(state[4])
                            rate.sleep()
                            rospy.loginfo("Joint Angle is: [%1.2f %1.2f %1.2f %1.2f %1.2f] ",
                                           state[0],state[1],state[2],state[3],state[4])
                        else:
                            pass
                    #start recorder to continue listening.
                    recorder.start()
                    
                    if inference.intent == 'sayHi':
                        recorder.stop()
                        state = np.array([-1,-1.4,-1,1.5,0])
                        rospy.loginfo("Moving to 'LEFT' state...")
                        pub3.publish(state[2])
                        rate.sleep()
                        
                        pub2.publish(state[1])
                        pub1.publish(state[0])
                        pub4.publish(state[3])
                        pub5.publish(state[4])
                        rate.sleep()
                        rospy.loginfo("Joint Angle is: [%1.2f %1.2f %1.2f %1.2f %1.2f] ",
                                       state[0],state[1],state[2],state[3],state[4])
                                       
                        state = np.array([-2.6,-1.4,-1,1.5,0])
                        rospy.loginfo("Moving to 'RIGHT' state...")
                        pub3.publish(state[2])
                        pub2.publish(state[1])
                        pub1.publish(state[0])
                        pub4.publish(state[3])
                        pub5.publish(state[4])
                        rate.sleep()
                        rospy.loginfo("Joint Angle is: [%1.2f %1.2f %1.2f %1.2f %1.2f] ",
                                   state[0],state[1],state[2],state[3],state[4])
                        state = np.array([-1,-1.4,-1,1.5,0])
                        rospy.loginfo("Moving to 'LEFT' state...")
                        pub3.publish(state[2])
                        pub2.publish(state[1])
                        pub1.publish(state[0])
                        pub4.publish(state[3])
                        pub5.publish(state[4])
                        rate.sleep()
                        rospy.loginfo("Joint Angle is: [%1.2f %1.2f %1.2f %1.2f %1.2f] ",
                                   state[0],state[1],state[2],state[3],state[4])
                        state = np.array([-2.6,-1.4,-1,1.5,0])
                        rospy.loginfo("Moving to 'RIGHT' state...")
                        pub3.publish(state[2])
                        pub2.publish(state[1])
                        pub1.publish(state[0])
                        pub4.publish(state[3])
                        pub5.publish(state[4])
                        rate.sleep()
                        rospy.loginfo("Joint Angle is: [%1.2f %1.2f %1.2f %1.2f %1.2f] ",
                                   state[0],state[1],state[2],state[3],state[4])
                        recorder.start()
                    if inference.intent == 'shutdown':
                       recorder.stop()
                       print('Shutting Down Script ...')
                       recorder.delete()
                       porcupine.delete()
                       rhino.delete()
                       wav_file.close()
                       exit(0)
    except KeyboardInterrupt:
        print('Stopping ...')
    finally:
        recorder.delete()
        porcupine.delete()
        rhino.delete()
        if wav_file is not None:
            wav_file.close()

