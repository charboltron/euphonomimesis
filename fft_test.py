from numpy.fft import fft, fftfreq, ifft
import scipy.fftpack
from playsound import playsound as ps
import struct
import numpy as np
import matplotlib.pyplot as plt
import wave as wav
import time
import os

#Define parameters to make .wav files
num_samples = 44100
nframes = num_samples                                    #nframes is just the number of samples
sampling_rate = 44100.0 
amplitude = 16000                                        #fixed amplitude
comptype="NONE"                                          #compression type
compname="not compressed" 
nchannels=1
sampwidth=2   
cwd = os.getcwd()

clip_dir = cwd+'/clips/'
waves = [file for file in os.listdir(clip_dir) if '.wav' in file]

for wave in range(len(waves)):
    wv = clip_dir+waves[wave]
    current_clip = wav.open(wv, 'rb')
    ps(wv)
    channels = current_clip.getnchannels()
    width = current_clip.getsampwidth()
    rate = current_clip.getframerate()
    frames = current_clip.getnframes()
    frame_width = width * channels

    max_sample = None
    min_sample = None
    wave_bytes = current_clip.readframes(frames)
    samples = []
    for f in range(0, len(wave_bytes), frame_width):
        frame = wave_bytes[f : f + frame_width]

        for c in range(0, len(frame), width):
            sample_bytes = frame[c : c + width]
            sample = int.from_bytes(sample_bytes,
                                    byteorder='little',
                                    signed=(width>1))
            sample = float(sample)
            samples.append(sample)

    print(f'max sample = {max_sample}, min sample = {min_sample}')


    T = 1.0 / num_samples
    yf = scipy.fftpack.rfft(samples)
    xf = np.linspace(0.0, 1.0/(2.0*T), num_samples/2)

    iyf = scipy.fftpack.irfft(yf, len(samples))

    f = 'new_sound_file.wav'

    wav_file = wav.open(f, 'w')
    wav_file.setparams(current_clip.getparams())
    print(len(samples), len(iyf))
    for samp in iyf:
        wav_file.writeframes(struct.pack('h', int(samp)))
    ps(cwd+'/'+f)
    exit()

    # fig, ax = plt.subplots()
    # ax.plot(xf, 2.0/num_samples * np.abs(yf[:num_samples//2]))
    # print(2.0/num_samples * np.abs(yf[:num_samples//2]))
    # plt.show()

    current_clip.close()