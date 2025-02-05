from MusicAIModel3.midi_aufbereiter import MidiAufbereiter

midi_files_path = "MusicAiModel\Midi_files\Hardstyle"
output_csv = "MusicAiModel2\hardstyle_data.csv"

aufbereiter = MidiAufbereiter(midi_files_path,output_csv)
aufbereiter.extract_midi_data()