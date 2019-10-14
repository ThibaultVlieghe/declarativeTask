import os
import sys

from config import numberLearningSubUnits

argument = "".join(sys.argv[1:])
for i in range(numberLearningSubUnits):
    os.system("python src/ld_declarativeTask.py " + argument + ' ' + str(i))
