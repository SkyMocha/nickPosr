import os
import csv
import numpy as np
from PIL import Image

directory = "/Users/Nick/Desktop/Audio_Data/Formatted_CSV_Output/"
output = "/Users/Nick/Desktop/Audio_Data/CSV_Output/"

def trackCount (npdata):
    return (int(npdata[0][4]))

def longest_track (npdata):
    longest_track = 0
    for line in npdata:
        if (int(line[1]) > longest_track):
            longest_track = (int(line[1]))
    return longest_track

def stringizeType (line):
    num = (int(line[2]))
    if (num == 0):
        return 'header'
    elif (num == 21):
        return 'start_track'
    elif (num == 42):
        return 'end_track'
    elif (num == 63):
        return 'end_of_file'
    elif (num == 84):
        return 'time_signature'
    elif (num == 106):
        return 'key_signature'
    elif (num == 127):
        return 'tempo'
    elif (num == 148):
        return 'smpte_offset'
    elif (num == 169):
        return 'note_on_c'
    elif (num == 190):
        return 'note_off_c'
    elif (num == 211):
        return 'pitch_bend_c'
    elif (num == 232):
       return 'control_c'
    elif (num == 253):
        return 'program_c'
    else:
        return 111

def stringizeLine (line):
    if len(line) > 2:
        line[2] = stringizeType(line)

def unpadLine (line):
    while '111' in line: 
        line.remove('111')

def unvaryColors(line):
    line[0] =  str(int(int(line[0]) / int(255/trackCount(npdata))))

image = Image.open (f"{directory}Chrono_Trigger.jpeg")
npdata = np.asarray(image)
npdata.setflags(write=1)
npdata = npdata.astype('str')

with open(f"{output}Chrono_Trigger.csv", "w+") as csv_file:

    csv_writer = csv.writer(csv_file, delimiter=',')

    track_len = longest_track(npdata)

    for line in npdata:
        # if (stringizeType(line) != -1):
        print (line)
        line.tolist()
        unpadLine(line)
        stringizeType (line)
        stringizeLine (line)
        unvaryColors (line)

        # print (line)

        csv_writer.writerow(line)


# for filename in os.listdir(directory):

#     if not filename.startswith('.'):