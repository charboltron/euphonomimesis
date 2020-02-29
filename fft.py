import numpy as np
import scipy.fftpack
from playsound import playsound as ps
import struct
import display_plot
import wave as wav
import os

cwd = os.getcwd()
clip_dir = cwd+'/clips/'
clips = [file for file in os.listdir(clip_dir) if '.wav' in file]

for clip in range(len(clips)):
    wv = clip_dir+clips[clip]
    current_clip = wav.open(wv, 'rb')
    ps(wv)
    channels = current_clip.getnchannels()
    width = current_clip.getsampwidth()
    rate = current_clip.getframerate()
    frames = current_clip.getnframes()
    frame_width = width * channels

    wave_bytes = current_clip.readframes(frames)
    samples = []
    for f in range(0, len(wave_bytes), frame_width):
        frame = wave_bytes[f : f + frame_width]

        for c in range(0, len(frame), width):
            sample_bytes = frame[c : c + width]
            sample = int.from_bytes(sample_bytes,byteorder='little',signed=(width>1))
            samples.append(float(sample))

    yf = scipy.fftpack.rfft(samples)

    #TODO: genetics
    
    iyf = scipy.fftpack.irfft(yf, len(samples))

    f = 'mod_clips/new_sound_file.wav'

    wav_file = wav.open(f, 'w')
    wav_file.setparams(current_clip.getparams())
    for samp in iyf:
        wav_file.writeframes(struct.pack('h', int(samp)))
    ps(cwd+'/'+f)

    # display_plot(yf, num_samples)
    current_clip.close()