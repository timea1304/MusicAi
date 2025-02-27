import glob
import pretty_midi
import pandas as pd
import collections
import numpy as np

midi_path = 'MusicAiModel\Midi_files\Hardstyle'

for file in glob.glob(midi_path):
#filenames = glob.glob(str(midi_path/'*.mid*'))
    print('Number of files:', len(file))
            
    sample_file = file
    print(sample_file)

    pm = pretty_midi.PrettyMIDI(sample_file)

    print('Number of instruments:', len(pm.instruments))
    instrument = pm.instruments[0]
    instrument_name = pretty_midi.program_to_instrument_name(instrument.program)
    print('Isntrument name:', instrument_name)

    for i, note in enumerate(instrument.notes[:10]):
        note_name = pretty_midi. note_number_to_name(note.pitch)
        duration = note.end - note.start
        print(f'{i}: pitch={note.pitch}, note_name ={note_name},'
            f' duration = {duration:.4f}')
        
"""  def midi_to_notes(midi_file: str) -> pd.DataFrame:
        pm = pretty_midi.PrettyMIDI(midi_file)
        instrument = pm.instruments[0]
        notes = collections.defaultdict(list)
        #Sort the notes by start time
        sorted_notes = sorted(instrument.notes, key=lambda note: note.start)
        prev_start = sorted_notes[0].start

        for note in sorted_notes:
        start = note.start
        end = note.end
        notes['pitch'].append(note.pitch)
        notes['start'].append(start)
        notes['end'].append(end)
        notes['step'].append(start - prev_start)
        notes['duration'].append(end - start)
        prev_start = start
        return pd.DataFrame({name: np.array(value) for name, value in notes.items()})

    raw_notes = midi_to_notes(file)
    raw_notes.head()

    get_note_names = np.vectorize(pretty_midi.note_number_to_name)
    sample_note_names = get_note_names(raw_notes['pitch'])"""