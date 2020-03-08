import numpy as np
import scipy.fftpack
from playsound import playsound as ps
import struct
import display_plot
import wave as wav
import os
import genetic as gen
import display_plot as disp

def get_clips(max_clips):
    cwd = os.getcwd()
    clip_dir = os.listdir(cwd+'/clips/')
    clips = [f for f in clip_dir if '.wav' in f]
    fft_data = []
    params = None
    for clip in range(min(max_clips, len(clips))):
        wv = cwd+'/clips/'+clips[clip]
        current_clip = wav.open(wv, 'rb')
        params = current_clip.getparams()
        ps(wv) # play sound
        channels = current_clip.getnchannels()
        width = current_clip.getsampwidth()
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
        yf = np.array(scipy.fftpack.rfft(samples))
        fft_data.append(yf) 
        current_clip.close()    
    return np.array(fft_data), params

def play_fft(fft_vector, params):
    cwd = os.getcwd()
    iyf = scipy.fftpack.irfft(fft_vector, 352800)
    file_path = 'mod_clips/new_sound_file.wav'
    write_file(file_path, iyf, params) 
    ps(cwd+'/'+file_path) # play modified sound
    return

def write_file(name, sample_data, params):
    wav_file = wav.open(name, 'w')
    wav_file.setparams(params)
    for samp in sample_data:
        wav_file.writeframes(struct.pack('h', int(samp)))

def loop():
    data, params = get_clips(2)
    ffts = []
    cross1 = data[0]
    cross2 = data[1]
    leftover1 = data[0][22000:]
    leftover2 = data[1][22000:]
    for i in range(1):
        cross1 = cross1[:22000]
        cross2 = cross2[:22000]
        cross1, cross2 = gen.crossover2(cross1, cross2)
        ffts.append(cross1) 
        ffts.append(cross2) 
        cross1, cross2 = np.append(cross1, leftover1), np.append(cross2, leftover2)
        play_fft(cross1, params)
        play_fft(cross2, params)
    return ffts

def main():
    ffts = loop()
    disp.display_ffts(ffts, len(ffts[0]))

main()

