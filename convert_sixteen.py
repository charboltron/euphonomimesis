import os
import soundfile

def convert_single_file(file):
    nameSolo = file.rsplit('.', 1)[0]
    data, samplerate = soundfile.read(file)                
    soundfile.write(nameSolo + '_16bit.wav', data, samplerate, subtype='PCM_16')

