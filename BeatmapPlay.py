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

        self.cFont = pygame.font.SysFont('Arial', 40)


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

        self.radius = int(config.CURRENT_SCALING*(54.4-4.48*int(self.playingBeatmap["CircleSize"])))
        self.innerRadius = int(self.radius*0.9)
        self.hCircleRadius = self.radius*2

        self.xOffset = int((config.SCREEN_RESOLUTION[0] - config.DEFAULT_RESOLUTION[0]*config.CURRENT_SCALING)/2)

        print("X offset: {}".format(self.xOffset))



    def getRenderSnapshot(self, interpolation):

        tempSurface = pygame.Surface(config.SCREEN_RESOLUTION)
        tempSurface.blit(self.bgIMG, (0,0))
        tempSurface.fill((0,0,0))

        combo = 0
        for hitObject in self.hitObjects:
            combo += 1
            cPos = self.soundHandler.musicChannel.get_pos()
            if cPos+self.fadeInStart >= int(hitObject[2]):
                alpha =  255 / self.fadeInTime * (cPos - (int(hitObject[2]) - self.fadeInStart))
                if alpha >= 255:
                    alpha = 255

                aCircleRadius = self.radius + self.hCircleRadius * ((int(hitObject[2])-cPos) / self.fadeInStart)
                cX = self.xOffset + int(int(hitObject[0])*config.CURRENT_SCALING)
                cY = int(int(hitObject[1])*config.CURRENT_SCALING)
              
                pygame.gfxdraw.filled_circle(tempSurface, cX, cY, self.radius, (255,255,255))
                pygame.gfxdraw.filled_circle(tempSurface, cX, cY, self.innerRadius, (0,0,0))
                for i in range(0,5):
                    pygame.gfxdraw.aacircle(tempSurface, cX, cY, int(aCircleRadius)+i, (255,255,255))
                tempFont = self.cFont.render(str(hitObject[-1]), True, (255,255,255))
                tempSurface.blit(tempFont, (cX-(tempFont.get_width() / 2), cY-(tempFont.get_height()/2)))
            else:
                break
        

        return tempSurface




    def update(self):

        if int(self.hitObjects[0][2]) < self.soundHandler.musicChannel.get_pos():
            self.hitObjects.pop(0)

        
