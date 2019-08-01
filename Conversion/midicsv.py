import os

directory = "/Users/Nick/Desktop/Audio_Data/MIDI/"
output = "/Users/Nick/Desktop/Audio_Data/CSV/"

for filename in os.listdir(directory):

    if not filename.startswith('.'):
        print (filename)
        command = f"midicsv -v '{directory + filename}' '{output + filename.replace('.mid', '')}.csv'"
        os.system(command)