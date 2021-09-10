
import pygame
import pygame.gfxdraw
import config
import math
import sys

import BeatmapSelect


class MainButton:

    def __init__(self, parent):


        self.radius = math.ceil((330*config.CURRENT_SCALING) / 2)
        self.rRadius = math.ceil((296*config.CURRENT_SCALING) / 2)
        self.pos = (math.ceil(config.SCREEN_RESOLUTION[0] / 2), math.ceil(config.SCREEN_RESOLUTION[1] / 2))

        self.bMargin = math.ceil((self.radius*2) / 10)
        self.bHeight = math.ceil(((self.radius*2) - (self.bMargin*5)) / 3)
        self.bWidth = math.ceil(config.SCREEN_RESOLUTION[0] / 2.25)
        self.bX = math.ceil(self.pos[0] - (self.radius/5))
        self.bY = math.ceil((self.pos[1] - self.radius) + self.bMargin)

        self.buttons = ["Play", "AI", "Exit"]
        self.functions = [self.optionPlay, self.defunctFunct, self.exit]

        self.parentClass = parent
        
        
        self.active = False


    def optionPlay(self):

        self.parentClass.newGamestate(BeatmapSelect.gsBeatmapSelect(self.parentClass))

    def defunctFunct(self):
        pass
    
    def exit(self):
        pygame.display.quit()
        pygame.quit()
        sys.exit(0)
    
    def render(self, surface):
        if not self.active:
            pygame.gfxdraw.filled_circle(surface, self.pos[0], self.pos[1], self.radius, config.WHITE)
            pygame.gfxdraw.filled_circle(surface, self.pos[0], self.pos[1], self.rRadius, config.PINK)
        else:
            for i in range(3):
                pygame.draw.rect(surface, config.BLUE, (self.bX, (self.bY + (self.bHeight+self.bMargin)*i), self.bWidth, self.bHeight))
            pygame.gfxdraw.filled_circle(surface, self.pos[0] - 300, self.pos[1], self.radius, config.WHITE)
            pygame.gfxdraw.filled_circle(surface, self.pos[0] - 300, self.pos[1], self.rRadius, config.PINK)


    def checkBounds(self, pos):
        print("Checking Main menu Bounds")
        if not self.active:
            if pos[0] >= self.pos[0]-self.radius and pos[0] <= self.pos[0] + self.radius:
                print("Xs Match")
                if pos[1] >= self.pos[1]-self.radius and pos[1] <= self.pos[1] + self.radius:
                    print("Within Bounds")
                    self.active = True
                    return True
        else:
            if pos[0] >= self.bX and pos[0] <= self.pos[0]+self.bWidth:
                for i in range(3):
                    if pos[1] >= (self.bY + (self.bHeight+self.bMargin)*i) and pos[1] <= (self.bY + (self.bHeight+self.bMargin)*i) + self.bHeight:
                        self.functions[i]()
                        return True

        


        
class gsMenu:

    def __init__(self, parent):

        bgPath = config.DEFAULT_PATH + '/assets/bg/online_background_ce0fcca19f9d1c89cb28dd1d9946596d.jpg'
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

        tempSurface = pygame.Surface(config.SCREEN_RESOLUTION)
        tempSurface.blit(self.bgIMG, (0,0))
        tempSurface.fill((150,150,150))

        for _object in self.buttons:
            _object.render(tempSurface)
            

        #tempSurface.fill((200,0,200))

        return tempSurface

                
        


        
