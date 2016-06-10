import mock
import sys
sys.modules.update((mod_name, mock.Mock()) for mod_name in ['matplotlib', 'matplotlib.pyplot', 'matplotlib.image'])

import librosa


EX_FILEPATH = 'songs/imitosis.wav'


def get_song_data(filepath):
    y, sr = librosa.load(filepath)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    song_length_ms = len(y) / float(sr) * 1000
    chromagram = librosa.feature.chroma_stft(y=y, sr=sr).T 	# transpose
    chroma_frame_length_ms = song_length_ms / float(chromagram.shape[0])
    return {
        'beat_times': [round(t, 2) for t in beat_times],
        'song_length_ms': song_length_ms,
        'chromagram': chromagram,
        'chroma_frame_length_ms': chroma_frame_length_ms
    }
