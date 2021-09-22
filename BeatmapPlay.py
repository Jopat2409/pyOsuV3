import BeatmapParse
import pygame
import config
import pygame.gfxdraw
import os


class gsBeatmapPlayer:



    def __init__(self, PATH, parentClass):

        # pointer to the parent class
        self.parent = parentClass
        # pointer to the sound handler used for playing music etc
        self.soundHandler = parentClass.soundStream
        #print(PATH)
        # load the data from the beatmap file which will be used to display and run the map
        self.playingBeatmap = PATH
        self.hitObjects = BeatmapParse.fullParse(self.playingBeatmap["osuPath"])
        #print(self.hitObjects)

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
                               "keyOsuRight":self.hasHitNextNote}

        # holds the value of the current combo held by the player
        self.combo = 0
        # holds the value of the maximum combo achieved by the player
        self.maxCombo = 0
        # holds the value of the number of misses held by the player
        self.missCount = 0
        # holds the value of the current score
        self.score = 0
        
        self.hitTimings = []

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
        

        

        

    """ Function that calculates all the necessary values used in the playing of the beatmap"""
    def getMapValues(self):

        # calculate the AR timings
        """ If the approach rate is less than 5, the formula to work it out is 800+400*(5-approach rate)/5"""
        if float(self.playingBeatmap["ApproachRate"]) < 5:
            self.fadeInTime = int(800 + 400*((5-float(self.playingBeatmap["ApproachRate"])) / 5))
            self.fadeInStart = int(1200 + 600*((5-float(self.playingBeatmap["ApproachRate"])) / 5))
        elif float(self.playingBeatmap["ApproachRate"]) == 5:
            """ If the approach rate is 5, the formula is just 800"""
            self.fadeInTime = 800
            self.fadeInStart = 1200
        elif float(self.playingBeatmap["ApproachRate"]) > 5:
            """ If the approach rate is greater than 5, the formula is 800-500*(appraoch rate - 5) / 5"""
            self.fadeInTime = int(800 - 500*((float(self.playingBeatmap["ApproachRate"])-5)/5))
            self.fadeInStart = int(1200 - 750*((float(self.playingBeatmap["ApproachRate"])-5)/5))
        # calculate the outer radius of the circle based on the current circle size
        self.radius = int(config.CURRENT_SCALING*(54.4-4.48*float(self.playingBeatmap["CircleSize"])))
        self.innerRadius = int(self.radius*0.9)
        self.hCircleRadius = self.radius*2

        # calculate the respective windows for scores, using the map's overall difficulty value
        self.hitWindows = [((400-20*float(self.playingBeatmap["OverallDifficulty"]))/2)+250,
                           ((280-16*float(self.playingBeatmap["OverallDifficulty"]))/2)+250,
                           ((160-12*float(self.playingBeatmap["OverallDifficulty"]))/2)+250]
        
        self.scoreWindows = [50,100,300]

        # calculate values related to the hit timing display
        self.rectSize = int(config.SCREEN_RESOLUTION[0] / 3)
        self.timingColors = [(255,0,0),(0,255,0),(0,0,255)]
        #print(self.hitWindows)

        self.xOffset = int((config.SCREEN_RESOLUTION[0] - config.DEFAULT_RESOLUTION[0]*config.CURRENT_SCALING)/2)

        #print("X offset: {}".format(self.xOffset))

        # ms before the hit window begins in which a player misses if they try to hit the circle
        self.missMargin = 50


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
                if aCircleRadius > self.radius:
                   for i in range(0,5):
                       pygame.gfxdraw.aacircle(tempSurface, cX, cY, aCircleRadius+i, (255,255,255))
                tempFont = self.cFont.render(str(hitObject[-1]), True, (255,255,255))
                tempSurface.blit(tempFont, (cX-(tempFont.get_width() / 2), cY-(tempFont.get_height()/2)))
            else:
                break
        comboText = self.cFont.render("{}x".format(self.combo), True, (255,255,255))
        tempSurface.blit(comboText, (100,100))
        self.drawUnstableRateMarker(tempSurface)
        

        return tempSurface
    
    def drawUnstableRateMarker(self, surface):

        for i in range(0,3):
            tempSize = self.hitWindows[i]*2
            pygame.draw.rect(surface, self.timingColors[i], (int((config.SCREEN_RESOLUTION[0] - tempSize)/2),1000,tempSize, 30))
        
        for hitMark in self.hitTimings:
            pygame.draw.rect(surface, (255,255,255), (int(config.SCREEN_RESOLUTION[0]/2)+hitMark*2, 950, 5, 100))

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
        cPos = self.soundHandler.musicChannel.get_pos()

        #print("Checking Timing Points")

        # calculate the difference between the current position and the timing point
        cDiff = cPos - self.hitObjects[0][2]

        # if the mouse overlaps with the circle but the timing is within the miss timing point, return 0
        if abs(cDiff) >= self.hitWindows[0] and abs(cDiff) <= self.hitWindows[0]+self.missMargin:
            return 0
        # if the differenece is greater than the miss window, ignore
        elif abs(cDiff) > self.hitWindows[0] + self.missMargin:
            return None

        # work out which score value to assign to the player
        scoresHit = []
        for i in range(len(self.hitWindows)):
            if abs(cDiff) < self.hitWindows[i]:
                scoresHit.append(self.scoreWindows[i])
            
        return max(scoresHit)
                
            


    def update(self):

        if int(self.hitObjects[0][2]) < self.soundHandler.musicChannel.get_pos():
            self.missNote()

        
