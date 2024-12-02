import tensorflow as tf
from music21 import instrument, note, chord, stream
import numpy as np
import pickle
model = tf.keras.models.load_model("music_model.keras")

with open("notes.pkl", "rb") as file: 
    notes = pickle.load(file)

pitchnames = sorted(set(notes))
note_to_int = {note: num for num, note in enumerate(pitchnames)}
int_to_note = {num:note for num, note in enumerate(pitchnames)}

sequence_length = 50
generated_notes_count = 500

start = np.random.randint(0,len(notes) - sequence_length)
pattern = [note_to_int[n] for n in notes [start:start + sequence_length]]

generated_notes = []
for i in range(generated_notes_count):
    prediction_input = np.reshape(pattern, (1, sequence_length, 1))
    prediction_input = prediction_input/ float(len(pitchnames))

    prediction = model.predict(prediction_input, verbose = 0)
    index = np.argmax(prediction)
    result = int_to_note[index]
    generated_notes.append(result)

    pattern.append(index)
    pattern = pattern[1:len(pattern)]

def create_midi_from_notes(notes, output_file="generated_music3.mid"):
    midi_stream = stream.Stream()

    for element in notes:
        if '.' in element or element.isdigit():
            chord_notes = element.split('.')
            chord_notes = [note.Note(int(n)) for n in chord_notes]
            for chord_note in chord_notes:
                chord_note.storedInstrument = instrument.Guitar()
            new_chord = chord.Chord(chord_notes)
            midi_stream.append(new_chord)
        else:
            new_note = note.Note(element)
            new_note.storedInstrument = instrument.Guitar()
            midi_stream.append(new_note)

    midi_stream.write("midi", fp=output_file)

create_midi_from_notes(generated_notes)
print("Die Musik wurde als 'generated_music.mid' gespeichert.")