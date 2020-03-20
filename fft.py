import math
import random
import wavio
import numpy as np
import scipy.fftpack
import scipy.io as sio
import scipy.io.wavfile
from playsound import playsound as ps
import struct
import display_plot
import wave as wav
import convert_sixteen
import os
from shutil import copyfile
import genetic as gen
import display_plot as disp

N = 1000

def get_clips(dir_name, max_clips):
  clips = [f for f in os.listdir(dir_name) if '.wav' in f]
  fft_data = []
  if max_clips == 1: 
    clips = [clips[np.random.randint(0, len(clips))]]
    # clips = [clip for clip in clips if clip == 'Curly_Wurlie.3.wav']
    print(f'Goal clip = {clips[0]}')
    copyfile(dir_name+clips[0], os.getcwd()+'/mod_clips/exp0_goal_'+clips[0])
  for clip in range(min(max_clips, len(clips))):
    wv = dir_name + clips[clip]
    _, data = sio.wavfile.read(wv)
    # transformed_data = np.array(scipy.fftpack.rfft(data))
    # fft_data.append(transformed_data)
    fft_data.append(data)
  return np.array(fft_data)

counter = 0

def play_fft(fft_vector):
    global counter
    counter += 1
    cwd = os.getcwd()
    # iyf = scipy.fftpack.irfft(fft_vector, 44100)
    file_path = cwd+'/mod_clips/exp' + str(counter) + '.wav'
    # write_file(file_path, iyf) 
    write_file(file_path, fft_vector) 
    return

def write_file(name, sample_data):
  sio.wavfile.write(filename=name, rate=44100, data=sample_data)
  convert_sixteen.convert_single_file(name)
  os.remove(name)

def get_temp(n): 

  T = N/n
  rand = np.random.uniform(low=0, high=0.69)
  if (math.exp(rand/T)-1) > 1: 
    print(f'annealing problem! anneal val: {(math.exp(rand/T)-1)}')
    return 1
  return math.exp(rand/T)-1

def breed_loop(N, data, gdata, save_interval):
  ffts = []
  min_errs = []
  for n in range(N):
    # print("Generation:", n)
    errors, goal = gen.fit_all(data, gdata)   
    new_data = np.zeros(np.shape(data))
    for i in range(len(data)//2): 
      if goal:
        print("Goal!")

      r = np.arange(len(errors))
      i1, i2 = np.random.choice(r, 2, p=errors)
      cross1, cross2 = gen.crossover(data[i1], data[i2])
      
      cross1, cross2 = gen.mutate(cross1, get_temp(n+1)), gen.mutate(cross2, get_temp(n+1))
      # cross1, cross2 = gen.mutate(cross1, .5), gen.mutate(cross2, .5)
      new_data[i], new_data[i+(len(data)//2)] = cross1, cross2

      if n % save_interval == 0 and i == 0:
        play_fft(cross1)
    
    data = new_data
    if n % 25 == 0:
        print(f'min error {np.amin(errors)}')
        min_errs.append(np.amin(errors))
        # ffts.append(data)
  
  return ffts, min_errs

def main(): 
  print('deleting files in mod_clips')
  mods = os.getcwd()+'/mod_clips/'
  for f in os.listdir(mods):
    os.remove(mods+f) 
  dir_name = os.getcwd() + '/1secs/'
  # dir_name = os.getcwd() + '/1sec_goals2/'
  g_dir_name = os.getcwd() + '/1sec_goals/'
  print('getting ffts from clips')
  data = get_clips(dir_name, 8657)
  np.random.shuffle(data)
  gdata = get_clips(g_dir_name, 1)
  ffts, min_errs = breed_loop(N, data, gdata, save_interval=20)
  # disp.display_ffts(ffts, len(ffts[0]))
  disp.display_fitness(min_errs, len(min_errs)) 

main()
