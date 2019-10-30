import keyboard
import sys
from ld_sound import *

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
