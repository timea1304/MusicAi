from note import Note
class MidiSammlung:
    def __init__(self):
        self.notes = []

    #note hinzufügen in die Liste
    def add_note(self, note):
        self.notes.append(note)
    
    #noten analysieren für einen Richtwert
    def analyze(self):
        #durchschnitt berechnen
        durations = [note.duration for note in self.notes]
        average_duration = sum(durations)/ len(durations) if durations else 0
        print(f"Average duration: {average_duration}")
    
    #Notensequenz erstellen also noten dauer und pitch zusammenfügen
    def generate_sequence(self, template):
        new_notes=[]
        for i, note in enumerate(self.notes):
            #mit pitch shift die Tonlage verändern/ noten höher oder tiefer machen
            new_pitch = template.get("pitch_shift", 0) + note.pitch
            #dauer anpassen
            new_duration = template.get("duration_multiplier", 1) * note.duration
            #Note mit den analysierten daten zusammen fügen
            new_notes.append(Note(new_pitch, new_duration, note.start_time))
        return new_notes
        
    