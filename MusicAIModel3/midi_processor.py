import pandas as pd
import numpy as np
import pickle
import ast

class MidiProcessor:
    def __init__(self, csv_file, sequence_length):
        self.csv_file = csv_file
        self.sequence_length = sequence_length
        self.notes = []
        self.n_vocab = 0

    def load_data(self):
        df = pd.read_csv(self.csv_file)
        notes =[] #liste
        for _, row in df.iterrows():
            try:
                pitch = ast.literal_eval(row["Noten (MIDI)"])
                if not isinstance(pitch, list):
                    pitch = [int(pitch)]  # Konvertiere in int
                else:
                    pitch = [int(p) for p in pitch]  # Falls Liste, konvertiere alle Elemente in int
            except Exception:
                pitch = [row["Noten (MIDI)"]]
            try:
                duration = ast.literal_eval(row["Dauer (Sekunden)"])
                duration = duration[0] if isinstance(duration, list) and duration else float(duration)
            except Exception:
                duration = float(row["Dauer (Sekunden)"])
            try:
                pause = ast.literal_eval(row["Pause (Sekunden)"])
                pause = pause[0] if isinstance(pause, list) and pause else float(pause)
            except Exception:
                pause = float(row["Pause (Sekunden)"])

            note_dict = {
                "pitch": pitch,
                "duration": duration,
                "pause": pause
                }
            notes.append(note_dict)
        self.notes = notes
        self.n_vocab = len(set(p["pitch"][0] if isinstance(p["pitch"], list) else p["pitch"] for p in notes))

        
        return notes
        #noten_df = df['Noten (MIDI)'].values
        #duration_df = df['Dauer (Sekunden)'].values
        #pause_df = df['Pause (Sekunden)'].values
       # return noten_df, duration_df, pause_df

    
    def process_midi(self):
        sequences =[]
        labels = {"pitch_output": [], "duration_output": [], "pause_output": []}
        
        if not self.notes:
            raise ValueError("Fehler: `self.notes` ist leer. Überprüfe `load_data()`.")
        
        if len(self.notes) < self.sequence_length:
            raise ValueError(f"Fehler: `self.sequence_length` ({self.sequence_length}) ist größer als die Anzahl der geladenen Noten ({len(self.notes)}).")
        
        print(f"Anzahl geladener Noten: {len(self.notes)}")
        print(f"Erwartete Sequenzlänge: {self.sequence_length}")
        print(f"Berechneter Bereich: {len(self.notes) - self.sequence_length}")

        pitch_values = [note["pitch"][0] if isinstance(note["pitch"], list) else note["pitch"] for note in self.notes]
        unique_pitches = sorted(set(pitch_values))
        pitch_to_idx = {pitch: idx for idx, pitch in enumerate(unique_pitches)}

        for i in range(len(self.notes)- self.sequence_length):
            sequence = self.notes[i:i + self.sequence_length]
            formatted_seq = [[pitch_to_idx[note["pitch"][0]] if isinstance(note["pitch"], list) 
                              else pitch_to_idx[note["pitch"]], note["duration"], note["pause"]] for note in sequence]
            sequences.append(formatted_seq)

            next_note = self.notes[i + self.sequence_length]
           # unique_pitches = sorted(set(pitch_values))
            #pitch_to_idx = {pitch: idx for idx, pitch in enumerate(unique_pitches)}
            labels["pitch_output"].append(pitch_to_idx[next_note["pitch"][0]]
                                           if isinstance(next_note["pitch"], list) else pitch_to_idx[next_note["pitch"]])
            labels["duration_output"].append(next_note["duration"])
            labels["pause_output"].append(next_note["pause"])
            #formatted_seq = []
        """sequence = self.notes[i:i + self.sequence_length]
                for note in  sequence:
                pitch = note["pitch"][0] if isinstance(note["pitch"], list) else note["pitch"]
                formatted_seq.append([pitch,note["duration"], note["pause"]])

             sequences.append(formatted_seq)"""

            # sequences, labels = [], {"pitch_output": [], "duration_output": [], "pause_output": []}

           
                
                #if isinstance (pitch, list):
                #    pitch = pitch[0]
                 #   print(pitch, note["duration"], note["pause"])
                
            #duration_seq = duration_df[i:i + self.sequence_length]
        """if sequences and len(sequences[-1]) != self.sequence_length:
                raise ValueError(f"Inkonsistente Sequenzlängen! Erwartet: {self.sequence_length}, Erhalten: {len(sequences[-1])}")

           
            next_note = notes[i + self.sequence_length]
            noten_labels.append(next_note["pitch"][0] if isinstance(next_note["pitch"], list) else next_note["pitch"])
            duration_labels.append(next_note["duration"])
            pause_labels.append(next_note["pause"])
            #sequences.append([noten_seq, duration_seq, pause_seq])
            #noten_labels.append(noten_df[i + self.sequence_length])
            #duration_labels.append(duration_df[i+self.sequence_length])
            #pause_labels.append(pause_df[i + self.sequence_length])"""
        print("Max Pitch Output:", max(labels["pitch_output"]))
        print("Min Pitch Output:", min(labels["pitch_output"]))

        X = np.array(sequences, dtype= np.float32).reshape(len(sequences), self.sequence_length, 3)
        y = {
            "pitch_output": np.array(labels["pitch_output"], dtype=np.int32),
            "duration_output": np.array(labels["duration_output"], dtype=np.float32),
            "pause_output": np.array(labels["pause_output"], dtype=np.float32)
         }
        #Debugging:
        print(f"X Shape: {X.shape}")
        print(f"Pitch_output Shape: {y['pitch_output'].shape}")
        print(f"Duration_output Shape: {y['duration_output'].shape}")
        print(f"Pause_output Shape: {y['pause_output'].shape}")
        print("Unique Pitch:", unique_pitches)
        print("Pitch to index:", pitch_to_idx)
        print("Pitch output:", labels["pitch_output"])
        return X, y
    
    
    def save_notes(self, filename="notes.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self.notes, f)

