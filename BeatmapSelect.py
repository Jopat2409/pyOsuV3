import random
import pickle
import os
import config
import glob
import BeatmapParse
import pygame
import math




class gsBeatmapSelect:





    def __init__(self, parentClass):

        self.parentClass = parentClass

        self.beatmaps = []



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

        self.font = pygame.font.SysFont('Arial', 25)

        if os.path.isfile(cPath):
            with open(cPath, 'r') as file:
                self.beatmaps = pickle.load(file)
        else:
            for beatmap in os.listdir("%s/beatmaps/"%config.DEFAULT_PATH):
                PATH = "%s\\beatmaps\\%s"%(config.DEFAULT_PATH, beatmap)
                for diff in glob.glob(PATH + "/" + "*.osu"):
                    
                    self.beatmaps.append(BeatmapParse.shallowRead(diff))
        print(self.beatmaps[0])
        self.calculateBmBounds()


        # points to the current index of the beatmap currently selected
        self.cBeatmap = random.randint(0, len(self.beatmaps))
        #print(len(self.beatmaps))
        #print(self.cBeatmap)

    def mButtonDown(self):

        #print("Mouse pressed")

        mX, mY = pygame.mouse.get_pos()
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

        print(self.beatmapBounds)
            
        

    def mButtonUp(self):

        if self.scrolling:
            self.scrolling = False
            self.decelerating = True
            self.velY = math.ceil(self.velTotal / self.velCount)
            #print(self.velY)

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


        for beatmap in self.beatmapBounds:
            # break out of for loop once all on screen beatmaps have been drawn
            if beatmap[1] + self.offset > config.SCREEN_RESOLUTION[1]:
                break
            # skip beatmap if it is off the top of the screen
            if beatmap[1] + self.offset + self.bmHeight < 0:
                continue
            # create the rectangle that will be drawn
            tempRect = (beatmap[0], beatmap[1]+self.offset, beatmap[2], beatmap[3])
            pygame.draw.rect(surface, (0,255,0),tempRect)
            surface.blit(self.font.render(beatmap["Title"], True, (0,0,0)), (int(beatmap[0]), int(beatmap[1]+self.offset)))

        
        

            

        

        

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


        
