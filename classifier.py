import tensorflow as tf
from music21 import converter, note, chord
import numpy as np
import glob
import pickle

def load_midi_files():
    notes=[]
    for file in glob.glob("Midi_files/*.mid"):
        midi = converter.parse(file)
        notes_to_parse = midi.flat.notes
        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))
    return notes

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


def create_model(sequence_length, n_vocab):
    model = tf.keras.Sequential([
        tf.keras.layers.LSTM(256, input_shape=(sequence_length, 1), return_sequences=True),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.LSTM(256, return_sequences=True),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.LSTM(128),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dense(n_vocab, activation='softmax')
    ])
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    return model


def train_model(model, X, y, epochs=200, batch_size=64):
    model.fit(X, y, epochs=epochs, batch_size=batch_size)
    model.save("music_model.keras")

sequence_length = 100
notes = load_midi_files()
X, y = prepare_sequences(notes, sequence_length)
model = create_model(sequence_length, len(set(notes)))
train_model(model, X, y)

with open("notes.pkl", "wb") as file:
    pickle.dump(notes, file)