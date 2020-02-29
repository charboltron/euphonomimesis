from numpy.fft import fft, fftfreq, ifft
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

# Get the signal file.
waves = [file for file in os.listdir(clip_dir) if '.wav' in file]
# waves = [file for file in os.listdir() if '.wav' in file]

for wave in range(len(waves)):
    wv = clip_dir+waves[wave]
    wavfile = wav.open(wv, 'rb')
    #play the sound
    # ps(wv)
    # Channels per frame.
    channels = wavfile.getnchannels()
    # Bytes per sample.
    width = wavfile.getsampwidth()
    # Sample rate
    rate = wavfile.getframerate()
    # Number of frames.
    frames = wavfile.getnframes()
    # Length of a frame
    frame_width = width * channels

    # Get the signal and check it.
    max_sample = None
    min_sample = None
    wave_bytes = wavfile.readframes(frames)
    # Iterate over frames.
    samples = []
    for f in range(0, len(wave_bytes), frame_width):
        frame = wave_bytes[f : f + frame_width]
        #print(frame)
        # Iterate over channels.
        for c in range(0, len(frame), width):
            # Build a sample.
            sample_bytes = frame[c : c + width]
            # XXX Eight-bit samples are unsigned
            sample = int.from_bytes(sample_bytes,
                                    byteorder='little',
                                    signed=(width>1))
            #print(sample)
            sample = float(sample)
            samples.append(sample)
            # Check extrema.
            #if max_sample == None:
            #    max_sample = sample
            #if min_sample == None:
            #    min_sample = sample
            #if sample > max_sample:
            #    max_sample = sample
            #if sample < min_sample:
            #    min_sample = sample

    import scipy.fftpack

    # Number of samplepoints
    # sample spacing
    T = 1.0 / num_samples
    # x = np.linspace(0.0, num_samples*T, num_samples)
    yf = scipy.fftpack.rfft(samples)
    xf = np.linspace(0.0, 1.0/(2.0*T), num_samples/2)

    iyf = scipy.fftpack.irfft(yf, len(samples))
    for i in range(0, 20000, 1000):
        print(samples[i], iyf[i])
    f = 'new_sound_file.wav'
    wav_file = wav.open(f, 'w')
    wav_file.setparams((nchannels, sampwidth, int(sampling_rate), nframes, comptype, compname))
    print(len(samples), len(iyf))
    samples -= amplitude//2
    for samp in samples:
        print(samp*amplitude)   
        wav_file.writeframes(struct.pack('h', int(samp*amplitude)//2))
    ps(cwd+f)
    exit()

    # print(yf)
    # print(f'min yf = {min(yf)}, max yf = {max(yf)}')
    # print(f'min xf = {min(xf)}, max xf = {max(xf)}')
    # # exit()
    # fig, ax = plt.subplots()
    # ax.plot(xf, 2.0/num_samples * np.abs(yf[:num_samples//2]))
    # print(2.0/num_samples * np.abs(yf[:num_samples//2]))
    # plt.show()

    wavfile.close()