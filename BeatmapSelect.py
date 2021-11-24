""" ---------- OSU MODULES ---------- """
import config                               # for program-global variables
import BeatmapParse                         # for parsing beatmaps
import BeatmapPlay                          # for playing beatmaps
import SkinLoader                           # for loading assets
""" ---------- PYTHON MODULES ---------- """
import random                               # for initializing song choice
import pickle                               # for serializing beatmaps
import os                                   # for joining paths
import glob                                 # for traversing beatmap directory
import pygame                               # for rendering
import math                                 # for rounding
import time                                 # for syncing beatmap and audio
import sys                                  # for exiting game
import checksumdir                          # for getting hash of beatmap files



class gsBeatmapSelect:

    def __init__(self, parentClass):

        # gets a reference to the parent class
        self.parentClass = parentClass

        # store a pointer to the sound handler
        self.soundHandler = parentClass.soundStream

        # array of beatmaps
        self.beatmaps = []

        # gamestate Unique identifier
        self.UUID = "gsBeatmapSelect"


        
        # gets the current osu multiplayer background
        bgPath = config.DEFAULT_PATH + '/assets/bg/online_background_68261587a4e3fbe77cad07120ee1e864.jpg'
        # load the background intoa pygame
        bg = pygame.image.load(bgPath)
        # scale it to the size of the screen
        self.bgIMG = pygame.transform.scale(bg, config.SCREEN_RESOLUTION)

        
        self.beatmapBounds = []

        # hard coded number representing how many beatmaps are shown on screen at once
        self.BMS = 7                # beatmaps per screen
        self.bmHeight = 150         # height of beatmap
        self.bmMargin = 10          # space between beatmaps
        self.bmOffset = 15          # offset from side of container
    
        # previous y coordinate of the mouse, used to scroll through beatmaps
        self.prevMY = 0

        # hard coded integers to do with movement of beatmap container
        self.offset = 0             # current offset of the beatmap array
        self.scrolling = False      # wether or not the user is scrolling
        self.decelerating = False   # used for smooth scrolling
        self.velTotal = 0           # used for smooth scrolling
        self.velCount = 0           # used for smooth scrolling
        self.velY = 0               # current velocity of the beatmap container
        self.decel = 1              # current decelleration
        self.decelCount = 0         # used for smooth scrolling
        self.maxMouseMovement = 5   # how much mouse input is considerd when decelerating

        # intialize the default font
        self.font = pygame.font.SysFont('Arial', 25)

        # load the assets for the beatmap select gamestate        
        SkinLoader.loadBeatmapSelectImages()
        # initialize the timer for timing how long it takes to load beatmaps
        bmLoadStart = time.time()
        # checks for beatmap cache
        cPath = config.DEFAULT_PATH + '\\.temp\\beatmapSelect.dat'
        # checks to see if a beatmap cache already exists
        if os.path.isfile(cPath):
            # if it does, load the objects stored in at directory cPath as self.beatmaps
            data = None
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
            for beatmap in os.listdir("%s/beatmaps/"%config.DEFAULT_PATH):
                PATH = "%s\\beatmaps\\%s"%(config.DEFAULT_PATH, beatmap)
                # append the checksum of the beatmap directory (used for loading when changed)
                bmParsed.append(checksumdir.dirhash(PATH))
                # loop through all .osu files in beatmap directory
                for diff in glob.glob(PATH + "/" + "*.osu"):
                    # parse .osu file and append it to list of beatmaps
                    self.beatmaps.append(BeatmapParse.shallowRead(diff,PATH))
                    count += 1
            print(f"Loaded {count} new beatmaps!")
            # writes it to cPath when all beatmaps are parsed
            with open(cPath, 'wb') as beatmapFile:
                tempData = (self.beatmaps, bmParsed)
                pickle.dump(tempData, beatmapFile)
        # calculate the bounds of all of the buttons / beatmap selection buttons
        self.calculateBmBounds()
        # output the time taken to load the beatmaps (DEBUG)
        print("It took {}s to load all beatmaps".format(time.time()-bmLoadStart))

        # points to the current index of the beatmap currently selected
        self.cBeatmap = -1

    """
    Called when the mouse button is pressed down
    """
    def mButtonDown(self):
        # get the current mouse position
        self.prevMousePos = pygame.mouse.get_pos()
        # unpack the tuple
        mX, mY = self.prevMousePos
        # if the x position is within the bounds of the beatmap bounding box
        if (mX > (config.SCREEN_RESOLUTION[0] / 3)*2) and mX < config.SCREEN_RESOLUTION[0]:
            # scrolling true
            self.scrolling = True
            # set the previous mouse position
            self.prevMY = pygame.mouse.get_pos()[1]

    def calculateBmBounds(self):

        self.bmOffset = math.ceil(config.SCREEN_RESOLUTION[0] / 60)
        self.bmHeight = math.ceil(config.SCREEN_RESOLUTION[1] / 10)
        self.bmWidth = config.SCREEN_RESOLUTION[0] / 3 + self.bmOffset
        self.bmMargin = math.ceil(self.bmHeight / 10)
        
        drawCount = 0
        for beatmap in self.beatmaps:

            self.beatmapBounds.append((0,(self.bmMargin*(drawCount+1) + self.bmHeight*drawCount), self.bmWidth, self.bmHeight))
            drawCount += 1

            
        

    def mButtonUp(self):

        if self.scrolling:
            tempX, tempY = pygame.mouse.get_pos()
            mDiff = abs((tempX - self.prevMousePos[0])^2 + (tempY - self.prevMousePos[1])^2)
            if mDiff <= self.maxMouseMovement^2:
                print("PRESSED BUTTON")
                self.scrolling = False
                self.decelerating = False
                self.velY = 0

                self.getBeatmap(tempY)
                return
            self.scrolling = False
            self.decelerating = True
            try:
                self.velY = math.ceil(self.velTotal / self.velCount)
            except ZeroDivisionError:
                pass
            #print(self.velY)

        


    def getBeatmap(self, mY):
        bmCount = 0
        print("getting beatmaps")
        for beatmap in self.beatmapBounds:
            bmOffset = beatmap[1] + self.offset
            if mY >= bmOffset and mY <= (bmOffset + self.bmHeight):
                if self.cBeatmap == bmCount:
                    self.parentClass.pauseGamestate(BeatmapPlay.gsBeatmapPlayer(self.beatmaps[self.cBeatmap], self.parentClass, False))
                else:
                    self.cBeatmap = bmCount
                    self.soundHandler.previewSong(self.beatmaps[bmCount]["BasePath"]+"/"+self.beatmaps[bmCount]["AudioFilename"],int(self.beatmaps[bmCount]["PreviewTime"]))
                    PATH = os.path.join(self.beatmaps[bmCount]["BasePath"],self.beatmaps[bmCount]["BackgroundImage"])
                    PATH = PATH.replace("\\","/")
                    bg = pygame.image.load(PATH.strip())
                    self.bgIMG = pygame.transform.scale(bg, config.SCREEN_RESOLUTION)
                return
            bmCount += 1


            

        


    def update(self):


        if self.scrolling:
            self.velY = pygame.mouse.get_pos()[1] - self.prevMY
            if self.velY != 0:
                self.velCount += 1
                self.velTotal += self.velY
            self.offset += self.velY
            self.prevMY = pygame.mouse.get_pos()[1]
        elif self.decelerating:
            self.offset += self.velY
            if self.velY > 0:
                self.velY -= self.decel
                if self.velY <= 0:
                    self.decelerating = False
            elif self.velY < 0:
                self.velY += self.decel
                if self.velY >= 0:
                    self.decelerating = False

                


    def drawBeatmapRects(self, surface):

        drawnbeatmaps = []
        drawCount = 0

        bmNumber = -1
        for beatmap in self.beatmapBounds:
            bmNumber += 1
            # break out of for loop once all on screen beatmaps have been drawn
            if beatmap[1] + self.offset > config.SCREEN_RESOLUTION[1]:
                break
            # skip beatmap if it is off the top of the screen
            if beatmap[1] + self.offset + self.bmHeight < 0:
                continue
            # create the rectangle that will be drawn
            rectX = self.bmMargin
            
            if bmNumber != self.cBeatmap:
                rectX += self.bmOffset


            tempRect = (rectX, self.offset + beatmap[1], beatmap[2], beatmap[3])
            pygame.draw.rect(surface, (0,255,0),tempRect)
            try:
                tempString = "{} [{}]".format(self.beatmaps[bmNumber]["Title"], self.beatmaps[bmNumber]["Version"])
            except TypeError:
                print(bmNumber)
                print(self.beatmaps[bmNumber-1])
                sys.exit(0)
            surface.blit(self.font.render(tempString, True, (0,0,0)), (rectX, int(beatmap[1]+self.offset)))
        
    """
    Render the gamestate
    interpolation: ?
    tempSurface: surface to draw to
    """
    def getRenderSnapshot(self, interpolation, tempSurface):
        
        # blit the backgroud image
        tempSurface.blit(self.bgIMG, (0,0))
        # if safe mode is enabled, draw over the background image
        if config.safeMode:
            tempSurface.fill((150,150,150))

        # create the frame that holds the beatmap selection buttons
        beatmapFrame = pygame.Surface((config.SCREEN_RESOLUTION[0] / 3, config.SCREEN_RESOLUTION[1]), pygame.SRCALPHA, 32)
        beatmapFrame.convert_alpha()
        
        # blit the beatmap rectangles onto the frame
        self.drawBeatmapRects(beatmapFrame)

        # blit the beatmap frame onto the main surface
        tempSurface.blit(beatmapFrame, ((config.SCREEN_RESOLUTION[0] / 3)*2,0))

        # blit the beatmap selection overlay
        tempSurface.blit(SkinLoader.stateMap["selectOverlay"], (0,0))