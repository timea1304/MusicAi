import tensorflow as tf
from music21 import converter, note, chord
import numpy as np
import glob
import pickle

# 1. Vorverarbeitung der MIDI-Dateien
def load_midi_files():
    guitar_notes = []
    drum_notes = []
    
    for file in glob.glob("midi_files/*.mid"):
        midi = converter.parse(file)
        
        # Gitarren- und Schlagzeugspuren extrahieren
        for part in midi.parts:
            if 'Guitar' in part.partName:  # Prüfen, ob es eine Gitarrenspur ist
                for element in part.flat.notes:
                    if isinstance(element, note.Note):
                        guitar_notes.append(str(element.pitch))
                    elif isinstance(element, chord.Chord):
                        guitar_notes.append('.'.join(str(n) for n in element.normalOrder))
            elif 'Drum' in part.partName:  # Prüfen, ob es eine Schlagzeugspur ist
                for element in part.flat.notes:
                    if isinstance(element, note.Note):
                        drum_notes.append(str(element.pitch))
                    elif isinstance(element, chord.Chord):
                        drum_notes.append('.'.join(str(n) for n in element.normalOrder))
    
    # Speichern der Noten für spätere Nutzung
    with open('guitar_notes.pkl', 'wb') as filepath:
        pickle.dump(guitar_notes, filepath)
    with open('drum_notes.pkl', 'wb') as filepath:
        pickle.dump(drum_notes, filepath)
    
    return guitar_notes, drum_notes

# 2. Vorbereitung der Sequenzen für das Training
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
    
    return X, y, len(pitchnames)

# 3. Modell für Mehrspur-Generierung
def create_multitrack_model(sequence_length, n_vocab):
    input_layer = tf.keras.layers.Input(shape=(sequence_length, 1))
    
    # Gitarren-Spur
    lstm_guitar = tf.keras.layers.LSTM(256, return_sequences=True)(input_layer)
    lstm_guitar = tf.keras.layers.Dropout(0.3)(lstm_guitar)
    lstm_guitar = tf.keras.layers.LSTM(256, return_sequences=True)(lstm_guitar)
    lstm_guitar = tf.keras.layers.Dropout(0.3)(lstm_guitar)
    lstm_guitar = tf.keras.layers.LSTM(128)(lstm_guitar)
    lstm_guitar_output = tf.keras.layers.Dense(n_vocab, activation='softmax', name="guitar_output")(lstm_guitar)
    
    # Schlagzeug-Spur
    lstm_drum = tf.keras.layers.LSTM(256, return_sequences=True)(input_layer)
    lstm_drum = tf.keras.layers.Dropout(0.3)(lstm_drum)
    lstm_drum = tf.keras.layers.LSTM(256, return_sequences=True)(lstm_drum)
    lstm_drum = tf.keras.layers.Dropout(0.3)(lstm_drum)
    lstm_drum = tf.keras.layers.LSTM(128)(lstm_drum)
    lstm_drum_output = tf.keras.layers.Dense(n_vocab, activation='softmax', name="drum_output")(lstm_drum)
    
    model = tf.keras.models.Model(inputs=input_layer, outputs=[lstm_guitar_output, lstm_drum_output])
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    
    return model

# 4. Training des Modells
def train_model(model, X_guitar, y_guitar, X_drum, y_drum, epochs=100, batch_size=64):
    model.fit([X_guitar, X_drum], [y_guitar, y_drum], epochs=epochs, batch_size=batch_size)
    model.save("music_multitrack_model.h5")

# 5. Generieren von Musik
def generate_music_multitrack(model, start_sequence, sequence_length, n_vocab, int_to_note):
    prediction_output_guitar = []
    prediction_output_drum = []
    
    sequence_in = start_sequence
    for _ in range(500):  # Anzahl der Noten, die generiert werden sollen
        prediction_input = np.reshape(sequence_in, (1, sequence_length, 1))
        prediction_input = prediction_input / float(n_vocab)
        
        prediction_guitar, prediction_drum = model.predict(prediction_input, verbose=0)
        
        index_guitar = np.argmax(prediction_guitar)
        index_drum = np.argmax(prediction_drum)
        
        result_guitar = int_to_note[index_guitar]
        result_drum = int_to_note[index_drum]
        
        prediction_output_guitar.append(result_guitar)
        prediction_output_drum.append(result_drum)
        
        sequence_in = np.append(sequence_in, [[index_guitar]], axis=0)
        sequence_in = sequence_in[1:len(sequence_in)]
    
    return prediction_output_guitar, prediction_output_drum

# Hauptskript
sequence_length = 100
guitar_notes, drum_notes = load_midi_files()
X_guitar, y_guitar, n_vocab_guitar = prepare_sequences(guitar_notes, sequence_length)
X_drum, y_drum, n_vocab_drum = prepare_sequences(drum_notes, sequence_length)

# Erstellen und Trainieren des Modells
model = create_multitrack_model(sequence_length, max(n_vocab_guitar, n_vocab_drum))
train_model(model, X_guitar, y_guitar, X_drum, y_drum)

# Generieren neuer Musik
start_sequence = X_guitar[0]  # Beispiel: Anfangssequenz von Gitarrendaten
int_to_note_guitar = {number: note for note, number in prepare_sequences(guitar_notes, sequence_length)[2].items()}
int_to_note_drum = {number: note for note, number in prepare_sequences(drum_notes, sequence_length)[2].items()}

prediction_output_guitar, prediction_output_drum = generate_music_multitrack(model, start_sequence, sequence_length, n_vocab_guitar, int_to_note_guitar)

print("Generated Guitar Notes:", prediction_output_guitar)
print("Generated Drum Notes:", prediction_output_drum)
