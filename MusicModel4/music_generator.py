import pickle
import numpy as np
from music21 import instrument, note, chord, stream
import tensorflow as tf


class MusicGenerator:
    def __init__(self, sequence_length, generated_notes_count,n_vocab, model, output_file):
        self.sequence_length = sequence_length
        self.output_file = output_file
        self.generated_notes_count = generated_notes_count
        self.model = model  # Neuronales Netz
        self.notes = []
        self.n_vocab = n_vocab
        self.generated_notes = []
        self.pitchnames = []
        self.note_to_int = {}
        self.int_to_note = {}
        self.pauses = []
        self.durations = []
        self.load_notes()
        

    def load_notes(self):
        """Lädt die Noten aus der Datei 'notes.pkl'"""
        try:
            with open("notes.pkl", "rb") as file:
                self.notes = pickle.load(file)

            self.pitchnames = sorted(set(item for item in self.notes))
            self.note_to_int = {note: num for num, note in enumerate(self.pitchnames)}
            self.int_to_note = {num: note for num, note in enumerate(self.pitchnames)}
            print("Notes loaded:", self.notes[:5])

        except FileNotFoundError:
            print("Fehler: 'notes.pkl' wurde nicht gefunden.")
            raise

    # noten generieren
    def generate_notes(self):
        # Zufällige Startsequence innerhalb der Trainierten Noten wählen
        start = np.random.randint(0, len(self.notes) - 1)
        pattern = [self.note_to_int[n] for n in self.notes[start:start + self.sequence_length]]
        # Liste um neue Noten zu speichern
        generated_notes = []  

        for _ in range(self.generated_notes_count):
            prediction_input = np.reshape(pattern, (1, self.sequence_length, 1))
            prediction_input = prediction_input / float(self.n_vocab)

            prediction = self.model.predict(prediction_input, verbose=0)
            index = np.argmax(prediction)
            result = self.int_to_note[index]
            generated_notes.append(result)

            pattern.append(index)
            pattern = pattern[1:] # erstes Element entfernen
        self.generate_notes = generated_notes
        return generated_notes

    """Erstellt eine MIDI-Datei aus den generierten Noten"""
    def create_midi_from_notes(self):
        midi_stream = stream.Stream()
        
        for element in self.generated_notes:
            if '.' in element or element.isdigit():  # Es ist ein Akkord
                chord_notes = [note.Note(int(n)) for n in element.split('.')]
                for chord_note in chord_notes:
                    chord_note.storedInstrument = instrument.Piano()
                new_chord = chord.Chord(chord_notes)
                midi_stream.append(new_chord)
            else:  
                new_note = note.Note(element)
                new_note.storedInstrument = instrument.Piano()
                midi_stream.append(new_note)

        midi_stream.write("midi", fp=self.output_file)    
        print(f"MIDI-Datei gespeichert als {self.output_file}")