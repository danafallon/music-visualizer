import mock
import sys
sys.modules.update((mod_name, mock.Mock()) for mod_name in ['matplotlib', 'matplotlib.pyplot', 'matplotlib.image'])

import librosa


EX_FILEPATH = 'songs/imitosis.mp3'


def get_song_data(filepath):
    y, sr = librosa.load(filepath)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    return {
        'beat_times': [round(t, 2) for t in beat_times],
        'song_length': len(y) / sr
    }
