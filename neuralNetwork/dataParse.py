import os
import pickle

from checksumdir import dirhash
import osrparse

import hashlib
import glob


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def getHashes(directory):

    hashes = {}
    print(directory)
    for beatmapFolder in os.listdir(directory):
        print(beatmapFolder)
        filePath = os.path.join(directory, beatmapFolder)
        for diff in glob.glob(os.path.join(filePath, "*.osu")):
            print(diff)
            hashes.update({md5(diff):diff})
            
    return hashes

def loadBeatmapHashes(beatmapDirectories):

    checkHashDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".temp/beatmapHashData.dat")
    if os.path.exists(checkHashDir):
        with open(checkHashDir, 'rb') as file:
            beatmapHashes = pickle.load(file)
    else:
        beatmapHashes = [{"FilePath":i,"CheckSum":dirhash(i),"Data":getHashes(i)} for i in beatmapDirectories]
        with open(checkHashDir, 'wb') as file:
            pickle.dump(file)

    return beatmapHashes

                
            
            


"""
Maps replay paths to beatmap files
Param: replayFolder - folder that replays are stored in
Param: addBeatmapFolders - additional beatmap folders to be considered
"""
def mapReplayFiles(replayFolder, *args):

    if not os.path.exists(replayFolder):
        print("ERROR: Replay file {} does not exist, please try again")
        return

    osuPath = os.path.join(os.getenv('LocalAppData'), "osu!")

    beatmapFiles = [os.path.join(osuPath, "beatmaps")] + list(args)
    # check if it exists, if not then exit as we cannot extract the needed data
    if not os.path.exists(osuPath):
        print("Cannot find a local installation of osu!")
        beatmapFiles = list(args)
        if len(args) == 0:
            print("No other beatmap locations are found.... returning")
            return

    
    bmHashes = loadBeatmapHashes(beatmapFiles)
    print(bmHashes)
    
    for replayFile in glob.glob(replayFolder):

        replayFullpath = os.path.join(replayFolder, replayFile)

        parsedReplay = osrparse.parse_replay_file(replayFullPath)

        replayBeatmapMap.update({beatmapFiles[beatmap_hash]:replayFullpath})
    
mapReplayFiles("R:\\Desktop\\neuralNetwork\\replays", "R:\\Desktop\\neuralNetwork\\beatmaps")
