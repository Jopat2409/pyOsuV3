
import pygame
import pygame.gfxdraw
import config
import math
import sys

import BeatmapSelect

# class for handling the main button in the middle
class MainButton:

    def __init__(self, parent):

        ## ---------- DEFINING SCALED DIMENSIONS ----------- ##
        self.radius = math.ceil((330*config.CURRENT_SCALING) / 2)
        self.rRadius = math.ceil((296*config.CURRENT_SCALING) / 2)
        self.pos = (math.ceil(config.SCREEN_RESOLUTION[0] / 2), math.ceil(config.SCREEN_RESOLUTION[1] / 2))

        self.bMargin = math.ceil((self.radius*2) / 10)
        self.bHeight = math.ceil(((self.radius*2) - (self.bMargin*5)) / 3)
        self.bWidth = math.ceil(config.SCREEN_RESOLUTION[0] / 2.25)
        self.bX = math.ceil(self.pos[0] - (self.radius/5))
        self.bY = math.ceil((self.pos[1] - self.radius) + self.bMargin)

        ## ----------------------------------------=---------##

        # the three buttons that can be selected
        self.buttons = ["Play", "AI", "Exit"]
        # the functions that correspond to them
        self.functions = [self.optionPlay, self.defunctFunct, self.exit]

        # get instance of parent class
        self.parentClass = parent
        
        # tracks wether or not the center button has been pressed
        self.active = False


    def optionPlay(self):
        #print("Playing")
        # switch to the next gamestate
        self.parentClass.newGamestate(BeatmapSelect.gsBeatmapSelect(self.parentClass))

    def defunctFunct(self):
        pass
    
    def exit(self):
        # exit out of the game
        pygame.display.quit()
        pygame.quit()
        sys.exit(0)
    
    def render(self, surface):
        # render the main osu button depending on wether or not it is active
        if not self.active:
            pygame.gfxdraw.filled_circle(surface, self.pos[0], self.pos[1], self.radius, config.WHITE)
            pygame.gfxdraw.filled_circle(surface, self.pos[0], self.pos[1], self.rRadius, config.PINK)
        else:
            for i in range(3):
                # render the three buttons
                pygame.draw.rect(surface, config.BLUE, (self.bX, (self.bY + (self.bHeight+self.bMargin)*i), self.bWidth, self.bHeight))
            # draw the osu button at an offset
            pygame.gfxdraw.filled_circle(surface, self.pos[0] - 300, self.pos[1], self.radius, config.WHITE)
            pygame.gfxdraw.filled_circle(surface, self.pos[0] - 300, self.pos[1], self.rRadius, config.PINK)


    def checkBounds(self, pos):
        #print("Checking Main menu Bounds")
        # check if the mouse is within the bounds of the main button if it is not already active
        if not self.active:
            if pos[0] >= self.pos[0]-self.radius and pos[0] <= self.pos[0] + self.radius:
                #print("Xs Match")
                if pos[1] >= self.pos[1]-self.radius and pos[1] <= self.pos[1] + self.radius:
                    #print("Within Bounds")
                    self.active = True
                    return True
        else:
            #check if the x values match the three buttons
            if pos[0] >= self.bX and pos[0] <= self.pos[0]+self.bWidth:
                # loop through and check the y values
                for i in range(3):
                    if pos[1] >= (self.bY + (self.bHeight+self.bMargin)*i) and pos[1] <= (self.bY + (self.bHeight+self.bMargin)*i) + self.bHeight:
                        self.functions[i]()
                        return True

        


        
class gsMenu:

    def __init__(self, parent):

        # set the background image
        bgPath = config.DEFAULT_PATH + '/assets/bg/online_background_ce0fcca19f9d1c89cb28dd1d9946596d.jpg'

        # scale the image to the size of the screen
        bg = pygame.image.load(bgPath)
        self.bgIMG = pygame.transform.scale(bg, config.SCREEN_RESOLUTION)

        self.parent = parent


        # --------------- game object components -------------#

        self.buttons = [MainButton(self.parent)]


        

    def update(self):
        pass


    def buttonNotPressed(self):
        self.buttons[0].active = False


        

    def getRenderSnapshot(self, interpolation):

        # create the surface that will be blitted to the main window
        tempSurface = pygame.Surface(config.SCREEN_RESOLUTION)
        # add the background image
        tempSurface.blit(self.bgIMG, (0,0))
        if config.safeMode:
            tempSurface.fill((150,150,150))

        # render all of the objects
        for _object in self.buttons:
            _object.render(tempSurface)
            

        #tempSurface.fill((200,0,200))

        return tempSurface

                
        


        
