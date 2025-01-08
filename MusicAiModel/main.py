import os
from midi_processor import MIDIProcessor
from model import MusicGeneratorModel
from music_generator import MusicGenerator
import pickle
import csv


sequence_length = 100
generated_notes_count = 100
epochs = 100
batch_size = 128
midi_folder = "MusicAiModel\Midi_files\Hardstyle"
aiModel = "hardstyle_model.keras"
feedback_file = "bewertung.csv"


def get_new_filename(base_name, folder="generated_Midi"):
    version = 1
    while os.path.exists(os.path.join(folder, f"{base_name}_{version}.midi")):
        version += 1
    return os.path.join(folder, f"{base_name}_{version}.midi")

def music_rating(filename, feedback_file):
    """Funktion zur Bewertung generierter Musik."""
    try:
        rating = int(input("Bewerten: (1 = schlecht|5 = sehr gut): "))
        if 1 <= rating <= 5:
            with open(feedback_file, "a") as file:
                writer = csv.writer(file)
                writer.writerow([filename, rating])
            print("Bewertung gespeichert.")
        else:
            print("Ungültige Bewertung. Bitte eine Zahl zwischen 1 und 5 eingeben.")
    except ValueError:
        print("Ungültige Eingabe. Bitte eine Zahl eingeben.")
    
def train_with_rating(actual_notes, feedback_file, sequence_length):
    positive_notes = []
    try:
        with open(feedback_file, "r") as file:
            reader = csv.reader(file)
            feedback = list(reader)
        for row in feedback:
            if len(row) != 2:  # Überprüfe, ob genau zwei Werte vorhanden sind
                print(f"Ungültige Zeile übersprungen: {row}")
                continue
            filename, rating = row
            try:
                if int(rating) >= 4: 
                    # Lade die entsprechenden Noten
                    with open(filename.replace('.midi', '.pkl'), "rb") as notes_file:
                        positive_notes.extend(pickle.load(notes_file))
            except (ValueError, FileNotFoundError) as e:
                print(f"Fehler beim Verarbeiten der Datei {filename}: {e}")
    except FileNotFoundError:
        print("Feedback-Datei nicht gefunden.")
    
    all_notes = actual_notes + positive_notes
    X, y = MIDIProcessor.prepare_sequences(all_notes, sequence_length)
    return X, y



# MIDI-Dateien verarbeiten
processor = MIDIProcessor(midi_folder)
notes = processor.load_midi_files()
if not notes:
    raise ValueError(f"Keine MIDI-Dateien im Ordner {midi_folder} gefunden.")
if len(notes) < sequence_length:
    raise ValueError(f"Die Anzahl der Noten ({len(notes)}) ist kleiner als die Sequenzlänge ({sequence_length}).")

processor.save_notes()

# Sequenzen vorbereiten
n_vocab = len(set(notes))
X, y = processor.prepare_sequences(notes, sequence_length)


model_handler = MusicGeneratorModel(sequence_length, n_vocab,batch_size, aiModel )
if os.path.exists(aiModel):
    print(f"Lade vorhandenes Modell: {aiModel}")
    model = model_handler.load_model(filepath=aiModel)
else:
    print("Trainiere ein neues Modell.")
    model_handler.train(X, y)
    model = model_handler.model


filename = get_new_filename("genHardstyle_music")
generator = MusicGenerator(sequence_length, generated_notes_count, model)
generator.generate_notes()
generator.create_midi_from_notes(filename)
print(f"Lied wurde generiert. Datei {filename} wurde gespeichert.")

music_rating(filename, feedback_file)
X, y = train_with_rating(notes, feedback_file, sequence_length)
if input("Weitertrainieren? (y/n): ").lower() == 'y':
    additional_epochs = int(input("Wie viele Epochen? "))
    model_handler.train(X, y, epochs=additional_epochs)


print(set(notes))
print(len(notes))
