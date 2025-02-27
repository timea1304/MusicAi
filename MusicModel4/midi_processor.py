import os
from mido import MidiFile
import numpy as np
import tensorflow as tf
import glob
from music21 import converter
import pretty_midi
import pickle

class MidiProcessor:
    def __init__(self, csv_file, sequence_length, midi_files_path):
        self.csv = csv_file
        self.sequence_length = sequence_length
        self.midi_files_path = midi_files_path
        self.notes=[]
                

    def load_midi_files(self):
       
        for file in os.listdir(self.midi_files_path):
            if not (file.endswith('.mid') or file.endswith('.midi')):
                continue

            file_path = os.path.join(self.midi_files_path, file)

            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Datei {file_path} nicht gefunden. Überprüfe den Pfad")

            print(f"Parsing {file_path}")
            try:
                midi = converter.parse(file)
                self.extract_notes(midi)
            except Exception as e:
                print(f"Fehler beim extracten der datei {file_path}: {e}")


    def extract_notes(self, midi):
        notes = {
            'pitch':[],
            'start':[],
            'end': [],
            'duration':[]
            }
        prev_start = 0

        try:
            
            pm = pretty_midi.PrettyMIDI(midi)
            if not pm.instruments:
                raise ValueError("Keine Instrumente in der MIDI-Datei gefunden.")
        
            instrument = pm.instruments[0]
            sorted_notes = sorted(instrument.notes, key = lambda note: note.start)
            prev_start = sorted_notes[0].start

            for note in sorted_notes:
                start = note.start
                end = note.end
                notes['pitch'].append(note.pitch)
                notes['start'].append(start)
                notes['end'].append(end)
                notes['step'].append(start - prev_start)
                notes['duration'].append(end - start)
                #vorherige start ist der jetzige start
                prev_start = start
            #speichern der Noten
            self.notes.append(notes) 
        except Exception as e:
               print(f"Fehler beim extracten der Noten: {e}")

    """
    Daten für das Trainieren vorbereiten
    """
    def prepare_sequences(self, notes, n_vocab):
        pitchnames = sorted(set(notes))

        if not self.notes:
            raise ValueError("Fehler: `self.notes` ist leer. Überprüfe `load_data()`.")
        
        if len(self.notes) < self.sequence_length:
            raise ValueError(f"Fehler: `self.sequence_length` ({self.sequence_length}) ist größer als die Anzahl der geladenen Noten ({len(self.notes)}).")
        
        
        print(f"Anzahl geladener Noten: {len(self.notes)}")
        print(f"Erwartete Sequenzlänge: {self.sequence_length}")
        print(f"Berechneter Bereich: {len(self.notes) - self.sequence_length}")

        note_to_int = dict((note, number) for number, note in enumerate(pitchnames))
    
    
        sequences_in = []
        targets = []
        for i in range(len(notes) - self.sequence_length):
            sequence_in = notes[i:i + self.sequence_length]
            sequence_out = notes[i + self.sequence_length]
            sequences_in.append([note_to_int[char] for char in sequence_in])
            targets.append(note_to_int[sequence_out])
        # sequence_ in in ein geeignetes Format formatieren, damit das Modell damit
        #arbeiten kann
        sequence_in =  np.reshape(sequences_in, (len(sequences_in), self.sequence_length, 1))
        sequences_in = np.array(sequences_in) / float(n_vocab)
        targets = tf.keras.utils.to_categorical(targets)

        return sequences_in, targets
    

    def save_notes(self, output_file="notes.pkl"):
        """Speichern der Noten in einer Pickle-Datei."""
        with open(output_file, "wb") as file:
            pickle.dump(self.notes, file)

    def load_notes(self, input_file="notes.pkl"):
        """Laden der Noten aus einer Pickle-Datei."""
        with open(input_file, "rb") as file:
            self.notes = pickle.load(file)

          
