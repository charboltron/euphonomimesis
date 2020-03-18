import os
import soundfile

# def convertAllFilesInDirectoryTo16Bit(directory):
#     for file in os.listdir(directory):
#         if(file.endswith('.wav')):
#             nameSolo = file.rsplit('.', 1)[0]
#             print(directory + nameSolo )
#             data, samplerate = soundfile.read(directory + file)                

#             soundfile.write(directory+'16bit_mod_clips/' + nameSolo + '16BIT.wav', data, samplerate, subtype='PCM_16')
#             print("converting " + file + "to 16 - bit")

def convert_single_file(file):
    nameSolo = file.rsplit('.', 1)[0]
    data, samplerate = soundfile.read(file)                
    soundfile.write(nameSolo + '_16bit.wav', data, samplerate, subtype='PCM_16')
    # print("converting " + file + "to 16 - bit")

