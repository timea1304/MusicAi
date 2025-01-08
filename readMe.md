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

Noch Löschen des ersten Models soll erstellt werden:
- Feedbacksystem
- Midiutil ggf einbauen


Hilfs Videos:
 https://www.youtube.com/watch?v=aOsET8KapQQ&t=517s
https://www.youtube.com/watch?v=2wM_zxd-NA4&t=343s
https://www.youtube.com/watch?v=MYVWPmzsRz8
https://www.youtube.com/watch?v=pg9apmwf7og
https://www.youtube.com/watch?v=Fa_V9fP2tpU
https://www.youtube.com/watch?v=cAkMcPfY_Ns
https://www.youtube.com/watch?v=29ZQ3TDGgRQ&t=458s

HilfsSeiten:
https://pypi.org/project/MIDIUtil/
https://docs.python.org/3/library/csv.html
https://docs.python.org/3/library/pickle.html
https://numpy.org/
https://www.music21.org/music21docs/
https://www.tensorflow.org/api_docs/python/tf/keras/layers/LSTM