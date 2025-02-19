import pickle
from music21 import instrument, note, chord, stream, tempo
import numpy as np


class MusicGenerator:
    def __init__(self, sequence_length, generated_notes_count, model, bpm):
        self.sequence_length = sequence_length
        self.generated_notes_count = generated_notes_count
        self.model = model  # Neuronales Netz
        self.notes = []
        self.generated_notes = []
        self.pitchnames = []
        self.note_to_int = {}
        self.int_to_note = {}
        self.pauses = []
        self.durations = []
        self.bpm = bpm
        self.load_notes()
        

    #noten aus notes.pkl laden um sie zu verarbeiten
    def load_notes(self):
        try:
            with open("notes.pkl", "rb") as file:
                self.notes = pickle.load(file)

        # Extrahiere nur die 'pitch'-Werte für pitchnames
            self.pitchnames = sorted(set(note["pitch"] for note in self.notes))
            self.note_to_int = {note: num for num, note in enumerate(self.pitchnames)}
            self.int_to_note = {num: note for num, note in enumerate(self.pitchnames)}
            print("Notes loaded:", self.notes[:5])

        except FileNotFoundError:
            print("Fehler: 'notes.pkl' wurde nicht gefunden.")
            raise
    """Check removed output file:"""
    # noten generieren
    def generate_notes(self):
        start = np.random.randint(0, len(self.notes) - self.sequence_length)
        pattern = self.notes[start:start + self.sequence_length]  # Pattern enthält vollständige Noten-Daten


        for i in range(self.generated_notes_count):
            #pitches = [self.note_to_int[note["pitch"]] for note in pattern]
            #durations = [note["duration"] for note in pattern]
            #pauses = [note["pause"] for note in pattern]

           # prediction_input = np.array([pitches, durations, pauses]).T
            prediction_input = np.array([
            [self.note_to_int[note["pitch"]] / float(len(self.pitchnames)),
            float(note["duration"]),
            float(note["pause"])]
            for note in pattern
            ])
            prediction_input = np.reshape(prediction_input, (1, self.sequence_length, 3))
            #prediction_input[:, :, 0] /= float(len(self.pitchnames)) 
        # Vohersage
            prediction = self.model.predict(prediction_input, verbose=0)
            pitch_index = np.argmax(prediction[0][0])
            predicted_duration = prediction[1][0][0]
            predicted_pause = prediction[2][0][0]


            result = {
                "pitch": self.int_to_note[pitch_index],
                "duration": max(0.25, min(predicted_duration, 2.0)),
                "pause": max(0.0, min(predicted_pause, 1.0))
            }
            self.generated_notes.append(result)
            
            pattern.append(result)
            pattern = pattern[1:]

    def create_midi_from_notes(self):
     midi_stream1 = stream.Part()  # Melodie
     midi_stream2 = stream.Part()  # Beat
 
     # Tempo und Instrumente hinzufügen
     tempo_bpm = tempo.MetronomeMark(number= self.bpm)
     midi_stream1.append(tempo_bpm)
     midi_stream2.append(tempo_bpm)
 
     midi_stream1.append(instrument.Piano())
     midi_stream2.append(instrument.Percussion())
 
     for element in self.generated_notes:
         # Pause generieren
         if element["pause"] > 0:
             rest = note.Rest(quarterLength=element["pause"])
             midi_stream2.append(rest)
             continue
 
         # Akkorde
         if isinstance(element["pitch"], str) and ('.' in element["pitch"] or element["pitch"].isdigit()):
             chord_notes = [note.Note(int(n)) for n in element["pitch"].split('.')]
             new_chord = chord.Chord(chord_notes)
             new_chord.quarterLength = element["duration"]
             midi_stream1.append(new_chord)
         else:  # Einzelnote
             new_note = note.Note(element["pitch"])
             new_note.quarterLength = element["duration"]
             if element["duration"] < 0.5:
                 midi_stream2.append(new_note)
             else:
                 midi_stream1.append(new_note)
 
     # MIDI speichern
     song = stream.Score()
     song.insert(0, midi_stream1)
     song.insert(0, midi_stream2)
     song.write("midi", fp=output_file)



