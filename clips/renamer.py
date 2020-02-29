import os 
import shutil

cwd = os.getcwd()
clip_dir = cwd+'/clips/'

[os.rename(f, f.replace(' ', '_')) for f in os.listdir() if '.wav' in f]
