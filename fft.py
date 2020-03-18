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
    wv = dir_name + clips[clip]
    _, data = sio.wavfile.read(wv)
    print(data.dtype, "dat")
    transformed_data = np.array(scipy.fftpack.rfft(data))
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
    write_file(file_path, iyf) 
    # ps(cwd+'/'+file_path) # play modified sound
    return

def write_file(name, sample_data):
  print(sample_data.dtype)
  sio.wavfile.write(filename=name, rate=44100, data=sample_data)

def breed_loop(N, data, gdata, save_interval):
  for n in range(N):
    print("Generation:", n)
    ffts = []
    new_data = np.zeros(np.shape(data))
    errors = gen.fit_all(data, gdata)
    for i in range(len(data)//2): #gen range*2 children
      r = np.arange(len(errors))
      i1, i2 = np.random.choice(r, 2, p=errors)
      cross1, cross2 = gen.crossover(data[i1], data[i2])
      # cross1, cross2 = gen.mutate(cross1, 0.8), gen.mutate(cross2, 0.8)
      new_data[i], new_data[i+(len(data)//2)] = cross1, cross2
      if n % save_interval == 0 and i == 0:
        play_fft(cross1)
        # play_fft(cross2)
    data = new_data
  return ffts

def main():
  dir_name = os.getcwd() + '/1secs/'
  g_dir_name = os.getcwd() + '/1sec_goals/'
  data = get_clips(dir_name, 1000)
  gdata = get_clips(g_dir_name, 1)
  ffts = breed_loop(1000, data, gdata, 10)
  # disp.display_ffts(ffts, len(ffts[0]))

main()

