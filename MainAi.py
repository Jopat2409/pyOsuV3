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

        for replay in glob.glob(os.path.join(replayFolder, "*.osr")):
            parsedReplay = osrparse.parse_replay_file(os.path.join(replayFolder, replay))
            mapHash = parsedReplay.beatmap_hash


    def trainNetwork(self, replayFolder):

        mappedReplays = self.mapReplayFiles(replayFolder)



if __name__ == "__main__":
    print("RUNNING")
    testNetwork = NeuralNetworkPlayer()