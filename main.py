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
        

        obj.record_sound('check.wav', duration=2)
        myaudio = AudioSegment.from_wav('check.wav')
        audios = silence.split_on_silence(myaudio, min_silence_len=300, silence_thresh=-32, keep_silence=400)
        for audio in audios:
            audio.export('test.wav')
            obj.noise_cancel()
            command = obj.asr()
            print(command)
            if command == 'drop':
                rb.dropObject()
            else:
                rb.pickup(command)

        tmp = cv2.waitKey(1000)
        if tmp != -1:
            key = chr(tmp)
            if key == 'q': run = False
            rb.apply(key)

    rb.stop()
    cv2.destroyAllWindows()