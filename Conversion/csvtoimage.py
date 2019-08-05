import os
import csv as csvMod
import numpy as np
from PIL import Image
import random

from time import sleep

directory = "/Users/Nick/Desktop/Audio_Data/CSV/"
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
    elif (command == 'marker_t'):
        return 74
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
        if line[4] == ' "major"':
            line[4] = 0
        elif line[4] == ' "minor"':
            line[4] = 255
        else:
            try:
                line[4] = (int(line[4]))
            except:
                line[4] = 111

    if len(line) > 3:
        if line[3] == ' "loopStart"':
            line[3] = 0
        elif line[3] == ' "loopEnd"':
            line[3] = 255
        else:
            try:
                line[3] = (int(line[3]))
            except:
                line[3] = 111

    if len(line) > 2:
        line[2] = numerizeType(line)
    
    if len(line) > 1:
        if (line[2] == 127 or line[2] == 106):
            line[1] = 0
        else:
            try:
                line[1] = (int(line[1]))
            except:
                line[1] = 111
        
    if len(line) > 0:
        line[0] = (int(line[0]))

def padLine (line):
    if len(line) == 10:
        line.append (111)
    if len(line) == 9:
        line.extend ((111, 111))
    if len(line) == 8:
        line.extend ((111, 111, 111))
    if len(line) == 7:
        line.extend ((111, 111, 111, 111))
    if len(line) == 6:
        line.extend ((111, 111, 111, 111, 111))
    if len(line) == 5:
        line.extend ((111, 111, 111, 111, 111, 111))
    if len(line) == 4:
        line.extend ((111, 111, 111, 111, 111, 111, 111))
    if len(line) == 3:
        line.extend ((111, 111, 111, 111, 111, 111, 111, 111))
    if len(line) == 2:
        line.extend ((111, 111, 111, 111, 111, 111, 111, 111, 111))
    if len(line) == 1:
        line.extend ((111, 111, 111, 111, 111, 111, 111, 111, 111, 111))

def varyColors(line, track_len):
    line[0] *= int(255/trackCount(csv))

def splitTempo (line):
    length = line[3]
    factors = factor (length)

    if (len (factors) >= 2):
        b = 1
        a = 1

        r = chooseLargest(factors)[0]
        g = chooseLargest (factors)[1]

        if (g > 255):

            length = chooseLargest(factors)[1]
            factors = chooseLargest (factor(length))

            g = chooseLargest (factors)[0]
            b = chooseLargest (factors)[1]

            if (b > 255):

                length = chooseLargest(factors)[1]
                factors = chooseLargest (factor(length))

                b = chooseLargest (factors)[0]
                a = chooseLargest (factors)[1]

        line.insert (4, g)
        line.insert (5, b)
        line.insert (6, a)
        line[3] = r

def splitHeader (line):
    length = line[5]
    factors = factor (length)

    if (len (factors) >= 2):
        b = 1

        r = chooseLargest(factors)[0]
        g = chooseLargest (factors)[1]

        if (g > 255):

            length = chooseLargest(factors)[1]
            factors = chooseLargest (factor(length))

            g = chooseLargest (factors)[0]
            b = chooseLargest (factors)[1]

        line.insert (6, g)
        line.insert (7, b)
        line[5] = r

def factor(x):
    factors = []
    for i in range(1, x + 1):
       if x % i == 0:
           factors.append (i)
    if len(factors) == 2:
        
        return factor (x - 1)
    else:
        return factors

def chooseLargest (nums):
    i = 0
    for num in nums:
        if (num > 255 and nums[len(nums)-i]):
            return [nums[i-1], nums[len(nums)-i]]
        else:
            i+=1
    return [nums[0], nums[len(nums)-1]]

def colorizeTime (line):
    length = line[1]
    factors = factor (length)

    if (len (factors) >= 2):
        b = 1
        a = 1
        q = 1

        r = chooseLargest(factors)[0]
        g = chooseLargest (factors)[1]

        if (g > 255):

            length = chooseLargest(factors)[1]
            factors = chooseLargest (factor(length))

            g = chooseLargest (factors)[0]
            b = chooseLargest (factors)[1]

            if (b > 255):

                length = chooseLargest(factors)[1]
                factors = chooseLargest (factor(length))

                b = chooseLargest (factors)[0]
                a = chooseLargest (factors)[1]

                if (a > 255):
                    length = chooseLargest(factors)[1]
                    factors = chooseLargest (factor(length))

                    a = chooseLargest (factors)[0]
                    q = chooseLargest (factors)[1]

        # print (r * g * b * a * q)

        line.insert (2, g)
        line.insert (3, b)
        line.insert (4, a)
        line.insert (5, q)
        line[1] = r

def addWhiteSpace (data):
    blankLine = [111, 111, 111, 111, 111, 111, 111, 111, 111, 111, 111]
    data.append(blankLine)
    data.append(blankLine)
    return True

i = 0

for filename in os.listdir(directory):

    if not filename.startswith('.'):

        try:

            if i < 203:
                i+=1
                continue

            print (f"STARTING {filename}")

            notes = False

            with open(directory + filename, encoding='utf-8', errors='ignore') as csv_file:
                csv_reader = csvMod.reader(csv_file, delimiter=',')

                csv = list(csv_reader)

                track_len = longest_track(csv)

                data = []
                for line in csv:
                    if (numerizeType(line) != 111):
                        numerizeLine(line)

                        if (line[2] == 127):
                            splitTempo(line)
                        if (line[2] == 0):
                            splitHeader(line)

                        varyColors(line, track_len)
                        colorizeTime (line)

                        padLine(line)

                        if not notes and (line[2] == 169 or line[2] == 190 or line[2] == 211 or line[2] == 232 or line[2] == 253):
                            notes = addWhiteSpace(data)

                        # print (line)

                        for elem in line:
                            if elem > 255:
                                # print (line)
                                continue

                        data.append( line )

                        sleep (0.00000000000000075)

                npdata = np.array (data, dtype='int')

                npdata = np.uint8(npdata)

                image = Image.fromarray(npdata, mode="P")
                image.save(f"{output + filename.replace('.csv', '')}.png")

                print (f"{filename} DONE")
                i+=1
        
        except:
            print (f"{filename} DID NOT WORK")
            continue

print ("PROCESS COMPLETE")
