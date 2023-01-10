import math  
import numpy as np 
from scipy.io.wavfile import write

scale_notes = {
    # pitch standard A440 ie a4 = 440Hz
    'S': 16.35,
    'R1': 17.32,
    'R2': 18.35,
    'G1': 18.35,
    'R3': 19.45,
    'G2': 19.45,
    'G3': 20.6,
    'M1': 21.83,
    'M2': 23.12,
    'P': 24.5,
    'D1': 25.96,
    'D2': 27.5,
    'N1': 27.5,
    'D3': 29.14,
    'N2': 29.14,
    'N3': 30.87
}


def play_raga(arorep):
    
    wavedata = []
    notes = arorep.split(' ')[:-1]
    notes.append('S2')
    notes.append('null')
    notes.extend([elem for elem in notes[::-1]])
    notes.append('null')
    # sampling rate
    sample_rate = 44100
    gain = 0.95
    for note in notes:
        if note == 'null':
            frequency = 0
            LENGTH = 0.4
        else:
            LENGTH = 0.65  # seconds to play sound
            if note == 'S2':
                note = 'S'
                octave = 4
            else: octave = 3
            frequency = scale_notes[note] * (2**(octave + 1))
        frames = int(sample_rate * LENGTH)

        wave_before_envelope=[]
        for x in range(frames):
            wave = gain*math.sin(2 * math.pi * frequency * x * (1/sample_rate))
            wave_before_envelope.append(float(wave))
    
        wavedata.extend(np.array(wave_before_envelope)*create_envelope(len(wave_before_envelope), 3/7., 4/7., 2, 1.5))
    enveloped_data = np.array(wavedata)
    write("test.wav", sample_rate, enveloped_data.astype(np.float32))

def create_envelope(len_samples, attack_prop, decay_prop, n1, n2):
    num_attack = np.round(len_samples*attack_prop)
    num_decay = np.round(len_samples*decay_prop)
    attack_frames = np.arange(num_attack)
    decay_frames = np.arange(num_decay)
    attack_frames = ((attack_frames*1./num_attack)**(1./n1))
    decay_frames = (1 - (decay_frames*1./num_decay)**(1./n2))
    return np.append(attack_frames, decay_frames)