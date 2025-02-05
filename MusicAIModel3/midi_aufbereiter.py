import pretty_midi
import csv
import os

class MidiAufbereiter:
    def __init__(self, midi_files_path, output_csv):
        self.midi_files_path = midi_files_path
        self.output_csv = output_csv

    def extract_midi_data(self):
        all_events = []
        for midi_file in os.listdir(self.midi_files_path):
            if not (midi_file.endswith('.mid') or midi_file.endswith('.midi')):
                continue

            midi_path = os.path.join(self.midi_files_path, midi_file)
            midi_data = pretty_midi.PrettyMIDI(midi_path)

            tempo_changes=midi_data.get_tempo_changes()
            tempo = round(tempo_changes[1][0], 2)if tempo_changes[1].size > 0 else 120

            for instrument in midi_data.instruments:
                prev_end_time = 0
                accords = {}

                for note in instrument.notes:
                    note_start = round(note.start, 3)
                    note_end = round(note.end, 3)
                    note_pitch = note.pitch
                    note_duration = note_end - note_start

                    if note_start not in accords:
                       accords[note_start] = []

                    accords[note_start].append((note_pitch, note_duration, note_end))

                for start_time in sorted(accords.keys()):
                    notes = accords[start_time]
                    pauses_duration = max(0, start_time - prev_end_time)

                    pitches = [n[0] for n in notes]
                    durations = [round(n[1], 3) for n in notes]
                    max_end_time = max(n[2] for n in notes)

                    all_events.append([midi_file,str(pitches),str(durations), round(pauses_duration, 3), tempo])

                    prev_end_time = max_end_time

        with open(self.output_csv, "w", newline='') as file:
                writer = csv.writer(file)
                writer. writerow(["Dateiname","Noten (MIDI)", "Dauer (Sekunden)", "Pause (Sekunden)", "Tempo(BPM)"])
                writer.writerows(all_events)

        print(f"CSV gespeichert unter: {self.output_csv}")
                    