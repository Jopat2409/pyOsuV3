import os
import pickle

from checksumdir import dirhash
import osrparse

import hashlib
import glob
import pandas as pd


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()





def getHashes(directory):

    hashes = {}
    for beatmapFolder in os.listdir(directory):
        print(beatmapFolder)
        filePath = os.path.join(directory, beatmapFolder)
        for diff in glob.glob(os.path.join(filePath, "*.osu")):
            hashes.update({md5(diff):diff})
            
    return {directory:hashes}

def loadBeatmapHashes(beatmapDirectories):

    # creates the hash map
    totalHashMap = {}
    # gets the directory of temporary files
    cacheDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".temp")
    # if the temp directory does not exist, make one
    if not os.path.isdir(cacheDir):
        os.mkdir(cacheDir)
    # create the path of the cache file
    hashMapDir = os.path.join(cacheDir, "aiData.dat")

    # if the cache file exists, load data from it
    if os.path.isfile(hashMapDir):
        with open(hashMapDir, "rb") as file:
            totalHashMap = pickle.load(file)

    # afterwards, update the cache file with any directories that were not present
    for beatmapDir in beatmapDirectories:
        if beatmapDir in totalHashMap:
            continue
        totalHashMap.update(getHashes(beatmapDir))

    # save the cache file
    with open(hashMapDir, "wb") as file:
        pickle.dump(totalHashMap, file)
    

    toDataFrame = {}
    for key,val in totalHashMap.items():
        toDataFrame.update(val)
        
    return toDataFrame

                
"""
Maps replay paths to beatmap files
Param: replayFolder - folder that replays are stored in
Param: addBeatmapFolders - additional beatmap folders to be considered
"""
def mapReplayFiles(replayFolder, args):

    replayMap = {"ReplayLocation":[],"BeatmapLocation":[]}

    # returns the function if the replay folder does not exist
    if not os.path.exists(replayFolder):
        print("ERROR: Replay file {} does not exist, please try again")
        return 0

    # gets the path of the local installation
    osuPath = os.path.join(os.getenv('LocalAppData'), "osu!")

    # creates an array containing all of the directories beatmaps can be found
    beatmapFiles = [os.path.join(osuPath, "Songs")] + list(args)
    # check if it exists, if not then exit as we cannot extract the needed data
    if not os.path.exists(osuPath):
        print("Cannot find a local installation of osu!")
        # update beatmap files with just the beatmap directories specified by the user
        beatmapFiles = list(args)
        # if none exist, return the function
        if len(args) == 0:
            print("No other beatmap locations are found.... returning")
            return 0 

    
    bmHashes = loadBeatmapHashes(beatmapFiles)

    for replay in glob.glob(os.path.join(replayFolder, "*.osr")):

        replayFile = os.path.join(replayFolder, replay)
        parsed_replay = osrparse.parse_replay_file(replayFile)
        try:
            replayMap["BeatmapLocation"].append(bmHashes[parsed_replay.beatmap_hash])
        except KeyError:
            #print(f"===ERROR PROCESSING {replay}: CANNOT FIND BEATMAP LOCATION====")
            continue
        replayMap["ReplayLocation"].append(replayFile)

    dataFrame = pd.DataFrame(replayMap)
    return dataFrame



        
        

    
if __name__ == "__main__":    
    
    dataset = mapReplayFiles("C:\\Users\\joant\\AppData\\Local\\osu!\\Replays", ["D:\\Downloads\\pyOsuV3-main (4)\\pyOsuV3-main\\beatmaps"])

    parseDataset(dataset)
    


