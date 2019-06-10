from time import time
import cv2
from voice import ASR
from robot import Robot
from pydub import AudioSegment, silence

if __name__ == '__main__':
    rb = Robot()
    asr = ASR()
    run = True
    while(run):
        frame = rb.getFrame()
        cv2.imshow('ai2thor', frame)
        
        asr.record_sound('record.wav', duration=5)
        myaudio = AudioSegment.from_wav('record.wav')
        audios = silence.split_on_silence(myaudio, min_silence_len=300, silence_thresh=-32, keep_silence=400)
        for audio in audios:
            print('Detecting...')
            audio.export('test.wav')
            asr.noise_cancel()
            command = asr.asr()
            print(command)
            if command == 'drop':
                rb.dropObject()
            else:
                rb.pickup(command)
            frame = rb.getFrame()
            cv2.imshow('ai2thor', frame)

        tmp = cv2.waitKey(50)
        if tmp != -1:
            key = chr(tmp)
            if key == 'q': run = False
            rb.apply(key)
        
    rb.stop()
    cv2.destroyAllWindows()