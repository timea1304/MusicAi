import yaml
from model import AIModel
from helper_class import HelperClass 
from midi_processor import MidiProcessor
import os
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

#KI Model initialisieren
aiModel = AIModel(
    sequence_length= config['training']['sequence_length'],
    n_vocab= n_vocab,
    batch_size= config['training']['batch_size'],
    epochs=config['training']['epochs'],
    model_path= config['model']['model_path']
)
print("Model traininieren...")
#Training (falls noch nicht trainiert)
aiModel.train(X,y)

# Falls ein trainiertes Modell geladen werden soll:
# ai_model.model = AIModel.load_model(config['model']['load_path'])

music_generator = MusicGenerator(
    sequence_length = config['training']['sequence_length'],
    generated_notes_count = config['training']['generated_notes_count'],
    model_path = config['model']['model_path'],
    n_vocab=n_vocab,
    output_file=helper.get_new_filename()
)
music_generator.load_notes()
music_generator.generate_notes()
music_generator.create_midi_from_notes()



