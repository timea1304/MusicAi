import glob
from music21 import converter, note, chord
import numpy as np
import tensorflow as tf
import pickle
import pretty_midi



class MIDIProcessor:
    def __init__(self, midi_folder):
        self.midi_folder = midi_folder
        self.notes = []
        
    def load_midi_files(self):
        for file in glob.glob(self.midi_folder + "/*.mid"):
            try:
                midi = converter.parse(file)
                notes_to_parse = midi.flatten().notes  
                for element in notes_to_parse:
                    if isinstance(element, note.Note):
                        self.notes.append(str(element.pitch))
                    elif isinstance(element, chord.Chord):
                        self.notes.append('.'.join(str(n) for n in element.normalOrder))
            except Exception as e:
                print(f"Fehler beim Verarbeiten der Datei {file}: {e}")
        return self.notes

    @staticmethod
    def prepare_sequences(notes, sequence_length):
        pitchnames = sorted(set(notes))
        note_to_int = dict((note, number) for number, note in enumerate(pitchnames))
        
        sequences = []
        targets = []
        for i in range(len(notes) - sequence_length):
            sequence_in = notes[i:i + sequence_length]
            sequence_out = notes[i + sequence_length]
            sequences.append([note_to_int[char] for char in sequence_in])
            targets.append(note_to_int[sequence_out])
        
        X = np.reshape(sequences, (len(sequences), sequence_length, 1))
        X = X / float(len(pitchnames))
        y = tf.keras.utils.to_categorical(targets)
        
        return X, y

    # Noten wieder in noten.pkl speichern
    def save_notes(self, output_file="notes.pkl"):
        with open(output_file, "wb") as file:
            pickle.dump(self.notes, file)
    
    def load_notes(self, input_file="notes.pkl"):
        with open(input_file, "rb") as file:
            self.notes = pickle.load(file)
