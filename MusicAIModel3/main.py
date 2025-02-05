import argparse
import yaml
from model import AIModel
from helper_class import HelperClass 
from midi_processor import MidiProcessor
import os

config_file = "config.yaml"

with open(config_file, 'r') as file:
    config = yaml.load(file, Loader= yaml.FullLoader)



helper = HelperClass(
    base_name=config['generating']['base_file'],
    Midi_folder=config['generating']['midi_folder']
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
    sequence_length=config['training']['sequence_length']
    )

notes = processor.load_data()

if len(notes) < config['training']['sequence_length']:
    raise ValueError(f"Die Anzahl der Noten({len(notes)}) ist kleiner als die Sequencelänge({config['sequence_length']}).")

processor.save_notes()

# Sequenzen vorbereiten
X, y = processor.prepare_sequences(notes,config['training']['sequence_length'])

n_vocab = len(set(note["pitch"] for note in notes))

aiModel = AIModel(
    sequence_length= config['training']['sequence_length'],
    n_vocab= n_vocab,
    batch_size= config['training']['batch_size'],
    musicModel= config['model']['save_path']
)

#Training (falls noch nicht trainiert)
aiModel.train(X, y, epochs=config['training']['epochs'])

# Falls ein trainiertes Modell geladen werden soll:
# ai_model.model = AIModel.load_model(config['model']['load_path'])


