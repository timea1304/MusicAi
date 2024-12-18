<p>Die classiefier.py und die generate_music funktioniert soweit,
ich bin gerade dabei es noch Objektorientiert umschreiben:
main.py
model.py
music_generator.py
midi_processor.py

diese Funktionieren aber noch nicht richtig zusammen.</p>

<p> "Sequence length bestimmt wie viele Informationen das Modell aus der Vergangenheit behalten kann.
Eine längere Sequenzlänge bedeutet, dass das Modell längerfristige Abhängigkeiten erfassen und komplexere Muster erlernen kann.
Jedoch erhöht es auch den Rechenaufwand. Eine kürzere Sequenzlänge bedeutet, dass das Model schneller Trainiert werden kann,
jedoch reduziert es auch die Menge an Kontext und die Ausdruckskraft des Modells."
- https://www.linkedin.com/advice/3/what-optimal-sequence-length-rnn-skills-machine-learning-nu4gc 
Es handelt sich um die länge des Kontexts die in Betracht gezogen werden, wärend eines Trainings</p>

Nach einem Durchgang mit vielen Durcheinander Gemischten Midi files ist mir aufgefallen das wohl akkorde mehr aufgenommen wurden und mehr eine Art durchgehender Rhytmus vorhanden ist, jedoch fehlt mir eine einheitliche Musikrichtung, dementsprechend, ist das nächste Ziel doch eher einen Interpreten, oder eine Musik richtung zu generieren.
Außerdem, muss ich die Lieder rausfiltern, die nur den Bass eines Liedes oder rein die Rythmic und nicht die Melodie darstellen.