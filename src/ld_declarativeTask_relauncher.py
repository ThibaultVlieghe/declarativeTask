import os
import sys

from time import time

from config import numberLearningSubUnits
from ld_utils import getPreviousState

argument = "".join(sys.argv[1:])
print "argument"
print argument  # TEMP
for i in range(numberLearningSubUnits):
    if i == 0:
        firstTime = str(time())
    else:
        arguments = argument.split(',')
        print "arguments"
        print arguments  # TEMP
        subjectName = arguments[1]
        if getPreviousState(subjectName, 0, 'DayOne-Learning'):
            break
    print "argument"
    print argument  # TEMP
    print """\"python src/ld_declarativeTask.py " + argument + ' ' + str(i) + ' ' + firstTime"""
    print "python src/ld_declarativeTask.py " + argument + ' ' + str(i) + ' ' + firstTime
    os.system("python src/ld_declarativeTask.py " + argument + ' ' + str(i) + ' ' + firstTime)
