import tensorflow as tf
from music21 import converter, note, chord
import numpy as np
import glob
import pickle

def load_midi_files():
    guitar_notes = []
    drum_notes = []