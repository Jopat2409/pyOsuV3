""" ---------- OSU MODULES ---------- """
import config

""" ---------- PYTHON MODULES ---------- """
import pygame

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
        self.bX = int((config.SCREEN_RESOLUTION[0] - self.bWidth) / 2)
        self.bY = int((config.SCREEN_RESOLUTION[1] - self.bHeight * 3) / 2)

        # set the text of the buttons
        self.buttonText = ["PLAY", "TRAIN"]
        # create the font used for the buttons
        self.font = pygame.font.SysFont('Arial', 25)

        # create the button bounds
        self.buttonBounds = [(self.bX, self.bY + self.bHeight * i * 2, self.bWidth, self.bHeight) for i in range(2)]
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
            surface.blit(self.font.render(self.buttonText[b], True, (0, 0, 0)),
                         (self.buttonBounds[b][0], self.buttonBounds[b][1]))


class gsNeuralNetworkTrain:

    def __init__(self, parentClass):

        # reference to the parent gamestate manager
        self.parentClass = parentClass
        # create buttons
        self.cButtonWrapper = pickButtonClass(self)

    """
    Called when the mouse is released
    """

    def mButtonUp(self):
        # unpack current mouse position
        mX, mY = pygame.mouse.get_pos()
        # loop through buttons
        for i in self.cButtonWrapper.buttonBounds:
            # reference to current button
            button = self.cButtonWrapper.buttonBounds[i]
            # if the mouse's x coordinate is within the bounds of the button
            if button[0] <= mX <= button[2]:
                # if the mouse's y coordinate is within the bounds of the button
                if button[1] <= mY < button[3]:
                    # call the function
                    self.cButtonWrapper.buttonFunct[i]()
                    # break, as no other button can be pressed
                    break

    """
    Render gamestate onto the main window
    tempSurface: surface to be rendered onto
    """

    def getRenderSnapshot(self, tempSurface):

        # render the buttons
        self.cButtonWrapper.render(tempSurface)
        return tempSurface

    """
    Update the gamestate
    """

    def update(self):

        return 0
