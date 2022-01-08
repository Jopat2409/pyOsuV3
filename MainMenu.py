""" ---------- OSU MODULES ---------- """
import config  # for accessing program-global variables
import AiGamestate  # for next gamestate
import BeatmapSelect  # for next gamestate

""" ---------- PYTHON MODULES ---------- """
import pygame  # for rendering
import pygame.gfxdraw  # for anti-aliased rendering
import math  # for rounding
import sys  # for exiting program
import glob  # for getting background image
import random  # for getting background image
import os  # for joining paths

"""
Class for handling the main UI section of the gamestate
need to change this and implement a UI manager
"""


class MainButton:

    def __init__(self, parent):

        # ---------- DEFINING SCALED DIMENSIONS ----------- #
        self.radius = math.ceil((330 * config.CURRENT_SCALING) / 2)
        self.rRadius = math.ceil((296 * config.CURRENT_SCALING) / 2)
        self.pos = (math.ceil(config.SCREEN_RESOLUTION[0] / 2), math.ceil(config.SCREEN_RESOLUTION[1] / 2))

        self.bMargin = math.ceil((self.radius * 2) / 10)
        self.bHeight = math.ceil(((self.radius * 2) - (self.bMargin * 5)) / 3)
        self.bWidth = math.ceil(config.SCREEN_RESOLUTION[0] / 2.25)
        self.bX = math.ceil(self.pos[0] - (self.radius / 5))
        self.bY = math.ceil((self.pos[1] - self.radius) + self.bMargin)

        # ----------------------------------------=---------#

        # the three buttons that can be selected
        self.buttons = ["Play", "AI", "Exit"]
        # the functions that correspond to them
        self.functions = [self.optionPlay, self.optionAI, self.exit]

        # get instance of parent class
        self.parentClass = parent

        # tracks whether or not the center button has been pressed
        self.active = False

    """
    Changes gamestate
    """

    def optionPlay(self):
        # switch to the beatmap selection gamestate
        self.parentClass.newGamestate(BeatmapSelect.gsBeatmapSelect(self.parentClass))

    """
    Changes gamestate
    """

    def optionAI(self):
        # sets the gamestate to the ai interface gamestate
        self.parentClass.newGamestate(AiGamestate.gsNeuralNetworkTrain(self.parentClass))

    """
    Exits the whole program
    """

    def exit(self):
        # exit out of the game
        config.isRunning = False

    """
    Renders the button onto the gamestate
    """

    def render(self, surface):
        # render the main osu button depending on wether or not it is active
        if not self.active:
            # draw the white outline around the circle
            pygame.gfxdraw.filled_circle(surface, self.pos[0], self.pos[1], self.radius, config.WHITE)
            # draw the pink interior
            pygame.gfxdraw.filled_circle(surface, self.pos[0], self.pos[1], self.rRadius, config.PINK)
            # create a rect for the main title text
            text_rect = config.titleFont.get_rect("OSU!ai", size=int(65 * config.CURRENT_SCALING))
            # center the text on the main screen
            text_rect.center = surface.get_rect().center
            # draw the text to the screen
            config.titleFont.render_to(surface, text_rect, "OSU!ai", (255, 255, 255),
                                       size=int(65 * config.CURRENT_SCALING))
        else:
            # draw the three buttons
            for i in range(3):
                # create the rect
                bgRect = pygame.Rect(self.bX, (self.bY + (self.bHeight + self.bMargin) * i), self.bWidth, self.bHeight)
                # draw the rectangle
                pygame.draw.rect(surface, config.BLUE, bgRect)
                # create a rect for the button text
                text_rect = config.titleFont.get_rect(self.buttons[i], size=int(20 * config.CURRENT_SCALING))
                # center the text within the button
                text_rect.center = bgRect.center
                # draw the text to the main screen
                config.titleFont.render_to(surface, text_rect, self.buttons[i], (255, 255, 255),
                                           size=int(20 * config.CURRENT_SCALING))
            # render the main osu button at an offset
            pygame.gfxdraw.filled_circle(surface, self.pos[0] - 300, self.pos[1], self.radius, config.WHITE)
            pygame.gfxdraw.filled_circle(surface, self.pos[0] - 300, self.pos[1], self.rRadius, config.PINK)

    def checkBounds(self, pos):
        # check if the mouse is within the bounds of the main button if it is not already active
        if not self.active:
            # check if the mouse's x position is within the button's bounds
            if self.pos[0] - self.radius <= pos[0] <= self.pos[0] + self.radius:
                # check if the mouse's y position is within the button's bounds
                if self.pos[1] - self.radius <= pos[1] <= self.pos[1] + self.radius:
                    self.active = True
                    return True
        else:
            # check if the x values match the three buttons
            if self.bX <= pos[0] <= self.pos[0] + self.bWidth:
                # loop through and check the y values
                for i in range(3):
                    if (self.bY + (self.bHeight + self.bMargin) * i) <= pos[1] <= (
                            self.bY + (self.bHeight + self.bMargin) * i) + self.bHeight:
                        # if the mouse is within the button's bounds, run the corresponding function
                        self.functions[i]()
                        return True


class gsMenu:

    def __init__(self, parent):

        # set the background image
        images = glob.glob(os.path.join(config.DEFAULT_PATH, "assets/bg", "*.jpg"))
        imgToRender = os.path.join(config.DEFAULT_PATH, "assets/bg", random.choice(images))

        # scale the image to the size of the screen
        bg = pygame.image.load(imgToRender).convert()
        self.bgIMG = pygame.transform.scale(bg, config.SCREEN_RESOLUTION)
        # create the shaded bars at the top and bottom of the screen where information goes
        self.tempRectHeight = int(config.SCREEN_RESOLUTION[1] / 8)
        self.uiRect = pygame.Surface((config.SCREEN_RESOLUTION[0], self.tempRectHeight)).convert_alpha()
        self.uiRect.set_alpha(125)
        # get a reference to the parent gamestatemanager class
        self.parent = parent
        # create the gamestate specific keymap
        self.KEY_MAP = {}
        # --------------- game object components -------------#
        self.buttons = [MainButton(self.parent)]

    def update(self):
        pass

    def buttonNotPressed(self):
        # set the button to inactive if it is not pressed
        self.buttons[0].active = False

    def getRenderSnapshot(self, interpolation, tempSurface):

        # add the background image
        tempSurface.blit(self.bgIMG, (0, 0))
        # add a blank screen if safemode is enabled
        if config.safeMode:
            tempSurface.fill((150, 150, 150))

        # render all of the objects
        for _object in self.buttons:
            _object.render(tempSurface)

        # blit the two rectangles that make the UI look cleaner
        tempSurface.blit(self.uiRect, (0, 0))
        tempSurface.blit(self.uiRect, (0, config.SCREEN_RESOLUTION[1] - self.tempRectHeight))

        # tempSurface.fill((200,0,200))
