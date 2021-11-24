import os
import pickle

from checksumdir import dirhash
import osrparse

import hashlib
import glob
import pandas as pd

"""
Method to get an md5 hash of a file
fname: path to the file
"""
def md5(fname):
    # initialize the md5 hash
    hash_md5 = hashlib.md5()
    # open the file im read binary mode
    with open(fname, "rb") as f:
        # split the file into chunks of 4096 bits (md5 hash can only take in 4096 at once)
        for chunk in iter(lambda: f.read(4096), b""):
            # update the hash with the data
            hash_md5.update(chunk)
    # return the hexadecimal hash
    return hash_md5.hexdigest()




"""
Method to map a directory to all of the beatmap hashes within it
directory: path to the beatmap folder
"""
def getHashes(directory):

    # initialize hashes dict
    hashes = {}
    # loop through all subdirectories within the main directory
    for beatmapFolder in os.listdir(directory):
        # create the filepath from the base path and the beatmap folder
        filePath = os.path.join(directory, beatmapFolder)
        # loop through all .osu files in the path
        for diff in glob.glob(os.path.join(filePath, "*.osu")):
            # update the hashes dict with a hash of the beatmap, mapped to it's path
            hashes.update({md5(diff):diff})
    # return the hash map
    return {directory:hashes}


""" 
Method to create the overall beatmap hash map
"""
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
    
    # initializes the final map
    toDataFrame = {}
    # loops through the beatmap base path (key) and hashmap (val) of the respective folder
    for key,val in totalHashMap.items():
        # update the final dict with the hashmap of the folder
        toDataFrame.update(val)
    
    # return the overall map
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

    # load the beatmap hashes
    bmHashes = loadBeatmapHashes(beatmapFiles)

    # loop through all .osr files in the user-specified folder
    for replay in glob.glob(os.path.join(replayFolder, "*.osr")):

        # create the path to the replay file
        replayFile = os.path.join(replayFolder, replay)
        # parse the replay file
        parsed_replay = osrparse.parse_replay_file(replayFile)
        try:
            # try and map the replay to a beatmap using the beatmap hash
            replayMap["BeatmapLocation"].append(bmHashes[parsed_replay.beatmap_hash])
        except KeyError:
            #print(f"===ERROR PROCESSING {replay}: CANNOT FIND BEATMAP LOCATION====")
            continue
        replayMap["ReplayLocation"].append(replayFile)

    # create a pandas dataframe with the hash map
    dataFrame = pd.DataFrame(replayMap)
    return dataFrame



        
        

# if the file is being debugged
if __name__ == "__main__":    
    # map replay files
    dataset = mapReplayFiles("C:\\Users\\joant\\AppData\\Local\\osu!\\Replays", ["D:\\Downloads\\pyOsuV3-main (4)\\pyOsuV3-main\\beatmaps"])
    # print out
    parseDataset(dataset)
    


