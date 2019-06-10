from time import time
import cv2
from voice import ASR
from robot import Robot
from pydub import AudioSegment, silence

if __name__ == '__main__':
    rb = Robot()
    obj = ASR()
    run = True
    while(run):
        frame = rb.getFrame()
        cv2.imshow('ai2thor', frame)
        

        obj.record_sound('record.wav', duration=5)
        t0 = time()
        myaudio = AudioSegment.from_wav('record.wav')
        audios = silence.split_on_silence(myaudio, min_silence_len=300, silence_thresh=-16, keep_silence=300)
        for audio in audios:
            print('Detecting...')
            audio.export('word.wav')
            obj.noise_cancel()
            command = obj.asr()
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
        t1 = time()
        print(t1-t0)

    rb.stop()
    cv2.destroyAllWindows()