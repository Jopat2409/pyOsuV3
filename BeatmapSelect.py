""" ---------- OSU MODULES ---------- """
import config  # for program-global variables
import BeatmapParse  # for parsing beatmaps
import BeatmapPlay  # for playing beatmaps
""" ---------- PYTHON MODULES ---------- """
import pickle  # for serializing beatmaps
import os  # for joining paths
import glob  # for traversing beatmap directory
import pygame  # for rendering
import math  # for rounding
import time  # for syncing beatmap and audio
import checksumdir  # for getting hash of beatmap files
import MainMenu

"""
Encapsulates the functions of the beatmap selection gamestate
"""


class gsBeatmapSelect:

    def __init__(self, parentClass):

        # gets a reference to the parent class
        self.bmMargin = None
        self.bmWidth = None
        self.bmHeight = None
        self.bmOffset = None
        self.prevMousePos = None
        self.parentClass = parentClass

        # store a pointer to the sound handler
        self.soundHandler = parentClass.soundStream
        # array of beatmaps
        self.beatmaps = []
        # initializes the bounds array of the beatmap
        self.beatmapBounds = []

        # load the background intoa pygame
        bg = pygame.image.load(
            config.DEFAULT_PATH + '/assets/bg/online_background_68261587a4e3fbe77cad07120ee1e864.jpg')
        # scale it to the size of the screen
        self.bgIMG = pygame.transform.scale(bg, config.SCREEN_RESOLUTION)

        # hard coded integers to do with movement of beatmap container
        self.offset = 0  # current offset of the beatmap array
        self.scrolling = False  # wether or not the user is scrolling
        self.decelerating = False  # used for smooth scrolling
        self.velTotal = 0  # used for smooth scrolling
        self.velCount = 0  # used for smooth scrolling
        self.velY = 0  # current velocity of the beatmap container
        self.prevMY = 0  # previous mouse y position
        self.decel = 1  # current deceleration
        self.decelCount = 0  # used for smooth scrolling
        self.maxMouseMovement = 5  # how much mouse input is considerd when decelerating

        self.KEY_MAP = {"keyPause": self.goBack}

        # initialize the default font
        self.font = pygame.font.SysFont('Arial', 25)
        # create the frame that holds the beatmap selection buttons
        self.beatmapFrame = pygame.Surface((config.SCREEN_RESOLUTION[0] / 3, config.SCREEN_RESOLUTION[1]),
                                           pygame.SRCALPHA, 32).convert_alpha()

        # initialize the timer for timing how long it takes to load beatmaps
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
        # calculate the bounds of all the buttons / beatmap selection buttons
        self.calculateBmBounds()
        # output the time taken to load the beatmaps (DEBUG)
        print("It took {}s to load all beatmaps".format(time.time() - bmLoadStart))

        # points to the current index of the beatmap currently selected
        self.cBeatmap = -1


    def goBack(self):
        """
        Transfers the state back to the main menu
        :return:
        """
        self.parentClass.newGamestate(MainMenu.gsMenu(self.parentClass))



    def DrawInfoPanel(self, surface):
        pygame.draw.rect(surface, (255, 255, 255),
                         (0, 0, config.SCREEN_RESOLUTION[0] / 3, config.SCREEN_RESOLUTION[1] / 3))
        tempString = "{} [{}]".format(self.beatmaps[self.cBeatmap]["Title"], self.beatmaps[self.cBeatmap]["Version"])
        # blit the text onto the rectangle
        surface.blit(self.font.render(tempString, True, (0, 0, 0)), (0, 0))

    def mButtonDown(self):
        """
        Called when the mouse button is pressed down
        """
        # get the current mouse position
        self.prevMousePos = pygame.mouse.get_pos()
        # unpack the tuple
        mX, mY = self.prevMousePos
        # if the x position is within the bounds of the beatmap bounding box
        if (mX > (config.SCREEN_RESOLUTION[0] / 3) * 2) and mX < config.SCREEN_RESOLUTION[0]:
            # scrolling true
            self.scrolling = True
            # set the previous mouse position
            self.prevMY = pygame.mouse.get_pos()[1]

    def calculateBmBounds(self):
        """
        Calculates the bounds of the buttons
        TODO should be changed when I create the UI system
        """

        self.bmOffset = math.ceil(config.SCREEN_RESOLUTION[0] / 60)  # get the y offset of beatmaps
        self.bmHeight = math.ceil(config.SCREEN_RESOLUTION[1] / 10)  # get the height of the beatmap
        self.bmWidth = config.SCREEN_RESOLUTION[0] / 3 + self.bmOffset  # get the width of the beatmap
        self.bmMargin = math.ceil(self.bmHeight / 10)  # get the margin of the beatmap

        # loops through all the beatmaps
        for drawCount, beatmap in enumerate(self.beatmaps):
            # calculates the bounds and appends them to the bounds array
            self.beatmapBounds.append(
                (0, (self.bmMargin * (drawCount + 1) + self.bmHeight * drawCount), self.bmWidth, self.bmHeight))

    def mButtonUp(self):
        """
        Runs when the mouse button is raised
        """
        # if the user is currently scrolling
        if self.scrolling:
            # unpack the mouse position
            tempX, tempY = pygame.mouse.get_pos()
            # IDK what this does, but it works (it doesn't)
            mDiff = abs((tempX - self.prevMousePos[0]) ^ 2 + (tempY - self.prevMousePos[1]) ^ 2)
            # if the difference in position is less that the minimum required (prevents accidentally scrolling rather
            # than clicking)
            if mDiff <= self.maxMouseMovement ^ 2:
                self.scrolling = False
                self.decelerating = False
                self.velY = 0

                # get the beatmap selected
                self.getBeatmap(tempY)
                return
            # else stop scrolling, but do start decelerating
            self.scrolling = False
            self.decelerating = True
            try:
                # slowly lower the velY
                self.velY = math.ceil(self.velTotal / self.velCount)
            except ZeroDivisionError:
                # in the case that self.velCount is 0, simply skip
                pass



    def getBeatmap(self, mY):
        """
        Ran when the user selects a beatmap
        mY: y position of the mouse when the beatmap was selected
        """
        # keep counter on how many beatmaps we have parsed
        bmCount = 0

        for beatmap in self.beatmapBounds:
            # get the y position of the beatmap
            bmOffset = beatmap[1] + self.offset
            # if the mouse y position intersects
            if bmOffset <= mY <= (bmOffset + self.bmHeight):
                # if this beatmap is already selected
                if self.cBeatmap == bmCount:
                    # pause the gamestate with a new beatmapPlay gamestate we pause here as the information currently
                    # in the class needs to be respored once the song has finished
                    self.parentClass.pauseGamestate(
                        BeatmapPlay.gsBeatmapPlayer(self.beatmaps[self.cBeatmap], self.parentClass, False))
                else:
                    # set the current beatmap to the beatmap
                    self.cBeatmap = bmCount
                    # preview the song the beatmap corresponds to 
                    self.soundHandler.previewSong(
                        self.beatmaps[bmCount]["BasePath"] + "/" + self.beatmaps[bmCount]["AudioFilename"],
                        int(self.beatmaps[bmCount]["PreviewTime"]))
                    # create the path to the background image
                    PATH = os.path.join(self.beatmaps[bmCount]["BasePath"], self.beatmaps[bmCount]["BackgroundImage"])
                    # Fix issues with permissions
                    PATH = PATH.replace("\\", "/")
                    # load the image
                    bg = pygame.image.load(PATH.strip())
                    # blit it onto the background after scaling to screen size
                    self.bgIMG = pygame.transform.scale(bg, config.SCREEN_RESOLUTION)
                return
            # increment the beatmap counter
            bmCount += 1

    def update(self):
        """
        Updates the gamestate
        """
        # if currently scrolling
        if self.scrolling:
            # set the current velocity to the difference between the current mouse position and the last mouse position
            self.velY = pygame.mouse.get_pos()[1] - self.prevMY
            # if the velocity is not 0
            if self.velY != 0:
                # incrememnt the velocity counter (used for averaging velocity for deceleration)
                self.velCount += 1
                # increate the veltotal by the velocity (used for the same purpose)
                self.velTotal += self.velY
            # increment the current render offset of the beatmap container by the velocity
            self.offset += self.velY
            # set the previous mouse y position to the current one
            self.prevMY = pygame.mouse.get_pos()[1]
        elif self.decelerating:
            # increase the offset by the velocity
            self.offset += self.velY
            # if still greater than 0
            if self.velY > 0:
                # decrement the velocity by the deceleration
                self.velY -= self.decel
                # if the velocity has come to a rest, stop decelerating
                if self.velY <= 0:
                    self.decelerating = False

    def drawBeatmapRects(self, surface):
        """
        Render the beatmap rectangles
        surface: surface for the beatmap bounding surface to be blitted to
        TODO need to update this method in prototype 2
        """
        for bmNumber, beatmap in enumerate(self.beatmapBounds):
            # increment the beatmap index
            # break out of for loop once all on screen beatmaps have been drawn
            if beatmap[1] + self.offset > config.SCREEN_RESOLUTION[1]:
                break
            # skip beatmap if it is off the top of the screen
            if beatmap[1] + self.offset + self.bmHeight < 0:
                continue
            # create the rectangle that will be drawn
            rectX = self.bmMargin

            # the current beatmap will have a slightly lower x value so the user can tell
            if bmNumber != self.cBeatmap:
                rectX += self.bmOffset

            # create the rectangle used for the beatmap
            tempRect = (rectX, self.offset + beatmap[1], beatmap[2], beatmap[3])
            # draw the rectangle onto the temporary surface
            pygame.draw.rect(surface, (0, 255, 0), tempRect)
            # create text with the beatmap's name and difficulty
            tempString = "{} [{}]".format(self.beatmaps[bmNumber]["Title"], self.beatmaps[bmNumber]["Version"])
            # blit the text onto the rectangle
            surface.blit(self.font.render(tempString, True, (0, 0, 0)), (rectX, int(beatmap[1] + self.offset)))


    def getRenderSnapshot(self, interpolation, tempSurface):
        """
        Render the gamestate
        interpolation: ?
        tempSurface: surface to draw to
        """

        # blit the backgroud image
        tempSurface.blit(self.bgIMG, (0, 0))
        # if safe mode is enabled, draw over the background image
        if config.safeMode:
            tempSurface.fill((150, 150, 150))

        # reset the surface to a clear blank surface
        self.beatmapFrame.fill((0, 0, 0, 0))
        # blit the beatmap rectangles onto the frame
        self.drawBeatmapRects(self.beatmapFrame)
        # blit the beatmap frame onto the main surface
        tempSurface.blit(self.beatmapFrame, ((config.SCREEN_RESOLUTION[0] / 3) * 2, 0))
        self.DrawInfoPanel(tempSurface)
