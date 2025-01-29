from midi import MidiSammlung

class MusicGenerator:
    def __init__ (self, template,model ):
        self.template = template
        self.model = model

    def generate_song(self, seed_sequence, length):
        generated = list(seed_sequence)
        for _ in range(length):
           # new_notes = midis.generate_sequence(self.template)
            #new_midi = MidiSammlung()
           # new_midi.notes = new_notes
           # new_notes.append(new_midi)
           input_seq = generated[-len(seed_sequence):]
           input_seq = input_seq.reshape(1,len(seed_sequence),3)
           prediction = self.model.predict(input_seq)[0]
           generated.append(prediction)
        return generated
    
 