import BeatmapParse
import pygame
import config
import pygame.gfxdraw
import os
import BeatmapFrame
import AiPlayer

class gsBeatmapPlayer:



    def __init__(self, PATH, parentClass, multi=False):
        print("INITIALIZING BEATMAP")
        self.tempPath = PATH
        # pointer to the parent class
        self.parent = parentClass
        # pointer to the sound handler used for playing music etc
        self.soundHandler = parentClass.soundStream
        #print(PATH)
        # load the data from the beatmap file which will be used to display and run the map
        self.playingBeatmap = PATH
        self.hitObjects = BeatmapParse.fullParse(self.playingBeatmap["osuPath"])

        self.pausedTime = 0
        self.offsetTime = 0
        #print(self.hitObjects)

        self.isMulti = multi
        

        # calculate all necessary values for the map, such as relative circle size, approach rate in ms etc
        self.getMapValues()

        # load and display the background image assigned to the map
        PATH = os.path.join(self.playingBeatmap["BasePath"],self.playingBeatmap["BackgroundImage"])
        PATH = PATH.replace("\\","/")
        bg = pygame.image.load(PATH.strip())
        # transform the image to the size of the screen currently
        self.bgIMG = pygame.transform.scale(bg, config.SCREEN_RESOLUTION)

        # initialize the font used throught the map
        self.cFont = pygame.font.SysFont('Arial', 40)

        # mapping all key presses to their respective functions
        self.KEY_MAP = {"keyOsuLeft":self.hasHitNextNote,
                               "keyOsuRight":self.hasHitNextNote,
                               "keyPause":self.pauseMap}
        self.buttonFunct = [self.pauseMap, self.retry, self.parent.resumeGamestate]

        # holds the value of the current combo held by the player
        self.combo = 0
        # holds the value of the maximum combo achieved by the player
        self.maxCombo = 0
        # holds the value of the number of misses held by the player
        self.missCount = 0
        # holds the value of the current score
        self.score = 0
        
        self.hitTimings = []

        self.isPaused = False

        if self.isMulti:
            self.AI = AiPlayer.ArtificialIntelligence("mrekk", "Fool")
            while not self.AI.isReady:
                continue
        
        # plays the song and begins the beatmap
        self.soundHandler.playSong(self.playingBeatmap["BasePath"]+"/"+self.playingBeatmap["AudioFilename"])

    """ Function called when a successful circle press is registererd"""
    def hitNote(self, score):
        # increment the player's current combo
        self.combo += 1
        # if the current combo is larger than the max combo, update the max combo
        if self.combo > self.maxCombo:
            self.maxCombo = self.combo
        # add to the user's current score the current combo multiplied by the hit score achieved (300, 100, 50)
        self.score += self.combo*score
        self.hitObjects.pop(0)

    """ Function called when a missed note is registered"""
    def missNote(self):
        
        self.missCount += 1
        self.combo = 0
        self.hitObjects.pop(0)

    def getCurrentPos(self):
        return self.soundHandler.musicChannel.get_pos() + self.offsetTime        

    def pauseMap(self):
        cPos = self.getCurrentPos()
        self.isPaused = not self.isPaused
        if self.isPaused:
            self.pausedTime = cPos
            self.soundHandler.pauseSong()
        else:
            self.offsetTime = self.pausedTime
            self.soundHandler.resumeSong(self.pausedTime)


        

    """ Function that calculates all the necessary values used in the playing of the beatmap"""
    def getMapValues(self):

        # calculate the AR timings
        """ If the approach rate is less than 5, the formula to work it out is 800+400*(5-approach rate)/5"""
        if float(self.playingBeatmap["ApproachRate"]) < 5:
            self.fadeInTime = int(800 + 400*((5-float(self.playingBeatmap["ApproachRate"])) / 5))
            BeatmapFrame.fadeInStart = int(1200 + 600*((5-float(self.playingBeatmap["ApproachRate"])) / 5))
        elif float(self.playingBeatmap["ApproachRate"]) == 5:
            """ If the approach rate is 5, the formula is just 800"""
            self.fadeInTime = 800
            BeatmapFrame.fadeInStart = 1200
        elif float(self.playingBeatmap["ApproachRate"]) > 5:
            """ If the approach rate is greater than 5, the formula is 800-500*(appraoch rate - 5) / 5"""
            self.fadeInTime = int(800 - 500*((float(self.playingBeatmap["ApproachRate"])-5)/5))
            BeatmapFrame.fadeInStart = int(1200 - 750*((float(self.playingBeatmap["ApproachRate"])-5)/5))
        # calculate the outer radius of the circle based on the current circle size
        BeatmapFrame.circleSize = int(config.CURRENT_SCALING*(54.4-4.48*float(self.playingBeatmap["CircleSize"])))
        BeatmapFrame.approachCircleSize = BeatmapFrame.circleSize*2

        # calculate the respective windows for scores, using the map's overall difficulty value
        self.hitWindows = [((400-20*float(self.playingBeatmap["OverallDifficulty"]))/2)*10,
                           ((280-16*float(self.playingBeatmap["OverallDifficulty"]))/2)*10,
                           ((160-12*float(self.playingBeatmap["OverallDifficulty"]))/2)*10]
        
        print(self.hitWindows)
        
        self.scoreWindows = [50,100,300]

        # calculate values related to the hit timing display
        self.rectSize = int(config.SCREEN_RESOLUTION[0] / 3)
        self.timingColors = [(255,0,0),(0,255,0),(0,0,255)]
        #print(self.hitWindows)

        self.xOffset = int((config.SCREEN_RESOLUTION[0] - config.DEFAULT_RESOLUTION[0]*config.CURRENT_SCALING)/2)

        #print("X offset: {}".format(self.xOffset))

        # ms before the hit window begins in which a player misses if they try to hit the circle
        self.missMargin = 50
        self.calcButtonBounds()

    def retry(self):

        self.__init__(self.tempPath, self.parent)

    def mButtonUp(self):
        if not self.isPaused:
            return
        mX, mY = pygame.mouse.get_pos()
        if mX >= self.buttonBounds[0][0] and mX <= self.buttonBounds[0][2] + self.buttonBounds[0][0]:

            funct = 0
            for button in self.buttonBounds:
                if mY >= button[1] and mY <= button[1] + button[3]:
                    self.buttonFunct[funct]()
                    break
                funct += 1

    def calcButtonBounds(self):

        height = int(config.SCREEN_RESOLUTION[1] / 6)
        width = int(config.SCREEN_RESOLUTION[0] / 3)
        yVal = int((config.SCREEN_RESOLUTION[0] - width) / 2)
        margin = int(height / 2)
        self.buttonBounds = [(yVal, height+(height+margin)*i, width, height) for i in range(3)]

    def drawFollowPoints(self, surface):

        followPointIndex = 0
        cTimePos = self.getCurrentPos()
        for i in range(len(self.hitObjects)):
            if i == 0:
                continue
            pObject = self.hitObjects[i-1]
            cObject = self.hitObjects[i]
            if cTimePos + self.fadeInStart >= pObject[2]:

                
                cPos = (cObject[0]+self.xOffset, cObject[1])
                cTime = cObject[2]
                pPos = (pObject[0]+self.xOffset, pObject[1])
                pygame.draw.aaline(surface, (255,255,255), cPos, pPos)
                #pTime = 
            else:
                break

            

        


    def getRenderSnapshot(self, interpolation):

        
        tempSurface = pygame.Surface(config.SCREEN_RESOLUTION)
        #tempSurface.fill((0,0,0))
        tempSurface.blit(self.bgIMG, (0,0))
        
        #tempSurface.fill((0,0,0))
        

        

        combo = 0
        for hitObject in self.hitObjects:
            combo += 1
            cPos = self.getCurrentPos()
            if cPos+BeatmapFrame.fadeInStart >= hitObject.timingPoint:
                hitObject.render(cPos, tempSurface)



            else:
                break
        if self.isMulti:
            aiPos = self.AI.getCursorPos(self.getCurrentPos())
            #print(self.getCurrentPos())
            pygame.gfxdraw.filled_circle(tempSurface, aiPos[0], aiPos[1], 20, (0,255,0))
        #self.drawFollowPoints(tempSurface)
        self.drawInfoUI(tempSurface)
        if self.isPaused:
            self.drawPauseMenu(tempSurface)
        else:
            self.drawUnstableRateMarker(tempSurface)
        

        return tempSurface
    
    def drawInfoUI(self ,surface):
        comboText = self.cFont.render("{}x".format(self.combo), True, (255,255,255))
        comboMargin = int(config.SCREEN_RESOLUTION[0]*(1/20))
        surface.blit(comboText, (comboMargin, config.SCREEN_RESOLUTION[1] - comboMargin))


    
    def drawUnstableRateMarker(self, surface):

        for i in range(0,3):
            tempSize = self.hitWindows[i]/2
            pygame.draw.rect(surface, self.timingColors[i], (int((config.SCREEN_RESOLUTION[0] - tempSize)/2),1000,tempSize, 20))
        
        for hitMark in self.hitTimings:
            pygame.draw.rect(surface, (255,255,255), (int(config.SCREEN_RESOLUTION[0]/2)+hitMark/2, 950, 2, 100))
    
    def drawPauseMenu(self, surface):

        for button in self.buttonBounds:
            pygame.draw.rect(surface, config.PINK, button)

    def checkCircle(self):

        mX, mY = pygame.mouse.get_pos()

        dX = abs(mX - (self.hitObjects[0].x))
        dY = abs(mY - self.hitObjects[0].y)
        #print("Evaluating mouse press {},{} with circle {},{}".format(mX, mY, self.hitObjects[0][0], self.hitObjects[0][1]))

        if dX > self.radius or dY > self.radius:
            return False

        if dX + dY <= self.radius:
            return True

        if dX**2 + dY**2 <= self.radius**2:
            return True
        else:
            return False

    def hasHitNextNote(self):

        """ For the note to have been hit, the user must have had both the cursor over the circle, and must have pressed the z or x button
        within the required timing points."""

        # if the user's mouse was not over the circle, no action should be taken
        if not self.checkCircle():
            return

        score = self.checkTimingPoints()
        # if the user's hit was not within any timing points, ignore it
        if score == None:
            return
        elif score == 0:
            self.missNote()
        else:
            self.hitNote(score)
        

        

    def checkTimingPoints(self):


        # get the current position in ms 
        cPos = self.getCurrentPos()

        #print("Checking Timing Points")

        # calculate the difference between the current position and the timing point
        cDiff = cPos - self.hitObjects[0].timingPoint
        self.hitTimings.append(cDiff)

        # if the mouse overlaps with the circle but the timing is within the miss timing point, return 0
        # if abs(cDiff) >= self.hitWindows[0] and abs(cDiff) <= self.hitWindows[0]+self.missMargin:
        #     return 0
        # if the differenece is greater than the miss window, ignore
        if abs(cDiff) > self.hitWindows[0] + self.missMargin:
            return None

        # work out which score value to assign to the player
        scoresHit = []
        for i in range(len(self.hitWindows)):
            if abs(cDiff) < self.hitWindows[i]:
                scoresHit.append(self.scoreWindows[i])
            
        return max(scoresHit)
                
            


    def update(self):
        try:
            if self.hitObjects[0].timingPoint < self.getCurrentPos():
                self.missNote()
        except IndexError:
            pass
        
        if not self.soundHandler.musicChannel.get_busy() and not self.isPaused:
            self.parent.resumeGamestate()

        
