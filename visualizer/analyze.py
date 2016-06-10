import mock
import sys
sys.modules.update((mod_name, mock.Mock()) for mod_name in ['matplotlib', 'matplotlib.pyplot', 'matplotlib.image'])

import numpy as np
import librosa


def get_song_data(filepath):
    y, sr = librosa.load(filepath)
    song_length_ms = len(y) / float(sr) * 1000
    S = np.abs(librosa.stft(y)).T
    rmse = librosa.feature.rmse(y=y)
    logamp = librosa.logamplitude(S ** 2)
    amplitudes = np.array([y[i] for i in np.arange(0, len(y), 512)])
    y_harmonic, y_percussive = librosa.effects.hpss(y)
    chromagram = librosa.feature.chroma_stft(y=y_harmonic, sr=sr).T
    chroma_frame_length_ms = song_length_ms / float(chromagram.shape[0])
    return {
        'song_length_ms': song_length_ms,
        'spectrogram': S,
        'rmse': rmse[0],
        'logamp': logamp,
        'amplitudes': amplitudes,
        'chromagram': chromagram,
        'chroma_frame_length_ms': chroma_frame_length_ms
    }
