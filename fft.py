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
    goal_clip = '0a0a8d4c.6.wav'
    fft_goal = []
    cwd = os.getcwd()
    clip_dir = os.listdir(cwd+'/1secs/')
    clips = [f for f in clip_dir if '.wav' in f if f != goal_clip]
    if(goal_clip not in clips):
        clips.insert(0, goal_clip)
    fft_data = []
    params = None
    for clip in range(min(max_clips, len(clips))):
        print(clips[clip])
        wv = cwd+'/1secs/'+clips[clip]
        current_clip = wav.open(wv, 'rb')
        params = current_clip.getparams()
        # ps(wv) # play sound
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
        if clips[clip] == goal_clip:
            fft_goal = yf
        else: 
            fft_data.append(yf) 
        current_clip.close()    
    return np.array(fft_data), params, fft_goal

counter = 0

def play_fft(fft_vector, params):
    global counter
    counter += 1
    cwd = os.getcwd()
    iyf = scipy.fftpack.irfft(fft_vector, 44100)
    file_path = 'mod_clips/exp' + str(counter) + '.wav'
    write_file(file_path, iyf, params) 
    # ps(cwd+'/'+file_path) # play modified sound
    return

def write_file(name, sample_data, params):
    wav_file = wav.open(name, 'w')
    wav_file.setparams(params)
    for samp in sample_data:
        if not ((-0x7fff - 1) <= int(samp) or int(samp) <= 0x7fff):
            print(f'whats this? {int(samp)}')
        else:
          wav_file.writeframes(struct.pack('h', int(samp)))

def breed_loop(N):
    data, params, gdata = get_clips(500)
    for n in range(N):
        ffts = []
        errors = gen.fit_all(data, gdata)

        for i in range(len(data)//2): #gen range*2 children
            r = np.arange(len(errors))
            i1, i2 = np.random.choice(r, 2, p=errors)
            cross1, cross2 = data[i1], data[i2]
            leftover1 = cross1[22000:]
            leftover2 = cross2[22000:]        
            cross1    = cross1[:22000]
            cross2    = cross2[:22000]
            
            cross1, cross2 = gen.crossover(cross1, cross2)
            # cross1, cross2 = gen.mutate(cross1, 0.8), gen.mutate(cross2, 0.8)
            cross1, cross2 = np.append(cross1, leftover1), np.append(cross2, leftover2)
            data[i], data[2*i] = cross1, cross2
            if n % 5 == 0 and i % 10 == 0:
                play_fft(cross1, params)
                play_fft(cross2, params)
    return ffts

def main():
    ffts = breed_loop(1000)
    # disp.display_ffts(ffts, len(ffts[0]))

main()

