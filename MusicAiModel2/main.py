import os
from midi_processor import MidiProcessor
from model import MusicModelAI
from music_generator import MusicGenerator
from helper_class import HelperClass
#import csv
#import pickle

#Anpassbare Daten zum Starten des Projekts
n_vocab = 128
sequence_length = 128
generated_notes_count = 150
epochs = 5
batch_size = 128
midi_folder = "MusicAiModel\\Midi_files\\Hardstyle"
aiModel = "hardstyle_model6.keras"
feedback_file = "bewertung.csv"
base_name = "mido_Hardstyle_01_"
midi_folder = "generated_Midi"

helper = HelperClass(feedback_file, base_name, midi_folder)

print("Lade MIDI-Dateien...")

midi_files = [
    os.path.join(midi_folder,file)
    for file in os.listdir(midi_folder)
    if file.endswith(".mid")or file.endswith(".midi")
]

#notes = processor.load_midi_files()
if not os.path.exists(midi_folder):
    raise ValueError(f"Der Ordner {midi_folder} existiert nicht. Bitte überprüfe den Pfad.")
print(f"Gefundene MIDI-Dateien: {midi_files}")

if not midi_files:
    raise ValueError(f"Keine Midi Dateiein im Ordner {midi_folder}")


processor = MidiProcessor(sequence_length, midi_folder)
notes = processor.load_midi_files(midi_files)

if len(notes) < sequence_length:
    raise ValueError(f"Die Anzahl der Noten({len(notes)})ist kleiner als die Sequence_length ({sequence_length})")


#processor.save_notes()
print("Trainingsdaten vorbereiten....")
train_data = processor.prepare_data(notes)
train_X = train_data[:,:-1,:]
train_Y_raw = train_data[:,-1,:]
train_Y = to_categorical(train_Y_raw, num_classes = n_vocab)

print("Neues Model oder Modell laden")
model_handler = MusicModelAI(epochs,batch_size,sequence_length,aiModel,n_vocab)

#processor.prepare_data()
if os.path.exists(aiModel):
    print(f"Lade vorhandenes Modell: {aiModel}")
    model = model_handler.load_model(filepath=aiModel)
else:
    print("Trainiere ein neues Modell.")
    model_handler.model.fit(train_X,train_Y,epochs = epochs, batch_size = batch_size)
    #model_handler.model.fit(epochs = epochs, batch_size = batch_size)
    model_handler.save_model()

print("Generiere ein Lied...")
#seed_sequence = train_X[0]
generator = MusicGenerator(model_handler.model, template=None)
#generated_notes = generator.generate_song(seed_sequence, generated_notes_count)
generated_notes = generator.generate_song(generated_notes_count)


filename = helper.get_new_filename()
helper.save_midi_file(generated_notes_count,filename)
#generator.generate_song()
print(f"Lied wurde generiert. Datei {filename} wurde gespeichert.")


helper.music_rating(filename, feedback_file)
positive_notes = helper.train_with_rating(notes)
if positive_notes:
    print("Trainiere Modell mit positiv ausgefallenen DAten...")
    positive_data = processor.prepare_data(positive_notes)
    train_X = positive_data[:,:-1,:]
    train_Y = positive_data[:,-1,:]
    model_handler.model.fit(train_X, train_Y, epochs=epochs, batch_size=batch_size)
    model_handler.save_model()
helper.train_with_rating()
