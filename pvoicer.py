#pvoicer.py - Script For Voice-Activated Control of Robotic Arm Through ROS
# Carlos Mella-Rijo, University of Texas at Arlington

# Create an instance of Picovoice using Porcupine keyword file  (.ppn), and a Rhino context file  (.rhn):
from picovoice import Picovoice

def wake_word_callback():
    # wake word detected
    pass

def inference_callback(inference):
   if inference.is_understood:
      intent = inference.intent
      slots = inference.slots
      # take action based on intent and slot values
   else:
      # unsupported command
      pass

handle = Picovoice(
     access_key=${ACCESS_KEY},
     keyword_path=${KEYWORD_FILE_PATH},
     wake_word_callback=wake_word_callback,
     context_path=${CONTEXT_FILE_PATH},
     inference_callback=inference_callback)
     
 def get_next_audio_frame():
    pass

while True:
    audio_frame = get_next_audio_frame()
    handle.process(audio_frame)
    
# Release resources explicitly when done with Picovoice:
   handle.delete()
   
# Create custom wake word and context files using the Picovoice Console . Download the custom models (.ppn and .rhn) and pass them into the Picovoice constructor.

handle = Picovoice(
     access_key=${ACCESS_KEY},
     keyword_path=${KEYWORD_FILE_PATH},
     wake_word_callback=wake_word_callback,
     context_path=${CONTEXT_FILE_PATH},
     inference_callback=inference_callback)
