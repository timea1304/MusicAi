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

Nach Löschen des ersten Models soll erstellt werden:
- Feedbacksystem
- Midiutil ggf einbauen


Hilfs Videos:
 https://www.youtube.com/watch?v=aOsET8KapQQ&t=517s <br>
https://www.youtube.com/watch?v=2wM_zxd-NA4&t=343s <br>
https://www.youtube.com/watch?v=MYVWPmzsRz8 <br>
https://www.youtube.com/watch?v=pg9apmwf7og <br>
https://www.youtube.com/watch?v=Fa_V9fP2tpU <br>
https://www.youtube.com/watch?v=cAkMcPfY_Ns <br>
https://www.youtube.com/watch?v=29ZQ3TDGgRQ&t=458s

HilfsSeiten:
https://pypi.org/project/MIDIUtil/ <br>
https://docs.python.org/3/library/csv.html <br>
https://docs.python.org/3/library/pickle.html <br>
https://numpy.org/ <br>
https://www.music21.org/music21docs/ <br>
https://www.tensorflow.org/api_docs/python/tf/keras/layers/LSTM
https://www.tensorflow.org/tutorials/audio/music_generation <br>
https://de.eitca.org/artificial-intelligence/eitc-ai-tff-tensorflow-fundamentals/natural-language-processing-with-tensorflow/long-short-term-memory-for-nlp/examination-review-long-short-term-memory-for-nlp/how-can-we-implement-lstm-in-tensorflow-to-analyze-a-sentence-both-forwards-and-backwards/<br>
https://developers.google.com/machine-learning/crash-course?hl=de <br>
https://keras.io/guides/sequential_model/ <br>
https://developers.google.com/machine-learning/intro-to-ml/supervised?hl=de <br>
https://www.rileynwong.com/blog/2019/2/25/generating-music-with-an-lstm-neural-network <br>
https://towardsdatascience.com/how-to-generate-music-using-a-lstm-neural-network-in-keras-68786834d4c5 <br>
https://github.com/cobanov/python-yaml-guide <br>
https://www.ionos.de/digitalguide/websites/web-entwicklung/python-string-to-list/ <br>
https://docs.python.org/3/library/ast.html <br>



GoogleSuche:
- Midi dateien
- Velocity
- duration bei Midi dateien
- Pitch bei Midi dateien

<p> Nach Einbau des Feedbacksystems kam es zur keiner Besserung der Generierung. Also hab ich eine Weitere Neuronale Schicht hinzugefügt, damit das Model die komplexeren Muster von Hardstyle/Hardcore lernen kann.
Nach generierung der 7. Version kam es wieder zu einem Fail.<br> Vermütung war das es ggf auch am Instrument und an der Geschwindigkeit der Generierten Midi file handelt.
<br> Nach verwendung eines Online Tools https://signal.vercel.app/edit und einwenig bearbeitung viel auf das es wirklich daran lag.

- Tempo einbauen
- Polysynth o.ä als instrument einbauen.