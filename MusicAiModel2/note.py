class Note:
    def __init__(self, pitch, duration, pause, velocity):
        #pitch = tonhöhe bsp.: 60 = C4
        self.pitch = pitch
        #240 ticks bei midi dateien, entspricht es einer halben Note
        self.duration = duration
        #pause in ticks 240 ticks wäre eine pause von einer halben Note
        self.pause = pause
        #lautsärke bzw anschlagsstärke 127 ist die maximale lautstärke
        #beeinflusst auch den klang ob sanft oder stark
        self.velocity = velocity
    
    #repräsentation
    def __repr__(self):
        return f"Note(pitch={self.pitch}, duration={self.duration}, pause={self.pause}, velocity={self.velocity})"

    
        
    