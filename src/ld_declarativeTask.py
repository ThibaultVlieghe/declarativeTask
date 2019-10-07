import sys

import numpy as np
from expyriment import control, stimuli, io, design, misc
from expyriment.misc import constants
from expyriment.misc._timer import get_time

from ld_matrix import LdMatrix
from ld_utils import setCursor, newRandomPresentation, getPreviousMatrix, path_leaf, readMouse
from config import *

if not windowMode:  # Check WindowMode and Resolution
    control.defaults.window_mode = windowMode
    control.defaults.window_size = misc.get_monitor_resolution()
    windowSize = control.defaults.window_size
else:
    control.defaults.window_mode = windowMode
    control.defaults.window_size = windowSize

if debug:
    control.set_develop_mode(True)

arguments = str(''.join(sys.argv[1:])).split(',')  # Get arguments - experiment name and subject

experimentName = arguments[0]
subjectName = arguments[1]

exp = design.Experiment(experimentName)  # Save experiment name
exp.add_experiment_info(['Subject: '])  # Save Subject Code
exp.add_experiment_info([subjectName])  # Save Subject Code

# Save time, nblocks, position, correctAnswer, RT
exp.add_data_variable_names(['Time', 'NBlock', 'Picture', 'Answers', 'RT'])

m = LdMatrix(matrixSize, windowSize)  # Create Matrix

if experimentName == 'DayOne-Learning':
    oldListPictures = None
    keepMatrix = True
elif experimentName == 'DayOne-TestLearning':
    oldListPictures = getPreviousMatrix(subjectName, 0, 'DayOne-Learning')
    keepMatrix = True
    nbBlocksMax = 1
elif experimentName == 'DayTwo-TestLearning':
    oldListPictures = getPreviousMatrix(subjectName, 1, 'DayOne-Learning')
    keepMatrix = True
    nbBlocksMax = 1
elif experimentName == 'DayTwo-TestInterference':
    oldListPictures = getPreviousMatrix(subjectName, 0, 'DayTwo-Interference')
    keepMatrix = True
    nbBlocksMax = 1
elif experimentName == 'DayTwo-Interference':
    oldListPictures = getPreviousMatrix(subjectName, 1, 'DayOne-Learning')
    keepMatrix = False
elif experimentName == 'DayThree-TestLearning':
    oldListPictures = getPreviousMatrix(subjectName, 2, 'DayOne-Learning')
    keepMatrix = True
    nbBlocksMax = 1
elif experimentName == 'DayThree-TestInterference':
    oldListPictures = getPreviousMatrix(subjectName, 1, 'DayTwo-Interference')
    keepMatrix = True
    nbBlocksMax = 1

if oldListPictures is False:
    print FAIL + "Warning: no old list of pictures found" + ENDC
    sys.exit()

newMatrix = m.findMatrix(oldListPictures, keepMatrix)  # Find newMatrix


exp.add_experiment_info(['Positions pictures:'])

control.initialize(exp)

m.associatePictures(newMatrix)  # Associate Pictures to cards

exp.add_experiment_info([m.listPictures])  # Add listPictures

control.start(exp, auto_create_subject_id=True, skip_ready_screen=True)

mouse = io.Mouse()  # Create Mouse instance
mouse.set_logging(True)  # Log mouse
mouse.hide_cursor(True, True)  # Hide cursor

setCursor(arrow)

bs = stimuli.BlankScreen(bgColor)  # Create blank screen
m.plotDefault(bs, True)  # Draw default grid

exp.clock.wait(shortRest)

correctAnswers = np.zeros(nbBlocksMax)
currentCorrectAnswers = 0
nBlock = 0

instructionRectangle = stimuli.Rectangle(size=(windowSize[0], m.gap * 2 + cardSize[1]), position=(
    0, -windowSize[1]/float(2) + (2 * m.gap + cardSize[1])/float(2)), colour=constants.C_DARKGREY)

''' Presentation all locations '''
presentationOrder = newRandomPresentation()

while currentCorrectAnswers < correctAnswersMax and nBlock < nbBlocksMax:
    presentationOrder = newRandomPresentation(presentationOrder)
    if 1 != nbBlocksMax:
        exp.add_experiment_info(['Block {} - Presentation'.format(nBlock)])  # Add listPictures
        exp.add_experiment_info(presentationOrder)  # Add listPictures
        instructions = stimuli.TextLine(' PRESENTATION ',
                                        position=(0, -windowSize[1]/float(2) + (2*m.gap + cardSize[1])/float(2)),
                                        text_font=None, text_size=textSize, text_bold=None, text_italic=None,
                                        text_underline=None, text_colour=textColor,
                                        background_colour=bgColor,
                                        max_width=None)
        instructionRectangle.plot(bs)
        instructions.plot(bs)
        bs.present(False, True)

        exp.clock.wait(shortRest)
        instructionRectangle.plot(bs)
        bs.present(False, True)

        ISI = design.randomize.rand_int(min_max_ISI[0], min_max_ISI[1])
        exp.clock.wait(ISI)

        for nCard in presentationOrder:
            mouse.hide_cursor(True, True)
            m.plotCard(nCard, True, bs, True)  # Show Location for ( 2s )
            exp.clock.wait(presentationCard)
            m.plotCard(nCard, False, bs, True)

            ISI = design.randomize.rand_int(min_max_ISI[0], min_max_ISI[1])
            exp.clock.wait(ISI)

    instructions = stimuli.TextLine(' TEST ',
                                    position=(0, -windowSize[1]/float(2) + (2*m.gap + cardSize[1])/float(2)),
                                    text_font=None, text_size=textSize, text_bold=None, text_italic=None,
                                    text_underline=None, text_colour=textColor,
                                    background_colour=bgColor,
                                    max_width=None)
    instructionRectangle.plot(bs)
    instructions.plot(bs)
    bs.present(False, True)

    exp.clock.wait(shortRest)  # Short Rest between presentation and cue-recall

    instructionRectangle.plot(bs)
    bs.present(False, True)

    ISI = design.randomize.rand_int(min_max_ISI[0], min_max_ISI[1])
    exp.clock.wait(ISI)

    ''' Cue Recall '''
    presentationOrder = newRandomPresentation(presentationOrder)
    exp.add_experiment_info(['Block {} - Test'.format(nBlock)])  # Add listPictures
    exp.add_experiment_info(presentationOrder)
    for nCard in presentationOrder:

        m._cueCard.setPicture(m._matrix.item(nCard).stimuli[0].filename)  # Associate Picture to CueCard

        m.plotCueCard(True, bs, True)  # Show Cue

        exp.clock.wait(presentationCard)  # Wait presentationCard

        m.plotCueCard(False, bs, True)  # Hide Cue

        mouse.show_cursor(True, True)

        start = get_time()
        rt, position = readMouse(start, mouseButton, responseTime)

        mouse.hide_cursor(True, True)
        if rt is not None:

            currentCard = m.checkPosition(position)

            if currentCard is not None and currentCard not in removeCards:
                m._matrix.item(currentCard).color = clickColor
                m.plotCard(currentCard, False, bs, True)

                exp.clock.wait(clicPeriod)  # Wait 200ms

                m._matrix.item(currentCard).color = cardColor
                m.plotCard(currentCard, False, bs, True)

            if currentCard == nCard:
                correctAnswers[nBlock] += 1
                exp.data.add([exp.clock.time, nBlock,
                              path_leaf(m._matrix.item(nCard).stimuli[0].filename),
                              path_leaf(m._matrix.item(currentCard).stimuli[0].filename),
                              rt])

            elif currentCard is None:
                exp.data.add([exp.clock.time, nBlock,
                              path_leaf(m._matrix.item(nCard).stimuli[0].filename),
                              None,
                              rt])
            else:
                exp.data.add([exp.clock.time, nBlock,
                              path_leaf(m._matrix.item(nCard).stimuli[0].filename),
                              path_leaf(m._matrix.item(currentCard).stimuli[0].filename),
                              rt])
        else:
            exp.data.add([exp.clock.time, nBlock,
                          path_leaf(m._matrix.item(nCard).stimuli[0].filename),
                          None,
                          rt])

        ISI = design.randomize.rand_int(min_max_ISI[0], min_max_ISI[1])
        exp.clock.wait(ISI)

    currentCorrectAnswers = correctAnswers[nBlock]  # Number of correct answers

    #if currentCorrectAnswers < correctAnswersMax and nBlock + 1 < nbBlocksMax:
    if nbBlocksMax != 1:

        instructions = stimuli.TextLine('You got ' + str(int(correctAnswers[nBlock])) + ' out of ' + str(m._matrix.size-len(removeCards)),
                                        position=(0, -windowSize[1]/float(2) + (2*m.gap + cardSize[1])/float(2)),
                                        text_font=None, text_size=textSize, text_bold=None, text_italic=None,
                                        text_underline=None, text_colour=textColor, background_colour=bgColor,
                                        max_width=None)
        instructions.plot(bs)
        bs.present(False, True)

        exp.clock.wait(shortRest)

        instructionRectangle.plot(bs)
        bs.present(False, True)

    instructions = stimuli.TextLine(
        ' REST ',
        position=(0, -windowSize[1]/float(2) + (2*m.gap + cardSize[1])/float(2)),
        text_font=None, text_size=textSize, text_bold=None, text_italic=None,
        text_underline=None, text_colour=textColor, background_colour=bgColor,
        max_width=None)

    instructions.plot(bs)
    bs.present(False, True)

    exp.clock.wait(shortRest)

    instructionRectangle.plot(bs)
    bs.present(False, True)

    exp.clock.wait(restPeriod)

    nBlock += 1

exp.clock.wait(5000)
control.end()
