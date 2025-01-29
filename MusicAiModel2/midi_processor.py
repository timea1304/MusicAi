from mido import MidiFile
import os
import numpy as np



class MidiProcessor:
    def __init__(self, sequence_length, midi_files):
        self.sequence_length = sequence_length
        self.midi_files = midi_files
        

    """
    midi dateien laden
    :return: Liste von Noten(pitch, velocity, time)
    """
    def load_midi_files(self, midi_files):
        notes=[]
        for file in midi_files:
            if not os.path.exists(file):
                 raise FileNotFoundError(f"Datei {file} nicht gefunden. Überprüfe den Pfad")
            midi = MidiFile(file)
            time = 0
        #midi_file = MidiFile(self.file_path)
        #for midi in midi.midi_group:
        # for i, midi in enumerate(midi_file.midis):
            #print(f"Midi {i}: {midi.name}")
            #midi_song = MidiSammlung()
            #time = 0
            for track in midi.tracks:
                for msg in track:
                    time+= msg.time
                    if msg.type == 'note_on' and msg.velocity > 0:
                        #note = Note(msg.note,0, time, msg.velocity)
                        notes.append((msg.note, msg.velocity, time))
                        # midi_song.add_note(note)
                    elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                        #for note in midi_song.notes:
                        #   if note.pitch == msg.note and note.duration == 0:
                        #      note.duration = time - note.start_time
                        #     break
                        notes.append((msg.note, 0, time))   
                #self.midis.append(midi_song)
        return notes
        
    """
    Daten für das Trainieren vorbereiten
    :return: Array mit Trainingsdaten(pitches, velocities, pauses).
    """
    def prepare_data(self,notes):
        sequences = []
       # for midi_file in midi_files:
           # notes = self.filter_data(midi_file)
        for i in range(len(notes) - self.sequence_length):
                sequences.append(notes[i:i + self.sequence_length])

        sequences = np.array(sequences)
        pitches = sequences[:,:,0]/127.0
        velocities = sequences[:,:,1]/127.0
        pauses = np.diff(sequences[:,:,2], axis = 1, prepend = 0) / max(sequences[:,:,2].max(),1)
        return np.stack([pitches,velocities,pauses], axis=-1)

    #!ggf ausklammern
   # def analyze(self):
    #    for i, midi in enumerate(self.tracks):
     #       print(f"Analyzing Song {i}")
      #      midi.analyze()
   