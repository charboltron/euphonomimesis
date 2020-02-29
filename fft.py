import numpy as np
import scipy.fftpack
from playsound import playsound as ps
import struct
import display_plot
import wave as wav
import os
import genetic

playback_params=None

def get_clips(max_clips):
    cwd = os.getcwd()
    clip_dir = os.listdir(cwd+'/clips/')
    clips = [f for f in clip_dir if '.wav' in f]
    fft_data = []
    for clip in range(min(max_clips, len(clips))):
        wv = cwd+'/clips/'+clips[clip]
        current_clip = wav.open(wv, 'rb')
        playback_params = current_clip.getparams()
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
    return np.array(fft_data)

def play_fft(fft_vector):
    cwd = os.getcwd()
    iyf = scipy.fftpack.irfft(fft_vector)
    file_path = 'mod_clips/new_sound_file.wav'
    write_file(file_path, iyf, playback_params) 
    ps(cwd+'/'+file_path) # play modified sound
    return

def write_file(name, sample_data, params):
    wav_file = wav.open(name, 'w')
    wav_file.setparams(params)
    for samp in sample_data:
        wav_file.writeframes(struct.pack('h', int(samp)))

def main():
    data = get_clips(4)
    for d in data:
        play_fft(d)

main()

#cross1, cross2 = crossover(fft_data[0], fft_data[1])
#inv_fft = scipy.fftpack.irfft(yf, len(samples))

