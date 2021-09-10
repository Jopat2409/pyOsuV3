import random
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

        # hard coded number representing how many beatmaps are shown on screen at once
        self.BMS = 7
        self.bmHeight = 70
        self.bmMargin = 10
        self.bmOffset = 15

        if os.path.isfile(cPath):
            with open(cPath, 'r') as file:
                self.beatmaps = pickle.load(file)
        else:
            for beatmap in os.listdir("%s/beatmaps/"%config.DEFAULT_PATH):
                PATH = "%s\\beatmaps\\%s"%(config.DEFAULT_PATH, beatmap)
                for diff in glob.glob(PATH + "/" + "*.osu"):
                    
                    self.beatmaps.append(BeatmapParse.shallowRead(diff))


        # points to the current index of the beatmap currently selected
        self.cBeatmap = random.randint(0, len(self.beatmaps))
        print(len(self.beatmaps))
        print(self.cBeatmap)


    def update(self):


        pass


    def drawBeatmapRects(self, surface):

        drawnbeatmaps = []
        drawCount = 0
        for beatmap in range(self.cBeatmap - int((self.BMS-1)/2), self.cBeatmap+int((self.BMS-1)/2)+1):
            try:
                cData = self.beatmaps[beatmap]
            except IndexError:
                break
            tempPos = self.bmMargin*(drawCount+1) + self.bmHeight*drawCount
            if beatmap != self.cBeatmap:
                tempRect = (0 + self.bmOffset, tempPos,config.SCREEN_RESOLUTION[0] / 3 + self.bmOffset, self.bmHeight)
            else:
                tempRect = (0, tempPos,config.SCREEN_RESOLUTION[0] / 3, self.bmHeight)
            pygame.draw.rect(surface, (0,(30*(drawCount+1))%255,0),tempRect)

            drawCount += 1

            

        

        

    def getRenderSnapshot(self, interpolation):

        tempSurface = pygame.Surface(config.SCREEN_RESOLUTION)
        tempSurface.blit(self.bgIMG, (0,0))
        tempSurface.fill((150,150,150))

        beatmapFrame = pygame.Surface((config.SCREEN_RESOLUTION[0] / 3, config.SCREEN_RESOLUTION[1]))

        beatmapFrame.fill((0,0,0))
        self.drawBeatmapRects(beatmapFrame)

        tempSurface.blit(beatmapFrame, ((config.SCREEN_RESOLUTION[0] / 3)*2,0))

        return tempSurface
                
            
            

        # this is for loading up all of the beatmap information that is required


        
