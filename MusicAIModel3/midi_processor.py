import pandas as pd
import numpy as np
import pickle
import ast

class MidiProcessor:
    def __init__(self, csv_file, sequence_length):
        self.csv_file = csv_file
        self.sequence_length = sequence_length
        self.notes = []

    def load_data(self):
        df = pd.read_csv(self.csv_file)
        notes =[]
        for _, row in df.iterrows():
            try:
                pitch = ast.literal_eval(row["Noten (MIDI)"])
            except Exception:
                pitch = row["Noten (MIDI)"]
            try:
                duration = ast.literal_eval(row["Dauer (Sekunden)"])
                duration = duration[0] if isinstance(duration, list) and duration else float(duration)
            except Exception:
                duration = float(row["Dauer (Sekunden)"])
            try:
                pause = ast.literal_eval(row["Pause (Sekunden)"])
                pause = pause[0] if isinstance(pause, list) and pause else float(pause)
            except Exception:
                pause = floar(row["Pause (Sekunden)"])

            note_dict = {
                "pitch": pitch,
                "duration": duration,
                "pause": pause
                }
            notes.append(note_dict)
        self.notes = notes
        return notes
        #noten_df = df['Noten (MIDI)'].values
        #duration_df = df['Dauer (Sekunden)'].values
        #pause_df = df['Pause (Sekunden)'].values
       # return noten_df, duration_df, pause_df

    
    def process_midi(self, notes):
        sequences =[]
        noten_labels = []
        duration_labels = []
        pause_labels = []

        for i in range(len(notes)- self.sequence_length):
            sequence = notes[i:i + self.sequence_length]
           # duration_seq = duration_df[i:i + self.sequence_length]
            sequences.append([[note["pitch"], note["duration"], note["pause"]] for note in sequence])
            next_note = notes[i + self.sequence_length]
            noten_labels.append(next_note["pitch"])
            duration_labels.append(next_note["duration"])
            pause_labels.append(next_note["pause"])
            #sequences.append([noten_seq, duration_seq, pause_seq])
            #noten_labels.append(noten_df[i + self.sequence_length])
            #duration_labels.append(duration_df[i+self.sequence_length])
            #pause_labels.append(pause_df[i + self.sequence_length])

        X = np.array(sequences)
        y = {
            "noten_output": np.array(noten_labels),
            "duration_output": np.array(duration_labels),
            "pause_output": np.array(pause_labels)
        }

        return X, y
    
    
    def save_notes(self, output_file="notes.pkl"):
        """Speichern der Noten in einer Pickle-Datei."""
        with open(output_file, "wb") as file:
            pickle.dump(self.notes, file)

