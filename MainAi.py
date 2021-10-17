import pickle
import os
import glob
import osrparse
import hashlib



def md5Checksum(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


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

        
        self.playerProfile = playerProfile
    
    
    def createBeatmapHash(self):
        replayHashFiles = {}

        for beatmap in glob.glob("\\beatmaps"):
            for difficulty in glob.glob(os.path.join("\\beatmaps", beatmap, "*.osu")):
                print(difficulty)




    def mapReplayFiles(self, replayFolder):

        for replay in glob.glob(os.path.join(replayFolder, "*.osr")):
            parsedReplay = osrparse.parse_replay_file(os.path.join(replayFolder, replay))
            mapHash = parsedReplay.beatmap_hash


    def trainNetwork(self, replayFolder):

        mappedReplays = self.mapReplayFiles(replayFolder)

            