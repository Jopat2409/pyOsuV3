import pickle
import os
import glob
import osrparse
import hashlib
import checksumdir


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
    return (int(prevPos[0] + (timeIn/overallTime)*xDiff), int(prevPos[1] + (timeIn/overallTime)*yDiff))

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
        self.FPS = 25       # a screenshot of the replay data is taken every 40 ms
    
    
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
            replayMap.update({parsedReplay:self.beatmapHash.beatmapHashMap[mapHash]})
        return replayMap

    def trainNetwork(self, replayFolder):

        mappedReplays = self.mapReplayFiles(replayFolder)
        
        trainingData = self.getIOData(mappedReplays)

    def parseTimeDelta(self, replayData):
        cTimeDelta = 0
        for i in replayData:
            tempTimeDelta = i.time_delta
            i.time_delta += cTimeDelta
            cTimeDelta += tempTimeDelta
        return replayData

    def replayParse(self, replay):

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
        return OUTPUT_DATA
                

    def getIOData(self, replayMap):

        for replay in replayMap:
            OUTPUT_DATA = self.replayParse(replay)
            INPUT_DATA = self.beatmapParse(replayMap[replay])



if __name__ == "__main__":
    print("RUNNING")
    testNetwork = NeuralNetworkPlayer()
    testNetwork.trainNetwork("C:\\Users\\Joe\\Documents\\GitHub\\pyOsuV3\\replaydata")