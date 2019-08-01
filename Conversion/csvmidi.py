import os

directory = "/Users/Nick/Desktop/Audio_Data/CSV_Ouptut/"
output = "/Users/Nick/Desktop/Audio_Data/MIDI_Output/"

for filename in os.listdir(directory):

    if not filename.startswith('.'):

        command = f"csvmidi -v '{directory + filename}' '{output + filename.replace('.csv', '')}.mid'"
        os.system(command)