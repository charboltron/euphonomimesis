
for i in range(len(v1)//(2*r)):
    print(r)
    if i >= len(v1)//(2*r):
      print(aList)
    aList.append(v1[i:i+r])
    aList.append(v2[i+r:i+2*r])
    bList.append(v2[i:i+r])
    bList.append(v1[i+r:i+2*r])
  aList.append(v1[len(v1) % r])
  bList.append(v1[len(v1) % r])
  print(len(v1), len(aList), len(v2), len(bList))

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
        am = max(samples)
        if ((-0x7fff - 1) > am or am > 0x7fff):
          print("Jesus Christ! It's so big!", am)
    return np.array(fft_data), params, fft_goal


def write_file(name, sample_data, params):
    wav_file = wav.open(name, 'w')
    wav_file.setparams(params)
    for samp in sample_data:
        if ((-0x7fff - 1) > int(samp) or int(samp) > 0x7fff):
            print(f'whats this? {int(samp)}')
        else:
          wav_file.writeframes(struct.pack('h', int(samp)))
