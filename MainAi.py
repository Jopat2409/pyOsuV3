import pickle
import os
import glob
import osrparse
import hashlib
import checksumdir
import BeatmapParse
import copy
import matplotlib

from numpy import array
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense

def md5Checksum(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def interpolate(pos1, pos2, cTime):

    prevPos = (pos1.x, pos1.y)
    cPos = (pos2.x, pos2.y)

    timeIn = cTime - pos1.time_delta
    overallTime = pos2.time_delta - pos1.time_delta
    xDiff = cPos[0] - prevPos[0]
    yDiff = cPos[1] - prevPos[1]
    return [int(prevPos[0] + (timeIn/overallTime)*xDiff), int(prevPos[1] + (timeIn/overallTime)*yDiff)]

class BeatmapHash:


    def __init__(self):

        self.beatmapHashMap = {}
        self.includedBeatmaps = []
        self.lastChecksumLocal = ""

class NeuralNetworkPlayer:


    def __init__(self, playerProfile=None):

        if not os.path.exists(".temp"):
            os.mkdir(".temp")
        if not os.path.exists(".temp\\profiles"):
            os.mkdir(".temp\\profiles")


        if playerProfile != None:
            with open(".temp\\profiles/{}.dat".format(playerProfile), "rb") as networkFile:
                self.network = pickle.load(networkFile)
        
        if not os.path.isfile(".temp/beatmaphash.dat"):
            self.createBeatmapHash()
        else:
            self.updateBeatmapHash()
        
        self.playerProfile = playerProfile


        """ ------------------- NEURAL NETWORK TRAINING PARAMETERS -----------------------"""
        self.FPS = 50       # a screenshot of the replay data is taken every 40 ms
    
    
    def createBeatmapHash(self):
        self.beatmapHash = BeatmapHash()
        basePath = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        for beatmap in os.listdir(os.path.join(basePath, "beatmaps")):
            for tempBeatmap in glob.glob(os.path.join(basePath, "beatmaps", beatmap, "*.osu")):
                self.beatmapHash.beatmapHashMap.update({md5Checksum(tempBeatmap):tempBeatmap})
            self.beatmapHash.includedBeatmaps.append(checksumdir.dirhash(os.path.join(basePath, "beatmaps", beatmap)))

        self.beatmapHash.lastChecksumLocal = checksumdir.dirhash(os.path.join(basePath, "beatmaps"))

        with open(".temp/beatmaphash.dat", 'wb') as tempFile:
            pickle.dump(self.beatmapHash, tempFile)

        
    def updateBeatmapHash(self):
        tempBeatmapHash = None
        basePath = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(".temp/beatmaphash.dat", 'rb') as tempFile:
            tempBeatmapHash = pickle.load(tempFile)
        
        if tempBeatmapHash.lastChecksumLocal == checksumdir.dirhash(os.path.join(basePath, "beatmaps")):
            print("The Same")
            self.beatmapHash = tempBeatmapHash
        else:
            total = 0
            tempBeatmapHash.lastChecksumLocal = checksumdir.dirhash(os.path.join(basePath, "beatmaps"))
            for beatmap in os.listdir(os.path.join(basePath, "beatmaps")):
                if checksumdir.dirhash(os.path.join(basePath, "beatmaps", beatmap)) in tempBeatmapHash.includedBeatmaps:
                    continue
                else:
                    total += 1
                    for tempBeatmap in glob.glob(os.path.join(basePath, "beatmaps", beatmap, "*.osu")):
                        tempBeatmapHash.beatmapHashMap.update({md5Checksum(tempBeatmap):tempBeatmap})
                    tempBeatmapHash.includedBeatmaps.append(checksumdir.dirhash(os.path.join(basePath, "beatmaps", beatmap)))
        
            self.beatmapHash = tempBeatmapHash
            with open(".temp/beatmaphash.dat", 'wb') as tempFile:
                pickle.dump(self.beatmapHash, tempFile)
            print("Parsed {} new beatmaps".format(total))
        


    def mapReplayFiles(self, replayFolder):

        replayMap = {}

        for replay in glob.glob(os.path.join(replayFolder, "*.osr")):
            parsedReplay = osrparse.parse_replay_file(os.path.join(replayFolder, replay))
            mapHash = parsedReplay.beatmap_hash
            replayMap.update({replay:self.beatmapHash.beatmapHashMap[mapHash]})
        return replayMap

    def trainNetwork(self, replayFolder):

        mappedReplays = self.mapReplayFiles(replayFolder)
        
        trainingData = self.getIOData(mappedReplays)

        self.network = Sequential()
        self.network.add(LSTM(50, activation='relu', input_shape=()))

    def parseTimeDelta(self, replayData):
        cTimeDelta = 0
        for i in replayData:
            tempTimeDelta = i.time_delta
            i.time_delta += cTimeDelta
            cTimeDelta += tempTimeDelta
        return replayData

    def beatmapParse(self, beatmapFile):

        beatmapHash = md5Checksum(beatmapFile)
        if beatmapHash in self.beatmapTimeSeriesMap:
            print("FOUND ALERADY PARSED BEATMAP YAY")
            return self.beatmapTimeSeriesMap[beatmapHash]

        hitObjectMap = BeatmapParse.aiParse(beatmapFile)

        INPUT_DATA = []
        timeSkip = 1000/self.FPS
        
        cTime = 0
        while cTime < hitObjectMap[-1][2]:
            for i in range(len(hitObjectMap)):
                tempHitObject = copy.deepcopy(hitObjectMap[i])
                if tempHitObject[2] >= cTime:
                    timeLeft = tempHitObject[2] - cTime
                    tempHitObject[2] = timeLeft
                    INPUT_DATA.append(tempHitObject)
                    hitObjectMap = hitObjectMap[i::]
                    break
            cTime += timeSkip
        self.beatmapTimeSeriesMap.update({beatmapHash:INPUT_DATA})
        return INPUT_DATA

        

    def replayParse(self, replay):

        replayHash = md5Checksum(replay)
        if replayHash in self.replayTempMap:
            return self.replayTempMap[replayHash]

        replay = osrparse.parse_replay_file(replay)
        replayData = replay.play_data
        replayData = self.parseTimeDelta(replayData)
        cTime = 0
        timeSkip = 1000/self.FPS

        OUTPUT_DATA = []
        isReading = True
        toPass = 0
        while(isReading):
            for replayEvent in range(len(replayData)):
                #print(replayData[replayEvent].time_delta)
                if replayData[replayEvent].time_delta > cTime:
                    #print("PARSING")
                    toPass = replayEvent
                    OUTPUT_DATA.append(interpolate(replayData[replayEvent-1], replayData[replayEvent], cTime))

                    break
            cTime += timeSkip
            replayData = replayData[toPass::]
            if len(replayData) == 0:
                isReading = False
        self.replayTempMap.update({replayHash:OUTPUT_DATA})
        return OUTPUT_DATA

    def parseData(self, dataToParse):

        """ Takes a data stream consiting of an array of [x, y, timeLeft, isSlider, isSpinner, cursorX, cursorY] and pairs it with the next cursorX, cursorY"""
        inputData = []
        outputData = []
        for i in range(len(dataToParse)-1):


            inputData.append(dataToParse[i])
            outputData.append(dataToParse[i+1][-2::])
            #print(dataToParse[i], "     ", dataToParse[i+1][-2::])
        
        return inputData, outputData


    def getIOData(self, replayMap):

        allDatasets = []

        try:
            with open(".temp\\replaymap.dat", "rb") as tempReplayMap:
                self.replayTempMap = pickle.load(tempReplayMap)
        except FileNotFoundError:
            self.replayTempMap = {}

        try:
            with open(".temp\\beatmapTimeSeriesMap.dat", "rb") as timeSeries:
                self.beatmapTimeSeriesMap = pickle.load(timeSeries)
        except FileNotFoundError:
            self.beatmapTimeSeriesMap = {}

        for replay in replayMap:
            OUTPUT_DATA = self.replayParse(replay)
            INPUT_DATA = self.beatmapParse(replayMap[replay])
            FINAL_DATA = [INPUT_DATA[i]+OUTPUT_DATA[i] for i in range(len(INPUT_DATA))]
            
            xInput, yOutput = self.parseData(FINAL_DATA)
            allDatasets.append((xInput, yOutput))
        with open(".temp\\replaymap.dat", 'wb') as tempReplayMap:
            pickle.dump(self.replayTempMap, tempReplayMap)
        with open(".temp\\beatmapTimeSeriesMap.dat", "wb") as timeSeries:
            pickle.dump(self.beatmapTimeSeriesMap, timeSeries)
        return allDatasets



if __name__ == "__main__":
    print("RUNNING")
    testNetwork = NeuralNetworkPlayer()
    testNetwork.trainNetwork("C:\\Users\\Joe\\Documents\\GitHub\\pyOsuV3\\replaydata")