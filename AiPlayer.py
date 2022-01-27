""" ---------- OSU MODULES ---------- """
import osrparse
import config

""" ---------- PYTHON MODULES ---------- """
from time import time

"""
Class for playing replay fliles (.osr files)
network: network that will handle the beatmap
beatmapFile: replay file to be played
"""


class ArtificialIntelligence:

    def __init__(self, network, beatmapFile):
        # wether the replay file has been loaded fully
        self.isReady = False
        # create the replay object from the file
        self.createReplay(beatmapFile)

    """
    Gets the required data for the replay file to be viewed
    """

    def createReplay(self, beatmap):

        # parse the replay file using osrparse
        self.replay = osrparse.parse_replay_file(beatmap)
        # get the data
        self.mouseData = self.replay.play_data
        # parse the mouse events
        self.getMouseEvents()
        # set ready to true
        self.isReady = True

    """
    Gets the cursor position of the replay at the time specified
    timePos: current time positon
    verbose: wether or not to print results (for debugging purposes)
    """

    def getCursorPos(self, timePos, verbose=False):

        if verbose:
            print(f"Current time is {timePos}, first mouse data time is {self.mouseData[0]}")

        # loop through mouse data
        for i in range(len(self.mouseData)):
            # get the current mouse data
            mousePos = self.mouseData[i]
            # if the time_delta of the mouse state matches the time position exactly (unlikely)
            if mousePos.time_delta == timePos:
                # simply return the x and y coordinate
                return [mousePos.x, mousePos.y]
            # else if the time_delta is between two mouse states
            elif mousePos.time_delta > timePos:
                # return the result of the interpolation between position i-1 and i
                return self.interpolatePosition(i - 1, i, timePos, verbose)

    """
    Parse the mouse events that were loaded, as mouse events are stored as [deltatime, x, y]
    when we need the format [time, x, y]
    """

    def getMouseEvents(self):
        # initialize the time position
        timePos = 0
        timeDeltaString = ""
        # loop through the mouse events
        for i in self.mouseData:
            # add the delta time (time since the last event)
            tempTime = i.time_delta
            # update the time to reflect that change
            i.time_delta += timePos
            # increment the timePos 
            timePos += tempTime
            # scale the x value to equate for scaling and x offset
            i.x = int(i.x * config.CURRENT_SCALING) + config.xOffset
            # scale the y value to equate for scaling and x offset
            i.y = int(i.y * config.CURRENT_SCALING) + config.yOffset

            timeDeltaString += str(i.time_delta) + " "
        print(timeDeltaString)

    """
    Interpolates the mouse position to fit the current time position in the song
    firstIndex: index of first mouse event to interpolate between
    secondIndex: index of the second mouse event to interpolate
    timePos: current time within the song
    verbose: wether or not the results will be printed (used for debugging)
    """

    def interpolatePosition(self, firstIndex, secondIndex, timePos, verbose=False):

        # get the mouse data for the first position
        pMData = self.mouseData[firstIndex]
        # get the mouse data for the second position
        cMData = self.mouseData[secondIndex]

        # if verbose, print some information about the process
        if verbose:
            print(f"{firstIndex} - {secondIndex}")
            print(f"{pMData.time_delta} < {timePos} < {cMData.time_delta}")

        # calculate the percentage between the two times that timePos is
        timeRatio = (timePos - pMData.time_delta) / (cMData.time_delta - pMData.time_delta)
        # if verbose, print the result
        if verbose:
            print(f"{timeRatio * 100}% of the way through")

        # calculate the difference in x position
        xDiff = int(pMData.x + (cMData.x - pMData.x) * timeRatio)
        # calculate the difference in y position
        yDiff = int(pMData.y + (cMData.y - pMData.y) * timeRatio)
        # if verbose, print some more information
        if verbose:
            print(f"{pMData.x} ---- {xDiff} ---- {cMData.x}")
            print(f"{pMData.y} ---- {xDiff} ---- {cMData.y}\n")

        # return a tuple containing the x difference and the y difference
        return (xDiff, yDiff)

    def generateData(self, beatmap):
        return "replaydata/WhitecatFool.osr"


# if the file is being ran for debugging purposes
if __name__ == "__main__":
    # create the ai
    ai = ArtificialIntelligence("mrekk", "beatmap")
    # get cursor position for 10000 timesteps
    for i in range(0, 10000):
        ai.getCursorPos(i)
