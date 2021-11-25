
import pygame
import config


"""
Class to encapsulate the buttons within the gamestate
parent: pointer to parent gamestate class
// WILL OVERRIDE THIS WITH UI METHODS
"""
class pickButtonClass:


    def __init__(self, parent):

        self.parent = parent
        # set the scaled button width
        self.bWidth = int(config.SCREEN_RESOLUTION[0] / 2)
        # get the scaled button height
        self.bHeight = int(config.SCREEN_RESOLUTION[1] / 9)

        # get the scaled x and y of the buttons
        self.bX = int((config.SCREEN_RESOLUTION[0]  - self.bWidth) / 2)
        self.bY = int((config.SCREEN_RESOLUTION[1] - self.bHeight*3) / 2)
 
        # set the text of the buttons
        self.buttonText = ["PLAY", "TRAIN"]
        # create the font used for the buttons
        self.font = pygame.font.SysFont('Arial', 25)

        # create the button bounds
        self.buttonBounds = [(self.bX, self.bY+self.bHeight*i*2, self.bWidth, self.bHeight) for i in range(2)]
        # create the button functions
        self.buttonFunc = [self.play, self.train]

    """
    Render the buttons to a surface
    surface: surface to render to
    """
    def render(self, surface):
        
        # loop through all of the buttons
        for b in range(len(self.buttonBounds)):
            print(b)
            pygame.draw.rect(surface, config.PINK, self.buttonBounds[b])
            surface.blit(self.font.render(self.buttonText[b], True, (0,0,0)), (self.buttonBounds[b][0], self.buttonBounds[b][1]))


class gsNeuralNetworkTrain:


    def __init__(self, parentClass):

        self.parentClass = parentClass

        self.cButtonWrapper = pickButtonClass(self)

    def mButtonUp(self):

        mX, mY = pygame.mouse.get_pos()
        for i in self.cButtonWrapper.buttonBounds:
            button = self.cButtonWrapper.buttonBounds[i]
            if mX >= button[0] and mX <= button[2]:
                if mY >= button[1] and mY < button[3]:
                    self.cButtonWrapper.buttonFunct[i]()
                    break


    def getRenderSnapshot(self, interpolation):

        tempSurface = pygame.Surface(config.SCREEN_RESOLUTION)

        tempSurface.fill((255,0,0))

        self.cButtonWrapper.render(tempSurface)


        return tempSurface


    def update(self):

        return 0
