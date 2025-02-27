import os
from mido import MidiFile
import numpy as np
import glob
from music21 import converter
import pretty_midi

class MidiProcessor:
    def __init__(self, csv_file, sequence_length, midi_files_path):
        self.csv = csv_file
        self.sequence_length = sequence_length
        self.midi_files_path = midi_files_path
        self.notes=[]
                

    def load_midi_files(self):
       
        for file in os.listdir(self.midi_files_path):
            if not (file.endswith('.mid') or file.endswith('.midi')):
                continue

            file_path = os.path.join(self.midi_files_path, file)

            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Datei {file_path} nicht gefunden. Überprüfe den Pfad")

            print(f"Parsing {file_path}")
            try:
                midi = converter.parse(file)
                
            except:

          
