import random
import pickle
import os
import config
import glob
import BeatmapParse
import pygame
import math
import time
import BeatmapPlay




class gsBeatmapSelect:





    def __init__(self, parentClass):

        self.parentClass = parentClass

        # store a pointer to the sound handler
        self.soundHandler = parentClass.soundStream

        # array of beatmaps
        self.beatmaps = []

        self.UUID = "gsBeatmapSelect"


        
        cPath = bgPath = config.DEFAULT_PATH + '/temp/beatmapSelect.obj'
        bgPath = config.DEFAULT_PATH + '/assets/bg/online_background_68261587a4e3fbe77cad07120ee1e864.jpg'
        bg = pygame.image.load(bgPath)
        self.bgIMG = pygame.transform.scale(bg, config.SCREEN_RESOLUTION)

        self.beatmapBounds = []

        # hard coded number representing how many beatmaps are shown on screen at once
        self.BMS = 7            # beatmaps per screen
        self.bmHeight = 150     # height of beatmap
        self.bmMargin = 10      # space between beatmaps
        self.bmOffset = 15      # offset from side of container

        # previous y coordinate of the mouse, used to scroll through beatmaps
        self.prevMY = 0

        # hard coded integers to do with movement of beatmap container
        self.offset = 0
        self.scrolling = False
        self.decelerating = False
        self.velTotal = 0
        self.velCount = 0
        self.velY = 0
        self.decel = 1
        self.decelCount = 0
        self.maxMouseMovement = 5


        self.font = pygame.font.SysFont('Arial', 25)

        bmLoadStart = time.time()

        if os.path.isfile(cPath):
            with open(cPath, 'r') as file:
                self.beatmaps = pickle.load(file)
        else:
            for beatmap in os.listdir("%s/beatmaps/"%config.DEFAULT_PATH):
                PATH = "%s\\beatmaps\\%s"%(config.DEFAULT_PATH, beatmap)
                for diff in glob.glob(PATH + "/" + "*.osu"):
                    
                    self.beatmaps.append(BeatmapParse.shallowRead(diff,PATH))
        self.calculateBmBounds()
        print("It took {}s to load all beatmaps".format(time.time()-bmLoadStart))
        #print(self.beatmaps)


        # points to the current index of the beatmap currently selected
        self.cBeatmap = -1
        #print(len(self.beatmaps))
        #print(self.cBeatmap)
        print(self.beatmaps)

    def mButtonDown(self):

        #print("Mouse pressed")

        self.prevMousePos = pygame.mouse.get_pos()
        mX, mY = self.prevMousePos
        if (mX > (config.SCREEN_RESOLUTION[0] / 3)*2) and mX < config.SCREEN_RESOLUTION[0]:
            self.scrolling = True
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
                    self.parentClass.pauseGamestate(BeatmapPlay.gsBeatmapPlayer(self.beatmaps[self.cBeatmap], self.parentClass))
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
            

        
        

            

        

        

    def getRenderSnapshot(self, interpolation):

        tempSurface = pygame.Surface(config.SCREEN_RESOLUTION)
        tempSurface.blit(self.bgIMG, (0,0))
        if config.safeMode:
            tempSurface.fill((150,150,150))

        beatmapFrame = pygame.Surface((config.SCREEN_RESOLUTION[0] / 3, config.SCREEN_RESOLUTION[1]), pygame.SRCALPHA, 32)
        beatmapFrame.convert_alpha()
        

        #beatmapFrame.fill((0,0,0))
        self.drawBeatmapRects(beatmapFrame)

        tempSurface.blit(beatmapFrame, ((config.SCREEN_RESOLUTION[0] / 3)*2,0))

        return tempSurface
                
            
            

        # this is for loading up all of the beatmap information that is required


        
