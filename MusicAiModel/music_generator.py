import pickle
from music21 import instrument, note, chord, stream
import numpy as np

class MusicGenerator:
    def __init__(self, sequence_length, generated_notes_count, model):
        self.sequence_length = sequence_length
        self.generated_notes_count = generated_notes_count
        self.model = model  # Neuronales Netz
        self.notes = []
        self.generated_notes = []
        self.pitchnames = []
        self.note_to_int = {}
        self.int_to_note = {}
        self.load_notes()

    #noten aus notes.pkl laden um sie zu verarbeiten
    def load_notes(self):
        
        try:
            with open("notes.pkl", "rb") as file:
                self.notes = pickle.load(file)
            self.pitchnames = sorted(set(self.notes))
            self.note_to_int = {note: num for num, note in enumerate(self.pitchnames)}
            self.int_to_note = {num: note for num, note in enumerate(self.pitchnames)}
        except FileNotFoundError:
            print("Fehler: 'notes.pkl' wurde nicht gefunden.")
            raise
    # noten generieren
    def generate_notes(self):
        start = np.random.randint(0, len(self.notes) - self.sequence_length)
        pattern = [self.note_to_int[note] for note in self.notes[start:start + self.sequence_length]]

        for i in range(self.generated_notes_count):
            prediction_input = np.reshape(pattern, (1, self.sequence_length, 1))
            prediction_input = prediction_input / float(len(self.pitchnames))
            
            prediction = self.model.predict(prediction_input, verbose=0)
            index = np.random.choice(len(prediction[0]), p=prediction[0])
            result = self.int_to_note[index]
            self.generated_notes.append(result)
            
            pattern.append(index)
            pattern = pattern[1:len(pattern)]

    def create_midi_from_notes(self, output_file="generated_music.midi"):
        midi_stream = stream.Stream()

        for element in self.generated_notes:
            if '.' in element or element.isdigit():
                chord_notes = [note.Note(int(n)) for n in element.split('.')]
                for chord_note in chord_notes:
                    chord_note.storedInstrument = instrument.Piano()
                new_chord = chord.Chord(chord_notes)
                midi_stream.append(new_chord)
            else: # Wenn es sich um eine Note und nicht um ein Akkord handelt
                new_note = note.Note(element)
                new_note.storedInstrument = instrument.Piano()
                midi_stream.append(new_note)
        #fp = file path
        midi_stream.write("midi", fp=output_file)


