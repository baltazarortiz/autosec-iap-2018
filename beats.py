# Beat tracking example
from __future__ import print_function
import librosa

import numpy as np

# 1. Get the file path to the included audio example
filename = 'funfunfun.mp3'

# 2. Load the audio as a waveform `y`
#    Store the sampling rate as `sr`
y, sr = librosa.load(filename)

# # 3. Run the default beat tracker
# tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
#
# print('Estimated tempo: {:.2f} beats per minute'.format(tempo))
#
# # 4. Convert the frame indices of beat events into timestamps
# beat_times = librosa.frames_to_time(beat_frames, sr=sr)
#
# print('Saving output to beat_times.csv')
# librosa.output.times_csv('beat_times.csv', beat_times)

D = librosa.stft(y)
print(D)

speed = np.abs(D[0])
rev   = np.abs(D[1])

speed /= np.max(speed, axis=0)
speed *= 140
np.savetxt('speed.csv', speed)

rev /= np.max(rev, axis=0)
rev *= 8

np.savetxt('rev.csv', rev)
