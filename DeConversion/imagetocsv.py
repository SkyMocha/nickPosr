import os
import csv
import numpy as np
from PIL import Image
from statistics import mean

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
        return 'Header'
    elif (num == 21):
        return 'Start_track'
    elif (num == 42):
        return 'End_track'
    elif (num == 63):
        return 'End_of_file'
    elif (num == 74):
        return 'Marker_t'
    elif (num == 84):
        return 'Time_signature'
    elif (num == 106):
        return 'Key_signature'
    elif (num == 127):
        return 'Tempo'
    elif (num == 148):
        return 'SMPTE_offset'
    elif (num == 169):
        return 'Note_on_c'
    elif (num == 190):
        return 'Note_off_c'
    elif (num == 211):
        return 'Pitch_bend_c'
    elif (num == 232):
       return 'Control_c'
    elif (num == 253):
        return 'Program_c'
    else:
        return 111

def stringizeLine (line):
    if len(line) > 2:
        line[2] = stringizeType(line)

        if (line[2] == 'Marker_t'):
            if int(line[3]) == 0:
                line[3] = 'loopStart'
            elif int(line[3]) == 255:
                line[3] = 'loopEnd'
        
        elif line[2] == 'Key_signature':
            if int(line[4]) == 0:
                line[4] = 'major'
            elif int(line[4]) == 255:
                line[4] = 'minor'

def unpadLine (line):
    i = len(line) - 1
    for elem in line:
        if (line[i] == '111'):
            line.pop(i)
            i-=1

def fix (line):
    if (line[2] == 'End_of_file' or line[2] == 'Start_track'):
        unpadLine(line)        

def unvaryColors(line):
    line[0] =  str(int(int(line[0]) / int(255/trackCount(npdata))))

def popple (line):
    line.pop (5)
    line.pop (4)
    line.pop (3)
    line.pop (2)

def normalizeLine (line):
    num = (int(line[6]))
    num2 = (int(line[2]))
    if (num == 169 or num == 190 or num == 211 or num == 232 or num == 253 or num == 42 or num == 74):
        time = int (line[1]) * int (line[2]) * int (line[3]) * int (line[4]) * int (line[5])
        line[1] = str(time)
        popple(line)

    elif (num2 == 0):
        time = int (line[5]) * int (line[6]) * int(line[7])
        line[5] = time
        line.pop (7)
        line.pop (6)

    elif (num2 == 127):
        time = int (line[3]) * int (line[4]) * int (line[5])
        line[3] = str(time)
        line.pop (6)
        line.pop (5)
        line.pop (4)


# def normalizeTime (normalize, data, npdata, i):
#     if normalize:
#         data[i-1][1] = str(int(mean ((int(data[i-2][1]), int(data[i][1])))))
#         return False
#     elif (int(npdata[i][1]) < int(npdata[i -1][1])):
#         return True

def normalizeTime (data, i):
    if (int(data[i][1]) < int(data[i - 1][1])):
        data[i][1] = data[i - 1][1]

for filename in os.listdir(directory):

    if not filename.startswith('.'):

        print (f"STARTING {filename}")

        image = Image.open (f"{directory + filename}")
        npdata = np.asarray(image)
        npdata.setflags(write=1)
        npdata = npdata.astype('int')
        npdata = npdata.astype('str')

        with open(f"{output + filename.replace('.png', '')}.csv", "w+") as csv_file:

            csv_writer = csv.writer(csv_file, delimiter=',')

            track_len = longest_track(npdata)

            data = []

            # normalize = False

            i = 0

            for line in npdata:
                line = line.tolist()

                normalizeLine(line)

                stringizeType (line)
                stringizeLine (line)
                unvaryColors (line)

                unpadLine(line)
                fix (line)

                data.append (line)

                if (line[1] != '0'):
                    normalizeTime(data, i)

                i+=1

            # data = sorted(data, key=lambda x: int(x[1]))

            # print (data)

            for line in data:
                line = [ f' {x}' for x in line ]

                csv_writer.writerow(line)
            
            print (f"{filename} DONE")

print ("PROCESS COMPLETE")