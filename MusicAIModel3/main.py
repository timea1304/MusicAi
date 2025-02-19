import argparse
import yaml
from model import AIModel
from helper_class import HelperClass 
from midi_processor import MidiProcessor
import os
import numpy as np
from music_generator import MusicGenerator


#config laden
config_file = "MusicAIModel3/config.yaml"

with open(config_file, 'r') as file:
    config = yaml.load(file, Loader= yaml.FullLoader)

#Helper Klasse initialisieren
helper = HelperClass(
    base_name=config['generating']['base_name'],
    midi_folder=config['generating']['midi_folder']
    )

print("Lade MIDI-Dateien...")
midi_files = [
    os.path.join(config['generating']['midi_folder'],file)
    for file in os.listdir(config['generating']['midi_folder'])
    if file.endswith(".mid")or file.endswith(".midi")
]
print(f"{len(midi_files)} MIDI-Dateien gefunden.")

processor = MidiProcessor(
    csv_file=config['training']['csv_file'],
    sequence_length=config['training']['sequence_length'],
   # n_vocab=config['training']['n_vocab']
    )
print("Verarbeite Midi Dateien...")
notes = processor.load_data()

if len(notes) < config['training']['sequence_length']:
    raise ValueError(f"Die Anzahl der Noten({len(notes)}) ist kleiner als die Sequencelänge({config['sequence_length']}).")

processor.save_notes()

# Sequenzen vorbereiten
X,y = processor.process_midi()
# Berechnung von n_vocab basierend auf einzigartigen Pitches
pitch_values = [pitch for note in notes if "pitch" in note and note["pitch"] is not None for pitch in note["pitch"]] 
unique_pitches = sorted(set(pitch_values))
n_vocab = len(unique_pitches)
print(f"Berechnetes n_vocab: {n_vocab}")

# Mapping für pitch_output erstellen
#pitch_to_idx = {pitch: idx for idx, pitch in enumerate(unique_pitches)}

# Pitches in Integer-Labels umwandeln
#y["pitch_output"] = np.array([pitch_to_idx[p] for p in y["pitch_output"]], dtype=np.int32)
# Sicherstellen, dass die anderen Labels korrekt formatiert sind
#y["duration_output"] = np.array([float(d) for d in y["duration_output"] if d is not None], dtype=np.float32).reshape(-1, 1)
#y["pause_output"] = np.array([float(p) for p in y["pause_output"] if p is not None], dtype=np.float32).reshape(-1, 1)

# Debug-Ausgaben
print(f"Min Pitch: {np.min(y['pitch_output'])}, Max Pitch: {np.max(y['pitch_output'])}")
print(f"Min Duration: {np.min(y['duration_output'])}, Max Duration: {np.max(y['duration_output'])}")
print(f"Min Pause: {np.min(y['pause_output'])}, Max Pause: {np.max(y['pause_output'])}")

#KI Model initialisieren
aiModel = AIModel(
    sequence_length= config['training']['sequence_length'],
    n_vocab= n_vocab,
    batch_size= config['training']['batch_size'],
    epochs=config['training']['epochs'],
    model_path= config['model']['model_path']
)

#Training (falls noch nicht trainiert)
aiModel.train(X, y)

music_generator = MusicGenerator(
    sequence_length = config['training']['sequence_length'],
    generated_notes_count = config['training']['generated_notes_count'],
    model_path = config['model']['model_path'],
    bpm = config['training']['bpm']
)

# Falls ein trainiertes Modell geladen werden soll:
# ai_model.model = AIModel.load_model(config['model']['load_path'])


