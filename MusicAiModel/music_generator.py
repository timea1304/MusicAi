import pickle
from music21 import instrument, note, chord, stream, tempo
import numpy as np
import random

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

    def create_midi_from_notes(self, output_file="generated_music.midi", bpm = 160):
        midi_stream1 = stream.Part() # melodie
        midi_stream2 = stream.Part() # beat
     

        tempo_bpm = tempo.MetronomeMark(number=bpm)
        midi_stream1.append(tempo_bpm)
        midi_stream2.append(tempo_bpm)
      

        midi_stream1.append(instrument.Piano())
        midi_stream2.append(instrument.Percussion())
       

        for element in self.generated_notes:
            if random.random() < 0.1:  # 10% Wahrscheinlichkeit für eine Pause
                rest = note.Rest(quarterLength=0.5)  # Dauer der Pause
                random.choice([midi_stream1, midi_stream2]).append(rest)
                continue

            if '.' in element or element.isdigit():
                chord_notes = [note.Note(int(n)) for n in element.split('.')]
               # for chord_note in chord_notes:
                #    chord_note.storedInstrument = instrument.Sampler()
                new_chord = chord.Chord(chord_notes)
                new_chord.quarterLength = random.choice([0.25,0.5,1.0])
                midi_stream1.append(new_chord)
                #midi_stream1.append(new_chord)
            else: # Wenn es sich um eine Note und nicht um ein Akkord handelt
                new_note = note.Note(element)
                new_note.quarterLength = random.choice([0.25,0.5,1.0])
                if new_note.quarterLength < 0.5:
                   midi_stream2.append(new_note)
                else:
                   midi_stream1.append(new_note)
               # new_note.storedInstrument = instrument.Sampler()
                #midi_stream1.append(new_note)
                #random.choice([midi_stream1,midi_stream2]).append(new_note)

       
        song = stream.Score()
        song.insert(0,midi_stream1)
        song.insert(0,midi_stream2)
        #fp = file path
        song.write("midi", fp=output_file)    


