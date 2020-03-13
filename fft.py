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
    goal_clip = 'Piccolo.3.wav'
    fft_goal = []
    cwd = os.getcwd()
    # clip_dir = os.listdir(cwd+'/clips/')
    clip_dir = os.listdir(cwd+'/1secs/')
    clips = [f for f in clip_dir if '.wav' in f if f != goal_clip]
    if(goal_clip not in clips):
        clips.insert(0, goal_clip)
    fft_data = []
    params = None
    for clip in range(min(max_clips, len(clips))):
        # print(clips[clip])
        if clips[clip] == goal_clip:
            wv = cwd+'/1sec_goals/'+clips[clip]
        else:
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
        if len(samples) != 44100: 
            print(f'deleting file! {wv}')
            os.remove(wv) 
            # exit()

        yf = np.array(scipy.fftpack.rfft(samples))
        if clips[clip] == goal_clip:
            fft_goal = yf
        else: 
            fft_data.append(yf) 
        current_clip.close()    
    return np.array(fft_data), params, fft_goal

def play_fft(fft_vector, params):
    cwd = os.getcwd()
    iyf = scipy.fftpack.irfft(fft_vector, 44100)
    file_path = 'mod_clips/new_sound_file.wav'
    write_file(file_path, iyf, params) 
    ps(cwd+'/'+file_path) # play modified sound
    return

def write_file(name, sample_data, params):
    wav_file = wav.open(name, 'w')
    wav_file.setparams(params)
    for samp in sample_data:
        samp = int(samp)
        if (samp<=32767 and samp>=-32767):
            wav_file.writeframes(struct.pack('h', samp))
        else:
            wav_file.writeframes(struct.pack('h', 0))

def breed_loop(N):
    data, params, gdata = get_clips(8715)
    for n in range(N):
        print(f'n = {n}')
        for i in range(len(data)//2): #gen range*2 children
            errors, goal = gen.fit_all(data, gdata)
            if(goal):
                play_fft(data[minindx], params)
                exit()
            r = np.arange(len(errors))
            i1, i2 = np.random.choice(r, 2, p=errors)
            cross1, cross2 = data[i1], data[i2]
            leftover1 = cross1[22000:]
            leftover2 = cross2[22000:]        
            cross1    = cross1[:22000]
            cross2    = cross2[:22000]
            
            minerr = 100.0
            maxerr1 = 0.0
            maxerr2 = 0.0
            for j in range(len(errors)):
                if errors[j] < minerr:
                    minerr = errors[j]
                    minindx = j
                if errors[j] > maxerr1:
                    if errors[j] > maxerr2:
                        maxerr2 = errors[j]
                        maxerrindx1 = j
                    else:
                        maxerr1 = errors[j]
                        maxerrindx2 = j
            if i == 0:
                print(f'mininum error = {min(errors/sum(errors))} ')
                play_fft(data[np.random.randint(0, len(data))], params)
                # play_fft(cross2, params)
            cross1, cross2 = gen.crossover(cross1, cross2)
            cross1, cross2 = gen.mutate(cross1, 1), gen.mutate(cross2, 1)
            cross1, cross2 = np.append(cross1, leftover1), np.append(cross2, leftover2)
            data[np.random.randint(0, len(data))], data[np.random.randint(0, len(data))] = cross1, cross2

    return

def main():
    breed_loop(1000)
    # disp.display_ffts(ffts, len(ffts[0]))

main()

