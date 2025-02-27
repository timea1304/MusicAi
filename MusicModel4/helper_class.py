import os
from mido import MidiFile,MidiTrack, Message

class HelperClass:
    def __init__(self, base_name, midi_folder):
        self.base_name = base_name
        self.midi_folder = midi_folder


    #neuen Dateinamen für das neue Leid erstellen
    def get_new_filename(self):
        version = 1
        while os.path.exists(os.path.join(self.folder, f"{self.base_name}_{version}.midi")):
            version += 1
        return os.path.join(self.folder, f"{self.base_name}_{version}.midi")
    
   #Generierte Lieder bewerten 
    """ def music_rating(self):
        try:
            rating = int(input("Bewerten: (1 = schlecht|5 = sehr gut):"))
            if 1 <= rating <= 5:
                with open(self.feedback_file, "a") as file:
                    writer = csv.writer(file)
                    writer.writerow([self.filename, rating])
                print("Bewertung gespeichert.")
            else:
                print("Ungültige Eingabe. Bitte eine Zahl eingeben.")
        except ValueError:
            print("Ungültige Eingabe. Bitte eine Zahl eingeben.")

    #mit den Bewertungen trainieren
    def train_with_rating(self, actual_notes):
        positive_notes = []
        try:
            with open(self.feedback_file, "r") as file:
                reader = csv.reader(file)
                feedback = list(reader)
            for row in feedback:
                if len(row) != 2:
                    print(f"Ungültige Zeile Übersprungen: {row}")
                    continue
                filename, rating = row
                try: 
                    if int(rating) >= 4:
                        with open(filename.replace('.midi', '.pkl'),'rb') as notes_file:
                            positive_notes.extend(pickle.load(notes_file))
                except(ValueError, FileNotFoundError) as e:
                    print(f"Fehler beim Verarbeiten der Datei {filename}")
        except FileNotFoundError:
            print("Feedback-Datei nicht gefunden.")

        all_notes = actual_notes + positive_notes

        return all_notes"""
    
    """def save_midi_file(self, notes, filename):
        midi = MidiFile()
        track = MidiTrack()
        midi.tracks.append(track)

        time = 0
        for note in notes:
            pitch = int(note[0] * 127)
            velocity = int(note[1] * 127)
            pause = int(note[2] * 480)  # Pause in Ticks
            track.append(Message('note_on', note=pitch, velocity=velocity, time=time))
            track.append(Message('note_off', note=pitch, velocity=0, time=pause))
            time = 0

        midi.save(filename)"""