import sounddevice as sd
import soundfile as sf
import numpy as np
import librosa
import hmmlearn.hmm as hmm
from pydub.playback import play
import os
import pickle
import noisereduce as nr
from pydub import AudioSegment, silence


class ASR():
    def __init__(self):
        self.mapping = ['drop','Lettuce','Apple','Bread','Potato','Spoon','Knife','Fork']
        self.hmm = pickle.load(open('model/hmm.pk', 'rb'))
        self.n_sample=30

    def softmax_stable(self, Z):
        """
        Compute softmax values for each sets of scores in Z.
        each column of Z is a set of score.    
        """
        e_Z = np.exp(Z - np.max(Z))
        A = e_Z / e_Z.sum()
        return A

    def record_sound(self, filename, duration=1, fs=44100, play=False):
        print('Recording...')
        # sd.play( np.sin( 2*np.pi*940*np.arange(fs)/fs )  , samplerate=fs, blocking=True)
        # sd.play( np.zeros( int(fs*0.2) ), samplerate=fs, blocking=True)
        data = sd.rec(frames=duration*fs, samplerate=fs, channels=1, blocking=True)
        if play:
            sd.play(data, samplerate=fs, blocking=True)
        sf.write(filename, data=data, samplerate=fs)

    def record_data(self, prefix, n=10, start=0, duration=1):
        print('Recording {} {} times'.format(prefix, n))
        for i in range(n):
            print('{}_{}.wav'.format(prefix, i+start))
            self.record_sound('train/{}/{}_{}.wav'.format(prefix, prefix, i+start), duration=duration)
            if i % 5 == 4:
                input("Press Enter to continue...")
    
    def noise_cancel(self, filename='test.wav'):
        data, fs = librosa.load(filename)
        reduced_noise = nr.reduce_noise(audio_clip=data, noise_clip=data)
        sf.write(filename, data=reduced_noise, samplerate=fs)
                
    def get_mfcc(self, filename):
        data, fs = librosa.load(filename, sr=None)
        mfcc = librosa.feature.mfcc(data, sr=fs, n_fft=1024, hop_length=128)
        return mfcc.T

    def train(self):
        model = []
        for item in self.mapping:
            print('Training {}'.format(item))
            data = [self.get_mfcc('train/{}/{}_{}.wav'.format(item, item, idx)) for idx in range(self.n_sample)]
            model_temp = hmm.GaussianHMM(n_components=30, verbose=True, n_iter=200)
            model_temp.fit(X=np.vstack(data), lengths=[x.shape[0] for x in data])
            model.append(model_temp)
        pickle.dump(model, open('model/hmm.pk','wb'))

    def asr(self):
        # self.record_sound('test.wav')
        mfcc = self.get_mfcc('test.wav')
        score = []
        for i in range(len(self.mapping)):
            score.append(self.hmm[i].score(mfcc))
        res = self.mapping[score.index(max(score))]
        print('predict: {}'.format(res))
        return res