# This package is for experimenting with a Python package called "chorder",
# which detects chords in mid files.
from chorder import Dechorder, Chord
from miditoolkit import MidiFile


# Root and bass pitch class (pc)
pc_translations = {0: "C", 1: "C♯/D♭", 2: "D", 3: "D♯/E♭", 4: "E", 5: "F", 6: "F♯/G♭", 7: "G", 8: "G♯/A♭", 9: "A", 10: "A♯/B♭", 11: "B", None: "None"}
# Quality = type of chord
quality_translation = {'m': "minor", 'M7': "major seventh", '7': "dominant seventh", 'm7':"minor seventh", 'o': "diminished", None: None}


def extract_chords():
  path_midi = "./data/audio/ron-minis-separated/ron-minis-cut-0251600-30s/ron-minis-cut-0251600-30s.mid"
  midi_obj = MidiFile(path_midi)
  return Dechorder.dechord(midi_obj, scale=None)


def translate_output():
  ts = []
  # (root_pc, quality, bass_pc)
  out = [(0, 'm', 0), (0, 'm', 0), (8, 'M7', 0), (8, 'M7', 0), (8, '7', 8), (8, '7', 8), (5, 'm7', 5), (5, 'm7', 5), (7, 'm7', 7), (7, 'm7', 7), (0, 'm', 0), (0, 'm', 0), (10, 'M7', 10), (10, 'M7', 10), (7, 'm7', 10), (7, 'm7', 10), (0, 'm7', 0), (0, 'm7', 0), (0, 'm', 0), (0, 'm', 0), (8, 'M7', 8), (8, 'M7', 8), (8, '7', 8), (8, '7', 8), (5, 'm7', 5), (7, 'm7', 7), (7, 'm7', 7), (0, 'm', 0), (0, 'o', 0), (0, 'o', 0), (10, 'M7', 10), (10, 'M7', 10), (3, 'M7', 7), (7, 'm', 7), (0, 'm7', 7), (0, 'm7', 7), (9, 'm7', 0), (9, 'm7', 0), (0, 'M7', 0), (0, 'M7', 0), (0, 'M7', 0), (0, 'M7', 0), (0, 'M7', 0), (0, 'M7', 0), (0, 'M7', 0), (0, 'M7', 0), (0, 'M7', 0), (6, 'o', 0), (6, 'o', 0), (6, 'o', 0), (0, 'M7', 0), (0, 'M7', 0), (6, 'o', 0), (6, 'o', 0), (0, 'm7', 0), (0, 'm7', 0), (0, 'm7', 0), (0, 'm7', 0), (0, 'm7', 0), (0, 'm7', 0), (None, None, None)]
  for chord in out:
    ts.append(f"{pc_translations[chord[0]]} {quality_translation[chord[1]]}")
  print(ts)


translate_output()
