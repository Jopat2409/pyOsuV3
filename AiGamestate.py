
import pygame
import config




class pickButtonClass:


    def __init__(self):

        self.bWidth = int(config.SCREEN_RESOLUTION[0] / 2)
        self.bHeight = int(config.SCREEN_RESOLUTION[1] / 9)

        self.bX = int((config.SCREEN_RESOLUTION[0]  - self.bWidth) / 2)
        self.bY = int((config.SCREEN_RESOLUTION[1] - self.bHeight*3) / 2)

        self.buttonText = ["PLAY", "TRAIN"]
        self.font = pygame.font.SysFont('Arial', 25)

        self.buttonBounds = [(self.bX, self.bY+self.bHeight*i*2, self.bWidth, self.bHeight) for i in range(2)]
        print(self.buttonBounds)

    def render(self, surface):
        
        for b in range(len(self.buttonBounds)):
            print(b)
            pygame.draw.rect(surface, config.PINK, self.buttonBounds[b])
            surface.blit(self.font.render(self.buttonText[b], True, (0,0,0)), (self.buttonBounds[b][0], self.buttonBounds[b][1]))

        


class gsNeuralNetworkTrain:


    def __init__(self, parentClass):

        self.parentClass = parentClass

        self.cButtonWrapper = pickButtonClass()



    def getRenderSnapshot(self, interpolation):

        tempSurface = pygame.Surface(config.SCREEN_RESOLUTION)

        tempSurface.fill((255,0,0))

        self.cButtonWrapper.render(tempSurface)


        return tempSurface


    def update(self):

        return 0
