from time import time
import osrparse
import config
import time


class ArtificialIntelligence:


    def __init__(self, network, beatmapFile):

        self.isReady = False
        self.createReplay(beatmapFile)
    

    def createReplay(self, beatmap):
        
        tempReplay = self.generateData(beatmap)
        self.replay = osrparse.parse_replay_file(tempReplay)
        self.mouseData = self.replay.play_data
        self.getMouseEvents()
        self.isReady = True


    def getCursorPos(self, timePos, verbose=False):

        if verbose:
                print(f"Current time is {timePos}, first mouse data time is {self.mouseData[0]}")

        for i in range(len(self.mouseData)):
            mousePos = self.mouseData[i]
            
            if mousePos.time_delta == timePos:
                return [mousePos.x, mousePos.y]
            elif mousePos.time_delta > timePos:
                return self.interpolatePosition(i-1, i, timePos, verbose)

    def getMouseEvents(self):
        timePos = 0
        timeDeltaString = ""
        for i in self.mouseData:
            tempTime = i.time_delta
            i.time_delta += timePos
            timePos += tempTime
            i.x = int(i.x*config.CURRENT_SCALING) + config.xOffset
            i.y = int(i.y*config.CURRENT_SCALING) + config.yOffset

            timeDeltaString += str(i.time_delta) + " "
        print(timeDeltaString)
        
    
    def interpolatePosition(self, firstIndex, secondIndex, timePos, verbose=False):

        

        pMData = self.mouseData[firstIndex]
        cMData = self.mouseData[secondIndex]
        
        if verbose:
            print(f"{firstIndex} - {secondIndex}")
            print(f"{pMData.time_delta} < {timePos} < {cMData.time_delta}")
        
        timeRatio = (timePos-pMData.time_delta) / (cMData.time_delta-pMData.time_delta)
        if verbose:
            print(f"{timeRatio*100}% of the way through")
            
        

        xDiff = int(pMData.x + (cMData.x - pMData.x)*timeRatio)
        yDiff = int(pMData.y + (cMData.y - pMData.y)*timeRatio)
        if verbose:
            print(f"{pMData.x} ---- {xDiff} ---- {cMData.x}")
            print(f"{pMData.y} ---- {xDiff} ---- {cMData.y}\n")
        

        return (xDiff, yDiff)



    def generateData(self, beatmap):
        return "replaydata/WhitecatFool.osr"
    



if __name__ == "__main__":

    ai = ArtificialIntelligence("mrekk", "beatmap")

    for i in range(0, 10000):
        ai.getCursorPos(i)

