from time import time
import osrparse
import config



class ArtificialIntelligence:


    def __init__(self, network, beatmapFile):


        self.createReplay(beatmapFile)
    

    def createReplay(self, beatmap):
        
        tempReplay = self.generateData(beatmap)
        self.replay = osrparse.parse_replay_file(tempReplay)
        self.mouseData = self.replay.play_data
        self.getMouseEvents()


    def getCursorPos(self, timePos):
        if self.mouseData[0].time_delta == timePos:
            return (int(self.mouseData[0].x), int(self.mouseData[0].y))
        elif self.mouseData[1].time_delta == timePos:
            self.mouseData.pop(0)
            return (int(self.mouseData[1].x), int(self.mouseData[1].y))
        
        return self.interpolatePosition(timePos)

    def getMouseEvents(self):
        timePos = 0
        for i in self.mouseData:
            tempTime = i.time_delta
            i.time_delta += timePos
            timePos += tempTime
            i.x = i.x*config.CURRENT_SCALING
            i.y = i.y*config.CURRENT_SCALING
    
    def interpolatePosition(self, timePosition):

        cEvent = self.mouseData[1]
        pEvent = self.mouseData[0]

        if timePosition > cEvent.time_delta:
            self.mouseData.pop(0)
            cEvent = self.mouseData[1]
            pEvent = self.mouseData[0]

        if timePosition > pEvent.time_delta and timePosition < cEvent.time_delta:
            #print("interpolated")
            timeDiff = cEvent.time_delta - pEvent.time_delta
            timeRatio = (timePosition - pEvent.time_delta) / timeDiff
            diffX = cEvent.x - pEvent.x
            diffY = cEvent.y - pEvent.y

            tempPos = (int(pEvent.x + diffX*timeRatio), int(pEvent.y + diffY*timeRatio))

            return tempPos
        #print("ERROR: {} is not in between {} and {}".format(timePosition, pEvent.time_delta, cEvent.time_delta))
        return (int(self.mouseData[0].x), int(self.mouseData[0].y))




    def generateData(self, beatmap):
        return "replaydata/WhitecatFool.osr"
    



if __name__ == "__main__":

    ai = ArtificialIntelligence("mrekk", "beatmap")
