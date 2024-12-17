from midi_processor import MIDIProcessor
from model import MusicGeneratorModel
from music_generator import MusicGenerator

sequence_length = 100
# MIDI-Dateien verarbeiten
processor = MIDIProcessor(midi_folder="midi_files")
notes = processor.load_midi_files()
X, y = processor.prepare_sequences(notes, sequence_length)

n_vocab = len(set(notes))
model_handler = MusicGeneratorModel(sequence_length, n_vocab)

model = model_handler.create_model(sequence_length, len(set(notes)))
model_handler.train(model, X, y)

processor.save_notes()

model = MusicGeneratorModel.load_model()
generator = MusicGenerator("midi_files", sequence_length, 50, model)
generator.generate_notes()
generator.create_midi_from_notes("generated_music1_0.midi")


