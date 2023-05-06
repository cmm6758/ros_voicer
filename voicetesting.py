# voicetesting.py - Basic voice command script with picovoice
import argparse, os, struct, wave, pvporcupine
from datetime import datetime
from pvrecorder import PvRecorder

# Creating porcupine module instance.
# args: access_key (from my picovoice account) and keyword_paths - path to where my porcupine ppn file is.
porcupine = pvporcupine.create(
            access_key='BKZ6QIyCZPIirHUNrqCmxR8mwVJHIPSGFv22P2/rFGpqJilSGLmf/g==',
            keyword_paths=['~/Desktop/Picovoice/Porcupine/Hey-Turtle-bot.ppn'],
            )
# Parsing porcupine ppn file to gather the keywords.Adds the keyword(s) to a matrix.
 keywords = list()
    for x in keyword_paths:
        keyword_phrase_part = os.path.basename(x).replace('.ppn', '').split('_')
        if len(keyword_phrase_part) > 6:
            keywords.append(' '.join(keyword_phrase_part[0:-6]))
        else:
            keywords.append(keyword_phrase_part[0])
# Print out porcupine version on startup.
    print('Porcupine version: %s' % porcupine.version)
 
# Create PVRecorder module instance.
# Args: Device_index - can pick audio device if one wishes. 
# The demo script has a function where the audio device list can be printed to the terminal.
    recorder = PvRecorder(
        device_index=args.audio_device_index,
        frame_length=porcupine.frame_length)
    recorder.start()
# Creates a .wav file where sound is stored while the script is listening. 
# Stores it to a file named w.wav in the same directory the script is in.
    wav_file = None
    if args.output_path is not None:
        wav_file = wave.open(args.output_path, "w")
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(16000)
# Prints a statement letting the user know the recording has started. 
# Also informs of the Python keyboard interrupt Ctrl+C.
    print('Listening ... (press Ctrl+C to exit)')

# Reads recording - done by pvrecorder module
# Porcupine then processes it and assigns a boolean variable to '1' upon detection of the keyword.
    try:
        while True:
            pcm = recorder.read()
            result = porcupine.process(pcm)

            if wav_file is not None:
                wav_file.writeframes(struct.pack("h" * len(pcm), *pcm))

            if result >= 0:
 # Letting Client know that the result was  detected.
                print('[%s] Detected %s' % (str(datetime.now()), keywords[result]))
 #Stopping script with Keyboard Interrupt. 
    except KeyboardInterrupt:
        print('Stopping ...')
    finally:
        recorder.delete()
        porcupine.delete()
        if wav_file is not None:
            wav_file.close()

# Makes script only execute code when chosen
if __name__ == '__main__':
    main()


