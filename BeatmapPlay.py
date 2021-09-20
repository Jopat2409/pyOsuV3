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

        PATH = os.path.join(self.playingBeatmap["BasePath"],self.playingBeatmap["BackgroundImage"])
        PATH = PATH.replace("\\","/")
        bg = pygame.image.load(PATH.strip())
        self.bgIMG = pygame.transform.scale(bg, config.SCREEN_RESOLUTION)

        self.cFont = pygame.font.SysFont('Arial', 40)

        self.KEY_MAP = {"keyOsuLeft":self.checkTimingPoints,
                               "keyOsuRight":self.checkTimingPoints}

        self.combo = 0
        self.maxCombo = 0
        self.missCount = 0
        self.score = 0

        self.soundHandler.playSong(self.playingBeatmap["BasePath"]+"/"+self.playingBeatmap["AudioFilename"])


    def hitNote(self, score):

        self.combo += 1
        if self.combo > self.maxCombo:
            self.maxCombo = self.combo

        self.score += self.combo*score

    def missNote(self):
        
        self.missCount += 1
        self.combo = 0
        

        

        


    def getMapValues(self):

        # calculate the AR timings
        if float(self.playingBeatmap["ApproachRate"]) < 5:
            self.fadeInTime = int(800 + 400*((5-float(self.playingBeatmap["ApproachRate"])) / 5))
            self.fadeInStart = int(1200 + 600*((5-float(self.playingBeatmap["ApproachRate"])) / 5))
        elif float(self.playingBeatmap["ApproachRate"]) == 5:
            self.fadeInTime = 800
            self.fadeInStart = 1200
        elif float(self.playingBeatmap["ApproachRate"]) > 5:
            self.fadeInTime = int(800 - 500*((float(self.playingBeatmap["ApproachRate"])-5)/5))
            self.fadeInStart = int(1200 - 750*((float(self.playingBeatmap["ApproachRate"])-5)/5))

        self.radius = int(config.CURRENT_SCALING*(54.4-4.48*float(self.playingBeatmap["CircleSize"])))
        self.innerRadius = int(self.radius*0.9)
        self.hCircleRadius = self.radius*2

        self.hitWindows = [(400-20*float(self.playingBeatmap["OverallDifficulty"]))/2,
                           (280-16*float(self.playingBeatmap["OverallDifficulty"]))/2,
                           (160-12*float(self.playingBeatmap["OverallDifficulty"]))/2]

        self.scoreWindows = [50,100,300]
        print(self.hitWindows)

        self.xOffset = int((config.SCREEN_RESOLUTION[0] - config.DEFAULT_RESOLUTION[0]*config.CURRENT_SCALING)/2)

        print("X offset: {}".format(self.xOffset))


    def drawFollowPoints(self):

        followPointIndex = 0
        for i in range(self.hitObjects):
            cObject = self.hitObjects[i]
            cPos = (cObject[0], cObject[1])
            cTime = cObject[2]
            pPos = (self.hitObjects[i-1][0], self.hitObjects[i-1][1])
            #pTime = 

            

        


    def getRenderSnapshot(self, interpolation):

        tempSurface = pygame.Surface(config.SCREEN_RESOLUTION)
        tempSurface.blit(self.bgIMG, (0,0))
        tempSurface.fill((0,0,0))
        

        

        combo = 0
        for hitObject in self.hitObjects:
            combo += 1
            cPos = self.soundHandler.musicChannel.get_pos()
            if cPos+self.fadeInStart >= hitObject[2]:
                alpha =  255 / self.fadeInTime * (cPos - (hitObject[2] - self.fadeInStart))
                if alpha >= 255:
                    alpha = 255

                aCircleRadius = int(self.radius + self.hCircleRadius * ((hitObject[2]-cPos) / self.fadeInStart))
                cX = self.xOffset + hitObject[0]
                cY = hitObject[1]

                
              
                pygame.gfxdraw.filled_circle(tempSurface, cX, cY, self.radius, (255,255,255))
                pygame.gfxdraw.filled_circle(tempSurface, cX, cY, self.innerRadius, (0,0,0))
##                if aCircleRadius > self.radius:
##                    for i in range(0,5):
##                        pygame.gfxdraw.aacircle(tempSurface, cX, cY, aCircleRadius+i, (255,255,255))
                tempFont = self.cFont.render(str(hitObject[-1]), True, (255,255,255))
                tempSurface.blit(tempFont, (cX-(tempFont.get_width() / 2), cY-(tempFont.get_height()/2)))
            else:
                break
        comboText = self.cFont.render("{}x".format(self.combo), True, (255,255,255))
        tempSurface.blit(comboText, (100,100))
        

        return tempSurface

    def checkCircle(self):

        mX, mY = pygame.mouse.get_pos()

        dX = abs(mX - (self.hitObjects[0][0]+self.xOffset))
        dY = abs(mY - self.hitObjects[0][1])
        #print("Evaluating mouse press {},{} with circle {},{}".format(mX, mY, self.hitObjects[0][0], self.hitObjects[0][1]))

        if dX > self.radius or dY > self.radius:
            return False

        if dX + dY <= self.radius:
            return True

        if dX**2 + dY**2 <= self.radius**2:
            return True
        else:
            return False

        

    def checkTimingPoints(self):



        cPos = self.soundHandler.musicChannel.get_pos()

        #print("Checking Timing Points")

        cDiff = cPos - self.hitObjects[0][2]

        scoresHit = []
        for i in range(len(self.hitWindows)):
            if abs(cDiff) < self.hitWindows[i]:
                scoresHit.append(self.scoreWindows[i])
            

        if len(scoresHit) == 0:
            pass
        else:
            if self.checkCircle():
                self.hitNote(max(scoresHit))
                #print("hit note {}".format(max(scoresHit)))
            else:
                self.missNote()

            self.hitObjects.pop(0)
                
            


    def update(self):

        if int(self.hitObjects[0][2])+self.hitWindows[0] < self.soundHandler.musicChannel.get_pos():
            self.hitObjects.pop(0)
            self.missNote()

        
