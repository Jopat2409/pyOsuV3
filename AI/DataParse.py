
import os
import hashlib
# import filedialog module
import glob
from tkinter import filedialog, Tk
import osrparse

BUF_SIZE = 65536 


def HASH_MD5(toHash):
    
    md5 = hashlib.md5()

    with open(toHash, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)

    return md5.hexdigest()

def GetDirFromDialogue():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    return filedialog.askdirectory()



def LoadReplaysFromFile(filePath : str):

    if not os.path.isdir(filePath):
        return

    returnArray = []
        
    for _replay in glob.glob(os.path.join(filePath, "*.osr")):
        returnArray.append(osrparse.parse_replay_file(_replay))

    return returnArray

def LoadBeatmapsFromSelectedFiles(*filePath):

    bmHash = {}
    
    for _fp in filePath:

        for _bmFile in os.listdir(_fp):

            for _osFile in glob.glob(os.path.join(_fp, _bmFile, "*.osu")):
                
                fullPath = os.path.join(_bmFile, _osFile)
                bmHash.update({HASH_MD5(fullPath): fullPath})
            
    return bmHash


def MapBeatmaps(replayFolder, *beatmapFiles):

    replays = LoadReplaysFromFile(replayFolder)
    bmMap = LoadBeatmapsFromSelectedFiles(*beatmapFiles)

    bmDict = {}
    for _rp in replays:
        if _rp.beatmap_hash in bmMap:
            bmDict.update({_rp: bmMap[_rp.beatmap_hash]})

    


def tempReplay():
    rFolder = GetDirFromDialogue()
    bFolder = GetDirFromDialogue()
    MapBeatmaps(rFolder, bFolder)

tempReplay()
