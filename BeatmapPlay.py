""" ---------- OSU MODULES ---------- """
import config
import BeatmapParse
import BeatmapFrame
import AiPlayer

""" ---------- PYTHON MODULES ---------- """
import pygame
import pygame.gfxdraw
import os


class gsBeatmapPlayer:
    """
    Encapsulates all the data and functions needed to play a beatmap
    PATH: path to the beatmap
    parentClass: callback to the parent class
    multi: wether multiplayer is enabled
    """

    def __init__(self, PATH, parentClass, multi=False):
        """ ------ TIMING VARIABLES ------- """
        self.fadeInStart = None
        self.buttonBounds = None
        self.missMargin = None
        self.xOffset = None
        self.timingColors = None
        self.rectSize = None
        self.scoreWindows = None
        self.hitWindows = None
        self.fadeInTime = None
        """ ---------------------------      """
        # create the temporary path
        self.tempPath = PATH

        # pointer to the parent class
        self.parent = parentClass
        # pointer to the sound handler used for playing music etc
        self.soundHandler = parentClass.soundStream
        # load the data from the beatmap file which will be used to display and run the map
        self.playingBeatmap = PATH

        # parse the full beatmap
        self.hitObjects = BeatmapParse.fullParse(self.playingBeatmap["osuPath"])

        self.pausedTime = 0  # time the game was paused
        self.offsetTime = 0  # cumulative offset time (caused by pauses)
        self.isMulti = multi  # isMultiplayer
        # initialize the font used throught the map
        self.cFont = pygame.font.SysFont('Arial', 40)
        # mapping all key presses to their respective functions
        self.KEY_MAP = {"keyOsuLeft": self.hasHitNextNote,
                        "keyOsuRight": self.hasHitNextNote,
                        "keyPause": self.pauseMap}
        # mapping the buttons to their respective button functions
        self.buttonFunct = [self.pauseMap, self.retry, self.parent.resumeGamestate]
        # holds the value of the current combo held by the player
        self.combo = 0
        # holds the value of the maximum combo achieved by the player
        self.maxCombo = 0
        # holds the value of the number of misses held by the player
        self.missCount = 0
        # holds the value of the current score
        self.score = 0

        # create the hit-timing array
        self.hitTimings = []
        # holds wether or not the map is paused
        self.isPaused = False
        self.getMapValues()  # Calculate all necessary map values

        # load and display the background image assigned to the map
        PATH = os.path.join(self.playingBeatmap["BasePath"], self.playingBeatmap["BackgroundImage"])
        PATH = PATH.replace("\\", "/")
        bg = pygame.image.load(PATH.strip()).convert()
        # transform the image to the size of the screen currently
        self.bgIMG = pygame.transform.scale(bg, config.SCREEN_RESOLUTION)

        # if multiplayer is enabled
        if self.isMulti:
            # initialize the AI player
            self.AI = AiPlayer.ArtificialIntelligence("mrekk", "Fool")
            # waits for the AI to be ready before proceeding
            while not self.AI.isReady:
                continue

        # plays the song and begins the beatmap
        self.soundHandler.playSong(self.playingBeatmap["BasePath"] + "/" + self.playingBeatmap["AudioFilename"])

    def hitNote(self, score):
        """
        Function called when a successful circle press is registererd
        """
        # increment the player's current combo
        self.combo += 1
        # if the current combo is larger than the max combo, update the max combo
        if self.combo > self.maxCombo:
            self.maxCombo = self.combo
        # add to the user's current score the current combo multiplied by the hit score achieved (300, 100, 50)
        self.score += self.combo * score
        self.hitObjects.pop(0)

    def missNote(self):
        """
        Function called when a missed note is registered
        """
        # increment the miss count
        self.missCount += 1
        # reset the player combo
        self.combo = 0
        # remove the current hit object that was missed
        self.hitObjects.pop(0)

    def getCurrentPos(self):
        """
        Get the current position of the music channel
        """
        # get the inbuilt position, plus any offset incurred by pauses
        return self.soundHandler.musicChannel.get_pos() + self.offsetTime

    def pauseMap(self):
        """
        Pause or resume the beatmap
        """
        # get a reference to the current position
        cPos = self.getCurrentPos()
        # switch self.isPaused
        self.isPaused = not self.isPaused
        # if the map has been paused
        if self.isPaused:
            # store the time that the map was paused at 
            self.pausedTime = cPos
            # pause the song
            self.soundHandler.pauseSong()
        else:
            # set the offset time
            self.offsetTime = self.pausedTime
            # resume the song at the paused time
            self.soundHandler.resumeSong(self.pausedTime)

    def getMapValues(self):
        """
        Function that calculates all the necessary values used in the playing of the beatmap
        """
        # calculate the AR timings
        """ If the approach rate is less than 5, the formula to work it out is 800+400*(5-approach rate)/5"""
        if float(self.playingBeatmap["ApproachRate"]) < 5:
            self.fadeInTime = int(800 + 400 * ((5 - float(self.playingBeatmap["ApproachRate"])) / 5))
            BeatmapFrame.fadeInStart = int(1200 + 600 * ((5 - float(self.playingBeatmap["ApproachRate"])) / 5))
        elif float(self.playingBeatmap["ApproachRate"]) == 5:
            """ If the approach rate is 5, the formula is just 800"""
            self.fadeInTime = 800
            BeatmapFrame.fadeInStart = 1200
        elif float(self.playingBeatmap["ApproachRate"]) > 5:
            """ If the approach rate is greater than 5, the formula is 800-500*(appraoch rate - 5) / 5"""
            self.fadeInTime = int(800 - 500 * ((float(self.playingBeatmap["ApproachRate"]) - 5) / 5))
            BeatmapFrame.fadeInStart = int(1200 - 750 * ((float(self.playingBeatmap["ApproachRate"]) - 5) / 5))

        # calculate the outer radius of the circle based on the current circle size
        BeatmapFrame.circleSize = int(config.CURRENT_SCALING * (54.4 - 4.48 * float(self.playingBeatmap["CircleSize"])))
        BeatmapFrame.approachCircleSize = BeatmapFrame.circleSize * 2

        # calculate the respective windows for scores, using the map's overall difficulty value
        self.hitWindows = [((400 - 20 * float(self.playingBeatmap["OverallDifficulty"])) / 2) * 10,
                           ((280 - 16 * float(self.playingBeatmap["OverallDifficulty"])) / 2) * 10,
                           ((160 - 12 * float(self.playingBeatmap["OverallDifficulty"])) / 2) * 10]

        # storing the scores for the respective hit windows
        self.scoreWindows = [50, 100, 300]

        # calculate values related to the hit timing display
        self.rectSize = int(config.SCREEN_RESOLUTION[0] / 3)
        self.timingColors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

        # calculate the x offset used
        self.xOffset = int((config.SCREEN_RESOLUTION[0] - config.DEFAULT_RESOLUTION[0] * config.CURRENT_SCALING) / 2)
        # ms before the hit window begins in which a player misses if they try to hit the circle
        self.missMargin = 50
        self.calcButtonBounds()

    def retry(self):
        """
        Called when a user wants to retry the beatmap
        """
        # re-initializes the own class
        self.__init__(self.tempPath, self.parent)

    def mButtonUp(self):
        """
         Function called when mouse button is lifted
        """
        # do nothing if game is not paused (as mouse button input is ignored while playing)
        if not self.isPaused:
            return
        # unpack the current mouse position
        mX, mY = pygame.mouse.get_pos()
        # if mx is within the paused button bounds
        if self.buttonBounds[0][0] <= mX <= self.buttonBounds[0][2] + self.buttonBounds[0][0]:
            # counter for runnin the correct function
            funct = 0
            # loop through button bounds
            for button in self.buttonBounds:
                # if mouse y position is within the current button bounds
                if button[1] <= mY <= button[1] + button[3]:
                    # execute the function at funct
                    self.buttonFunct[funct]()
                    break
                # increment funct
                funct += 1

    def calcButtonBounds(self):
        """
        calculate the bounds for pause buttons
        """
        # work out the height
        height = int(config.SCREEN_RESOLUTION[1] / 6)
        # work out the width
        width = int(config.SCREEN_RESOLUTION[0] / 3)
        # work out the y coordinate
        yVal = int((config.SCREEN_RESOLUTION[0] - width) / 2)
        # work out the distance between buttons
        margin = int(height / 2)
        # update button bounds
        self.buttonBounds = [(yVal, height + (height + margin) * i, width, height) for i in range(3)]

    def getRenderSnapshot(self, interpolation, tempSurface):
        """
        Render the gamestate
        """

        # fill the surface with black
        # tempSurface.fill((0,0,0))
        tempSurface.blit(self.bgIMG, (0, 0))
        # initialize the combo
        combo = 0
        # get the current song position
        cPos = self.getCurrentPos()
        for hitObject in self.hitObjects:
            combo += 1
            # if the current position is within the fade in timeframe of the hit object
            if cPos + BeatmapFrame.fadeInStart >= hitObject.timingPoint:
                # render the hit object
                hitObject.render(cPos, tempSurface)
            else:
                # since the hit objects are stored linearly, break after an exception
                break
        # if multiplayer is enabled
        if self.isMulti:
            # get the current position of the AI cursor
            aiPos = self.AI.getCursorPos(cPos)
            # render the AI cursor
            pygame.gfxdraw.filled_circle(tempSurface, aiPos[0], aiPos[1], 20, (0, 255, 0))
        # draw the information (percentage, combo etc)
        self.drawInfoUI(tempSurface)
        # if game is paused then draw the paused menu
        if self.isPaused:
            self.drawPauseMenu(tempSurface)
        # else draw the unstable rate marker
        else:
            self.drawUnstableRateMarker(tempSurface)



    def drawInfoUI(self, surface):
        """
        Draw the combo, percentage ETC
        surface: surface to be drawn to
        """
        # render the current user combo
        comboText = self.cFont.render("{}x".format(self.combo), True, (255, 255, 255))
        # work out the margin of the combo
        comboMargin = int(config.SCREEN_RESOLUTION[0] * (1 / 20))
        # blit the combo onto the main screen
        surface.blit(comboText, (comboMargin, config.SCREEN_RESOLUTION[1] - comboMargin))



    def drawUnstableRateMarker(self, surface):
        """
        Draw the unstable rate indicator
        surface: surface to be drawn to
        """
        for i in range(0, 3):
            # work out the relative size of the window
            tempSize = self.hitWindows[i] / 2
            # draw the hit window rectangle
            pygame.draw.rect(surface, self.timingColors[i], (
                int((config.SCREEN_RESOLUTION[0] - tempSize) / 2), config.SCREEN_RESOLUTION[1] - 50, tempSize, 20))
        # loop through recent timing differences
        for hitMark in self.hitTimings:
            # draw an indicator where it falls on the scale
            pygame.draw.rect(surface, (255, 255, 255), (
                int(config.SCREEN_RESOLUTION[0] / 2) + hitMark / 2, config.SCREEN_RESOLUTION[1] - 90, 2, 100))

    def drawPauseMenu(self, surface):
        """
        Draws the paused menu
        surface: surface to be drawn onto
        """
        # blit the pause overlay image onto the screen
        pass

    def checkCircle(self):
        """
        Check if the mouse is within the current hitcircle
        """
        # unpack the mouse position
        mX, mY = pygame.mouse.get_pos()

        dX = abs(mX - self.hitObjects[0].x)
        dY = abs(mY - self.hitObjects[0].y)

        # if dx or dy are out of the beatmap circle size
        if dX > BeatmapFrame.circleSize or dY > BeatmapFrame.circleSize:
            # the circle has not been hit
            return False
        # if dx + dY is less than circle size
        if dX + dY <= BeatmapFrame.circleSize:
            # the circle has been hit
            return True

        # as a last resort, use the equation of the circle to absolutely check the bounds
        if dX ** 2 + dY ** 2 <= BeatmapFrame.circleSize ** 2:
            return True
        else:
            return False

    def hasHitNextNote(self):
        """
        Check if the user has sucessfully hit the next circle
        """
        # if the user's mouse was not over the circle, no action should be taken
        if not self.checkCircle():
            return

        # get the score to award the user based on the error interval
        score = self.checkTimingPoints()
        # if the user's hit was not within any timing points, ignore it
        if score is None:
            return
        # if user pressed within the miss hit window, miss note
        elif score == 0:
            self.missNote()
        # else hit the note with the score
        else:
            self.hitNote(score)

    def checkTimingPoints(self):
        """
        Check wether the user hit the note within a designated timing point
        """

        # get the current position in ms
        cPos = self.getCurrentPos()

        # print("Checking Timing Points")

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
        """
        Update the gamestate
        """
        try:
            # if the first hit object has alreayd passed
            if self.hitObjects[0].timingPoint < self.getCurrentPos():
                # miss the note
                self.missNote()
                # play hitsound (debug purposes)
                self.soundHandler.playEffect("hitSound")
        except IndexError:
            pass
        # IDK why this is here?
        if not self.soundHandler.musicChannel.get_busy() and not self.isPaused:
            self.parent.resumeGamestate()
