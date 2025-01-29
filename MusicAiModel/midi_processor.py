import glob
from music21 import converter, note, chord
import numpy as np
import tensorflow as tf
import pickle


class MIDIProcessor:
    def __init__(self, midi_folder):
        self.midi_folder = midi_folder
        self.notes = []
        
    def load_midi_files(self):
        for file in glob.glob(self.midi_folder + "/*.mid"):
            try:
                midi = converter.parse(file)
                notes_to_parse = midi.flatten().notes  

                prev_offset = 0.0  # Für Pausenberechnung
                for element in notes_to_parse:
                    if isinstance(element, note.Note):
                        self.notes.append({
                            "pitch": str(element.pitch),
                            "duration": element.quarterLength,
                            "offset": element.offset,
                            "pause": max(0.0, element.offset - prev_offset - element.quarterLength)  # Keine negativen Pausen
                        })
                        prev_offset = element.offset
                    elif isinstance(element, chord.Chord):
                        self.notes.append({
                            "pitch": '.'.join(str(n) for n in element.normalOrder),
                            "duration": element.quarterLength,
                            "offset": element.offset,
                            "pause": max(0.0, element.offset - prev_offset - element.quarterLength)
                        })
                        prev_offset = element.offset
                    elif isinstance(element, note.Rest):
                        self.notes.append({
                            "pitch": "rest",
                            "duration": element.quarterLength,
                            "offset": element.offset,
                            "pause": 0.0  # Pausen in Rest-Objekten sind nicht relevant
                        })
                        prev_offset = element.offset
            except Exception as e:
                print(f"Fehler beim Verarbeiten der Datei {file}: {e}")
        return self.notes

    @staticmethod
    def prepare_sequences(notes, sequence_length):
        # Aufteilen der Noten in ihre Bestandteile
        pitches = [note["pitch"] for note in notes]
        durations = [note["duration"] for note in notes]
        pauses = [note["pause"] for note in notes]

        # Mapping für Pitches erstellen
        pitchnames = sorted(set(pitches))
        pitch_to_int = {note: num for num, note in enumerate(pitchnames)}

        sequences = []
        targets = []

        # Sequenzen erstellen
        for i in range(len(notes) - sequence_length):
            sequence_in_pitches = pitches[i:i + sequence_length]
            sequence_in_durations = durations[i:i + sequence_length]
            sequence_in_pauses = pauses[i:i + sequence_length]
            sequence_out = pitches[i + sequence_length]

            sequences.append({
                "pitches": [pitch_to_int[note] for note in sequence_in_pitches],
                "durations":[float(d) for d in sequence_in_durations],
                "pauses": [float(d) for d in sequence_in_pauses]
            })
            targets.append(pitch_to_int[sequence_out])

        # Sequenzen in numpy-Arrays umwandeln
        X_pitches = np.array([sequence["pitches"] for sequence in sequences], dtype=np.float32)
        X_durations = np.array([sequence["durations"] for sequence in sequences], dtype = np.float32)
        X_pauses = np.array([sequence["pauses"] for sequence in sequences], dtype=np.float32)

        # Kombinieren der Daten
        X = np.stack((X_pitches, X_durations, X_pauses), axis=-1)
        y = tf.keras.utils.to_categorical(targets, num_classes = len(pitchnames))
        
        return X, y

    def save_notes(self, output_file="notes.pkl"):
        """Speichern der Noten in einer Pickle-Datei."""
        with open(output_file, "wb") as file:
            pickle.dump(self.notes, file)
    
    def load_notes(self, input_file="notes.pkl"):
        """Laden der Noten aus einer Pickle-Datei."""
        with open(input_file, "rb") as file:
            self.notes = pickle.load(file)
