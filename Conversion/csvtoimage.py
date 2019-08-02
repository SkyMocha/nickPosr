import os
import csv
import numpy as np
from PIL import Image
from numpy import eye

directory = "/Users/Nick/Desktop/Audio_Data/testCSV/"
output = "/Users/Nick/Desktop/Audio_Data/Formatted_CSV/"

def trackCount (csv):
    return csv[0][4]

def longest_track (csv):
    longest_track = 0
    for line in csv:
        if (int(line[1]) > longest_track):
            longest_track = (int(line[1]))
    return longest_track

def numerizeType (line):
    command = line[2].lower().replace(' ', '')
    if (command == 'header'):
        return 0
    elif (command == 'start_track'):
        return 21
    elif (command == 'end_track'):
        return 42
    elif (command == 'end_of_file'):
        return 63
    elif (command == 'time_signature'):
        return 84
    elif (command == 'key_signature'):
        return 106
    elif (command == 'tempo'):
        return 127
    elif (command == 'smpte_offset'):
        return 148
    elif (command == 'note_on_c'):
        return 169
    elif (command == 'note_off_c'):
        return 190
    elif (command == 'pitch_bend_c'):
        return 211
    elif (command == 'control_c'):
       return 232
    elif (command == 'program_c'):
        return 253
    else:
        return 111

def numerizeLine (line):
    if len(line) > 7:
        line[7] = (int(line[7]))
    if len(line) > 6:
        line[6] = (int(line[6]))
    if len(line) > 5:
        line[5] = (int(line[5]))
    if len(line) > 4:
        line[4] = (int(line[4]))
    if len(line) > 3:
        line[3] = (int(line[3]))
    if len(line) > 2:
        line[2] = numerizeType(line)
    if len(line) > 1:
        line[1] = (int(line[1]))
    if len(line) > 0:
        line[0] = (int(line[0]))

def padLine (line):
    if len(line) == 7:
        line.append (111)
    if len(line) == 6:
        line.extend ((111, 111))
    if len(line) == 5:
        line.extend ((111, 111, 111))
    if len(line) == 4:
        line.extend ((111, 111, 111, 111))
    if len(line) == 3:
        line.extend ((111, 111, 111, 111, 111))
    if len(line) == 2:
        line.extend ((111, 111, 111, 111, 111, 111))
    if len(line) == 1:
        line.extend ((111, 111, 111, 111, 111, 111, 111))

def varyColors(line, track_len):
    line[0] *= int(255/trackCount(csv))

def colorizeTime (line, track_len):
    line[1] = 0

with open(directory + "Chrono_Trigger.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    csv = list(csv_reader)

    track_len = longest_track(csv)

    data = []
    for line in csv:
        if (numerizeType(line) != 111):
            numerizeLine(line)
            padLine(line)
            varyColors(line, track_len)
            colorizeTime (line, track_len)

            # print (line)

            data.append( line )

    npdata = np.array (data, dtype='int')

    print (npdata)

    npdata = np.uint8(npdata)

    print (npdata)

    image = Image.fromarray(npdata)
    image.save(f"{output}Chrono_Trigger.jpeg")

# for filename in os.listdir(directory):

#     if not filename.startswith('.'):