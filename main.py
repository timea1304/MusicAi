from midi_processor import MIDIProcessor
from model import MusicGeneratorModel
from music_generator import MusicGenerator

sequence_length = 100
generated_notes_count = 300
midi_folder="Midi_files"

# MIDI-Dateien verarbeiten
processor = MIDIProcessor(midi_folder)
notes = processor.load_midi_files()
processor.save_notes()



X, y = processor.prepare_sequences(notes, sequence_length)
n_vocab = len(set(notes))


model_handler = MusicGeneratorModel(sequence_length, n_vocab,100,128)
model_handler.train( X, y)

model = model_handler.load_model(filepath='music_model.h5')

generator = MusicGenerator("midi_files", sequence_length, generated_notes_count, model)
generator.generate_notes()
generator.create_midi_from_notes("generated_music1_0.midi")

print("Lied wurde generiert. Datei wurde gespeichert.")


