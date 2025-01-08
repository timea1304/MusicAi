import tensorflow as tf
from music21 import instrument, note, chord, stream
import numpy as np
import pickle

# Laden des trainierten Modells und der Noten
model = tf.keras.models.load_model("music_model.keras")

# Startsequenz laden und vorbereiten
with open("MusicAiModel/notes.pkl", "rb") as file:  # Noten werden hier gespeichert, wenn ein Training des modells statt findet
    notes = pickle.load(file)

# umwandeln von noten to int und int to note
pitchnames = sorted(set(notes))
note_to_int = {note: num for num, note in enumerate(pitchnames)}
int_to_note = {num: note for num, note in enumerate(pitchnames)}

# Länge der Startsequenz und generierten Noten
sequence_length = 300
generated_notes_count = 500  # Anzahl generierten Noten, in der End Midi file

# Zufällige Startsequence innerhalb der Trainierten Noten wählen
start = np.random.randint(0, len(notes) - sequence_length)
pattern = [note_to_int[n] for n in notes[start:start + sequence_length]]

# neue Noten generieren
generated_notes = []
for i in range(generated_notes_count):
    prediction_input = np.reshape(pattern, (1, sequence_length, 1))
    prediction_input = prediction_input / float(len(pitchnames))
    
    prediction = model.predict(prediction_input, verbose=0)
    index = np.argmax(prediction)
    result = int_to_note[index]
    generated_notes.append(result)
    
    pattern.append(index)
    pattern = pattern[1:len(pattern)]

# Die Noten in eine MIDI-Datei umwandeln
def create_midi_from_notes(notes, output_file="generated_music7.mid"):
    midi_stream = stream.Stream()
    
    for element in notes:
        if '.' in element or element.isdigit():  # Es ist ein Akkord
            chord_notes = element.split('.')
            chord_notes = [note.Note(int(n)) for n in chord_notes]
            for chord_note in chord_notes:
                chord_note.storedInstrument = instrument.Piano()
            new_chord = chord.Chord(chord_notes)
            midi_stream.append(new_chord)
        else:  
            new_note = note.Note(element)
            new_note.storedInstrument = instrument.Piano()
            midi_stream.append(new_note)

    midi_stream.write("midi", fp=output_file)

# Speichern der generierten Noten als MIDI-Datei
create_midi_from_notes(generated_notes)
print("Die Musik wurde als 'generated_music.mid' gespeichert.")
