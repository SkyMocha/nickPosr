import os
import cv2
import csv
import numpy as np
from math import exp, sqrt

import difflib

# REFERENCE #
# https://stackoverflow.com/questions/7063437/midi-timestamp-in-seconds

# System_exclusive doesn't matter?

# Tracks play at same time

directory = "/Users/Nick/Desktop/Audio_Data/testCSV/"
output = "/Users/Nick/Desktop/Audio_Data/Formatted_CSV/"

header = {
    "track": 0, 
    "time": 1,
    "c_event": 2,
    "channel": 3, 
    "note": 4,
    "velocity": 5,
}

# NUMBER GENERATION #

def trackCount (csv):
    tracks = 1
    longest_track = 0
    for line in csv:
        if (int(line[0]) > tracks):
            tracks = (int(line[0]))
        if (int(line[1]) > longest_track):
            longest_track = (int(line[1]))
    return (tracks, longest_track)

def tempo (csv):
    tempo = ""
    for line in csv:
        if line[2].lower().replace(' ', '') == 'tempo':
            tempo = (int(line[3]))
    return tempo

def click (csv):
    click = 0
    for line in csv:
        if line[2].lower().replace(' ', '') == 'time_signature':
            click = (int(line[5]))
    return click

def midiClock (csv):
    return (int(csv[0][5]))

def multiSquare (num, amount):
    if (amount <= 0):
        return num
    else:
        return multiSquare(sqrt(num), amount-1)

# DRAWING #

def drawNote (csv, image):
    for line in csv:
        if line[2].lower().replace(' ', '') == 'note_on_c':
            print (line)
            
    

with open(directory + "Beach_Cave.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    csv = list(csv_reader)

    (tracks, track_len) = trackCount(csv)

    print (f"{tracks} TRACKS")
    print (f"{track_len} IS THE HIGHEST TRACK LENGTH")

    print (f"TEMPO IS {tempo(csv)}")

    bpm = (tempo(csv) / 500000) * 120
    print (f"{bpm} BEATS PER MINUTE")

    mClockPerMin = bpm * click (csv) 
    print (f"{mClockPerMin} MIDI CLOCK TICKS PER MINUTE")

    # formula = track_len / tracks / mClockPerMin
    # print (f"FORMULA RETURNS {formula}")

    # squareAmount = midiClock(csv)/240
    # print (f"WILL BE SUQARING {squareAmount} TIMES")

    # duration = multiSquare(formula, squareAmount)
    # print (f"DURATION OF {duration} MINUTES")

    # durationSeconds = round (duration * 60)
    # print (f"DURATION OF {durationSeconds} SECONDS")

    height = 96
    width = 384

    image = np.zeros((height , int (width) , 3), np.uint8)

    # for row in csv:
    #     print (row)
    # print(f'Processed {line_count} lines.')

cv2.imshow('Image', image)

cv2.waitKey(0)
cv2.destroyAllWindows()

# for filename in os.listdir(directory):

#     if not filename.startswith('.'):
