from typing import overload
import config


def getAR(approachRate):

    preempt = 0
    fadeIn = 0

    if approachRate > 5:
        preempt = 1200 - 750*(approachRate-5)/5
        fadeIn = 800 - 500*(approachRate-5)/5
    elif approachRate < 5:
        preempt = 1200 + 600*(approachRate-5)/5
        fadeIn = 800 + 400*(approachRate-5)/5
    else:
        preempt = 1200
        fadeIn = 800

    return(preempt, fadeIn)


def getCS(circleSize):

    return int((54.4 - 4.48 * circleSize)*config.CURRENT_SCALING)


def getHitWindows(overallDifficulty):

    return {50:(400-20*overallDifficulty)/2,
            100:(280-16*overallDifficulty)/2,
            300:(160-12*overallDifficulty)/2}