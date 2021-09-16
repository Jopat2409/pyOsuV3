import BeatmapParse
import pygame
import config
import pygame.gfxdraw
import os


class gsBeatmapPlayer:



    def __init__(self, PATH, parentClass):

        self.parent = parentClass
        self.soundHandler = parentClass.soundStream
        print(PATH)
        self.playingBeatmap = PATH
        self.hitObjects = BeatmapParse.fullParse(self.playingBeatmap["osuPath"])
        print(self.hitObjects)

        self.getMapValues()

        self.soundHandler.playSong(self.playingBeatmap["BasePath"]+"/"+self.playingBeatmap["AudioFilename"])

        PATH = os.path.join(self.playingBeatmap["BasePath"],self.playingBeatmap["BackgroundImage"])
        PATH = PATH.replace("\\","/")
        bg = pygame.image.load(PATH.strip())
        self.bgIMG = pygame.transform.scale(bg, config.SCREEN_RESOLUTION)


    def getMapValues(self):

        # calculate the AR timings
        if int(self.playingBeatmap["ApproachRate"]) < 5:
            self.fadeInTime = 800 + 400*((5-int(self.playingBeatmap["ApproachRate"])) / 5)
            self.fadeInStart = 1200 + 600*((5-int(self.playingBeatmap["ApproachRate"])) / 5)
        elif int(self.playingBeatmap["ApproachRate"]) == 5:
            self.fadeInTime = 800
            self.fadeInStart = 1200
        elif int(self.playingBeatmap["ApproachRate"]) > 5:
            self.fadeInTime = 800 - 500*((int(self.playingBeatmap["ApproachRate"])-5)/5)
            self.fadeInStart = 1200 - 750*((int(self.playingBeatmap["ApproachRate"])-5)/5)

        self.radius = 75



    def getRenderSnapshot(self, interpolation):

        tempSurface = pygame.Surface(config.SCREEN_RESOLUTION)
        tempSurface.blit(self.bgIMG, (0,0))
        if config.safeMode: 
            tempSurface.fill((0,0,0))

        
        for hitObject in self.hitObjects:
            if self.soundHandler.musicChannel.get_pos()+self.fadeInStart >= int(hitObject[2]):
                alpha =  255 / self.fadeInTime * (self.soundHandler.musicChannel.get_pos() - (int(hitObject[2]) - self.fadeInStart))
                if alpha >= 255:
                    alpha = 255
              
                pygame.gfxdraw.filled_circle(tempSurface, int(int(hitObject[0])*config.CURRENT_SCALING), int(int(hitObject[1])*config.CURRENT_SCALING), 76, (255,255,255,alpha))
                pygame.gfxdraw.filled_circle(tempSurface, int(int(hitObject[0])*config.CURRENT_SCALING), int(int(hitObject[1])*config.CURRENT_SCALING), 70, (255,0,0,alpha))


        return tempSurface




    def update(self):

        if int(self.hitObjects[0][2]) < self.soundHandler.musicChannel.get_pos():
            self.hitObjects.pop(0)

        
