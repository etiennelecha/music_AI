from music21 import converter, note, chord
import numpy as np
import random
import pandas as pd

def extractNote(element):
    return int(element.pitch.ps)


def extractDuration(element):
    return element.duration.quarterLength


def get_notes(notes_to_parse):
    """
    Get all the notes and chords from the midi files in the ./midi_songs directory
    """
    durations = []
    notes = []
    start = []

    for element in notes_to_parse:
        if isinstance(element, note.Note):
            if element.isRest:
                continue

            start.append(element.offset)
            notes.append(extractNote(element))
            durations.append(extractDuration(element))

        elif isinstance(element, chord.Chord):
            if element.isRest:
                continue
            for chord_note in element.notes:
                start.append(element.offset)
                durations.append(extractDuration(element))
                notes.append(extractNote(chord_note))

    return {"start": start, "pitch": notes, "dur": durations}


def midi_to_matrix(midi_path, resolution=1/16, lowerBoundNote=21, upperBoundNote=127):

    '''
    Takes in a midi file and returns a numpy array:
        rows = notes
        columns = time (resolution parameter)
    '''

    mid = converter.parse(midi_path)

    data = {}

    notes_to_parse = mid.flat.notes
    data = get_notes(notes_to_parse)

    pitches = data["pitch"]
    durs = data["dur"]
    starts = data["start"]

    matrix = np.zeros((upperBoundNote - lowerBoundNote,
                       int((max(starts) + durs[-1]) / resolution)))

    for dur, start, pitch in zip(durs, starts, pitches):
        dur = int(dur / resolution)
        start = int(start / resolution)

        for j in range(start, start + dur):
            # added line below to create clear division inbetween notes
            matrix[pitch - lowerBoundNote, start - 1] = 0
            matrix[pitch - lowerBoundNote, j] = 1

    return matrix


def random_xy(matrix, len_x, len_y):

    '''
    Create random couple X, y of given length out of input matrix
    '''

    width, length = matrix.shape

    start = random.randint(0,width-(len_x+len_y))

    left_x = start
    right_x = start + len_x

    left_y = right_x
    right_y = right_x + len_y

    return matrix[:, left_x:right_x], matrix[:, left_y:right_y]


def get_X_y(midi_path, resolution, len_x, len_y, n_sequences):
    '''
    Create dataframe out of midi file with random X,y
    '''
    X = []
    y = []
    matrix = midi_to_matrix(midi_path, resolution)
    for n in range(n_sequences):
        split_ = random_xy(matrix, len_x, len_y)
        X += [split_[0].T]
        y += [split_[1].T]
    return np.array(X), np.array(y)
