import math  
import pyaudio  


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


def playnote(note, note_style = None):
    octave = 3
    if note == 'S2':
        note = 'S'
        octave = 4
    frequency = scale_notes[note] * (2**(octave + 1))

    p = pyaudio.PyAudio()  # initialize pyaudio

    # sampling rate
    sample_rate = 22050

    LENGTH = 1  # seconds to play sound

    frames = int(sample_rate * LENGTH)

    wavedata = ''

    # generating waves
    stream = p.open(
        format=p.get_format_from_width(1),
        channels=1,
        rate=sample_rate,
        output=True)
    for x in range(frames):
        wave = math.sin(x / ((sample_rate / frequency) / math.pi)) * 127 + 128

        if note_style == 'bytwos':
            for i in range(3):
                wave += math.sin((2 + 2**i) * x /
                                 ((sample_rate / frequency) / math.pi)) * 127 + 128
            wavedata = (chr(int(wave / 4)
                            ))

        elif note_style == 'even':
            for i in range(3):
                wave += math.sin((2 * (i + 1)) * x /
                                 ((sample_rate / frequency) / math.pi)) * 127 + 128
            wavedata = (chr(int(wave / 4)
                            ))

        elif note_style == 'odd':
            for i in range(3):
                wave += math.sin(((2 * i) + 1) * x /
                                 ((sample_rate / frequency) / math.pi)) * 127 + 128
            wavedata = (chr(int(wave / 4)
                            ))

        elif note_style == 'trem':
            wave = wave * (1 + 0.5 * math.sin((1 / 10)
                                              * x * math.pi / 180)) / 2
            wavedata = (chr(int(wave)))

        else:
            wavedata = (chr(int(wave))
                        )

        stream.write(wavedata)

    stream.stop_stream()
    stream.close()
    p.terminate()

def play_raga(raga):
    notes = raga.split(" ")[:-1]
    notes.append('S2')
    for elem in notes:
        playnote(elem)
