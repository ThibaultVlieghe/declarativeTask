import subprocess
import keyboard
import os
import sys
import pickle
from config import rawFolder, soundsFolder, dataFolder, sounds, tempSounds

# Documentation: https://trac.ffmpeg.org/wiki/AudioVolume
# https://ffmpeg.org/ffmpeg.html#Main-options
# https://www.igorkromin.net/index.php/2016/12/23/prevent-errors-during-ffmpeg-execution-in-a-loop/

# How to install ffmpeg on Windows: https://www.wikihow.com/Install-FFmpeg-on-Windows


def play_sound(j):
    subprocess.call('ffplay -nodisp -loglevel quiet -autoexit ' + soundsFolder + tempSounds[j])


def change_volume(j, volume_adjustment_db=0):
    input_sound = soundsFolder + sounds[j]
    output_sound = soundsFolder + tempSounds[j]
    command = 'ffmpeg -loglevel quiet -y -i ' + input_sound + \
              ' -filter:a "volume=' + str(volume_adjustment_db) + 'dB" ' + output_sound + ' -nostdin'
    subprocess.call(command)


def present_options(j):
    if j == 0:
        print "here is the 1st sound"
    elif j == 1:
        print "here is the 2nd sound"
    elif j == 2:
        print "here is the 3rd sound"
    elif j > 3:
        print "here is the " + str(j) + "th sound"

    print "press a to increase the volume, or d to decrease"
    print "You may not increase the sound over 0dB"
    print "if the sound is not high enough, please ask the supervisor to increase system volume"
    print "press q to move onto the next sound"
    print "press any other key to hear the sound again"


def delete_temp_files():
    for j in range(len(sounds)):
        try:
            output_sound = soundsFolder + tempSounds[j]
            os.remove(output_sound)
        except:
            pass


########################################################################################################################
subject_name = ''.join(sys.argv[1:])
soundsVolumeAdjustmentIndB = [0] * len(sounds)

for i in range(len(sounds)):
    dontMoveOn = True
    while dontMoveOn:
        present_options(i)
        change_volume(i, volume_adjustment_db=soundsVolumeAdjustmentIndB[i])
        print "it is now " + str(soundsVolumeAdjustmentIndB) + " dB"
        play_sound(i)
        key = keyboard.read_key()
        if key == 'a' and soundsVolumeAdjustmentIndB[i] + 5 <= 0:
            soundsVolumeAdjustmentIndB[i] += 5
        elif key == 'd':
            soundsVolumeAdjustmentIndB[i] -= 5
        elif key == 'q':
            dontMoveOn = False

delete_temp_files()

# Saving sounds adjustment: (this script is supposed to be executed in src)
subject_file = 'soundsVolumeAdjustmentIndB_' + subject_name + '.pkl'

with open(dataFolder + subject_file, 'w') as f:
    pickle.dump(soundsVolumeAdjustmentIndB, f)
