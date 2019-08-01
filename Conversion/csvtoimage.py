import os
import cv2
import csv
import numpy as np
from math import exp, sqrt

# REFERENCE #
# https://stackoverflow.com/questions/7063437/midi-timestamp-in-seconds

directory = "/Users/Nick/Desktop/Audio_Data/CSV/"
output = "/Users/Nick/Desktop/Audio_Data/Formatted_CSV/"

header = {
    "track": 0, 
    "time": 1,
    "c_event": 2,
    "channel": 3, 
    "note": 4,
    "velocity": 5,
}

with open(directory + "1-02_Chrono_Trigger.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    csv = list(csv_reader)

    bpm = (int(csv[3][3]) / 500000) * 120
    print (f"{bpm} BEATS PER MINUTE")

    mClockPerMin = bpm * 24
    print (f"{mClockPerMin} MIDI CLOCK TICKS PER MINUTE")

    duration = sqrt((int (csv[len(csv) - 2][1]) / mClockPerMin))
    print (f"DURATION OF {duration} MINUTES?")

    height = 96
    width = (int (csv[len(csv) - 2][1]) / int(csv[0][5]))

    image = np.zeros((height , int (width) , 3), np.uint8)


    # for row in csv:
    #     print (row)
    # print(f'Processed {line_count} lines.')

# cv2.imshow('Image', image)

# cv2.waitKey(0)
# cv2.destroyAllWindows()

# for filename in os.listdir(directory):

#     if not filename.startswith('.'):
