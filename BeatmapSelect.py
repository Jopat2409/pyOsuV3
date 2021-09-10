
import pickle
import os
import config
import glob
import BeatmapParse
import pygame




class gsBeatmapSelect:





    def __init__(self, parentClass):

        self.parentClass = parentClass

        self.beatmaps = []

        cPath = bgPath = config.DEFAULT_PATH + '/temp/beatmapSelect.obj'
        bgPath = config.DEFAULT_PATH + '/assets/bg/online_background_68261587a4e3fbe77cad07120ee1e864.jpg'
        bg = pygame.image.load(bgPath)
        self.bgIMG = pygame.transform.scale(bg, config.SCREEN_RESOLUTION)

        if os.path.isfile(cPath):
            with open(cPath, 'r') as file:
                self.beatmaps = pickle.load(file)
        else:
            for beatmap in os.listdir("%s/beatmaps/"%config.DEFAULT_PATH):
                PATH = "%s\\beatmaps\\%s"%(config.DEFAULT_PATH, beatmap)
                beatmapTemp = []
                for diff in glob.glob(PATH + "/" + "*.osu"):
                    
                    beatmapTemp.append(BeatmapParse.shallowRead(diff))

                self.beatmaps.append(beatmapTemp)

        print(self.beatmaps)


    def getRenderSnapshot(self, interpolation):

        tempSurface = pygame.Surface(config.SCREEN_RESOLUTION)
        tempSurface.blit(self.bgIMG, (0,0))


        return tempSurface
                
            
            

        # this is for loading up all of the beatmap information that is required


        
