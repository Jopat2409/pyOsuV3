import threading
import glob
import time
import os
import config
import Loader
import pickle
import checksumdir
import BeatmapParse

class BeatmapLoader(Loader.Loader):

    def __init__(self):
        super(BeatmapLoader, self).__init__({str:list})

    def IsActive(self):
        return super(BeatmapLoader, self).is_alive()

    def Load(self):

        # initialize the timer for timing how long it takes to load beatmaps
        self.beatmaps = []
        bmLoadStart = time.time()
        # checks for beatmap cache
        cPath = config.DEFAULT_PATH + '\\.temp\\beatmapSelect.dat'
        # checks to see if a beatmap cache already exists
        if os.path.isfile(cPath):
            # if it does, load the objects stored in at directory cPath as self.beatmaps
            # read bytes of the cache file
            with open(cPath, 'rb') as file:
                # store the beatmap information
                data = pickle.load(file)
            # store the beatmap array in the current beatmap array
            self.beatmaps = data[0]
        else:
            # if it does not exist
            count = 0
            bmParsed = []
            # loop through all beatmap directories
            for beatmap in os.listdir("%s/beatmaps/" % config.DEFAULT_PATH):
                PATH = "%s\\beatmaps\\%s" % (config.DEFAULT_PATH, beatmap)
                # append the checksum of the beatmap directory (used for loading when changed)
                bmParsed.append(checksumdir.dirhash(PATH))
                # loop through all .osu files in beatmap directory
                for diff in glob.glob(PATH + "/" + "*.osu"):
                    # parse .osu file and append it to list of beatmaps
                    self.beatmaps.append(BeatmapParse.shallowRead(diff, PATH))
                    count += 1
            print(f"Loaded {count} new beatmaps!")
            # writes it to cPath when all beatmaps are parsed
            with open(cPath, 'wb') as beatmapFile:
                tempData = (self.beatmaps, bmParsed)
                pickle.dump(tempData, beatmapFile)

        print("It took {}s to load all beatmaps".format(time.time() - bmLoadStart))
        return self.beatmaps

    
