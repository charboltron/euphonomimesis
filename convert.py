import scipy.io as sio
import scipy.io.wavfile
import librosa
import os

def write_file(name, sample_data):
  sio.wavfile.write(filename=name, rate=44100, data=sample_data)

def read_files():
  cwd = os.getcwd()
  clip_dir = os.listdir(cwd+'/1secs/')
  clips = [f for f in clip_dir if '.wav' in f]
  for clip in range(len(clips)):
    print(clips[clip])
    wv = cwd+'/1secs/'+clips[clip]
    y, sr = librosa.load(wv, sr=44100, mono=True)
    write_file(wv, y)


read_files()
