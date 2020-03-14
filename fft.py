import numpy as np
import scipy.fftpack
import scipy.io as sio
import scipy.io.wavfile
from playsound import playsound as ps
import struct
import display_plot
import wave as wav
import os
import genetic as gen
import display_plot as disp

def get_clips(dir_name, max_clips):
  clips = [f for f in os.listdir(dir_name) if '.wav' in f]
  fft_data = []
  for clip in range(min(max_clips, len(clips))):
    print(clips[clip])
    wv = dir_name + clips[clip]
    _, data = sio.wavfile.read(wv)
    transformed_data = np.array(scipy.fftpack.rfft(data))
    print(len(transformed_data))
    fft_data.append(transformed_data)
  return np.array(fft_data)


counter = 0

def play_fft(fft_vector):
    global counter
    counter += 1
    cwd = os.getcwd()
    iyf = scipy.fftpack.irfft(fft_vector, 44100)
    file_path = 'mod_clips/exp' + str(counter) + '.wav'
    # write_file(file_path, iyf, params) 
    write_file_new(file_path, iyf) 
    # ps(cwd+'/'+file_path) # play modified sound
    return

def write_file(name, sample_data):
  sio.wavfile.write(filename=name, rate=44100, data=sample_data)
  print("success writing")

def breed_loop(N, data, gdata):
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
            #if n % 5 == 0 and i % 10 == 0:
                #play_fft(cross1)
                #play_fft(cross2)
    return ffts

def main():
  dir_name = os.getcwd() + '/1secs/'
  g_dir_name = os.getcwd() + '/1sec_goals/'
  data = get_clips(dir_name, 100)
  gdata = get_clips(g_dir_name, 1)
  ffts = breed_loop(1000, data, gdata)
  # disp.display_ffts(ffts, len(ffts[0]))

main()

