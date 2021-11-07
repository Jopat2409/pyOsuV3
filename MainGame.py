""" ---------- OSU MODULES ---------- """
import GameState                            # for handling different gamestates
import config                               # for program global variables
import UiManager                            # for managing UI elements
import UiElements                           # for creating UI elements
import SkinLoader                           # for loading assets

""" ---------- PYTHON MODULES ---------- """
import time                                 # for perf_counter()
import sys                                  # for exiting game
import pygame                               # for rendering and sound
import traceback                            # for getting error messages
import logging                              # for logging errors




"""
This class holds all of the general information and functions used throughout the game, such as the gameloop,
input handling methods and render/update methods
"""
class osuGame():

    def __init__(self):

        # defines how many times per second the game updates
        self.MS_PER_UPDATE = 1/500
        # initializes the class used for managing the current game state
        self.gsManager = GameState.gameStateManager()
        # set's the game's running state to TRUE
        self.running = True
        # initializes the external frame and update per second counters
        self.frames = 0
        self.updates = 0

        # initializes the UI manager 
        self.uiManager = UiManager.uiManager()
        # passes the ui manager to the gamestate manager
        self.gsManager.setUiManager(self.uiManager)
        # creates the default UI used 
        self.createDefaultUi()
        # loads all necessary assets
        SkinLoader.loadImageMaps()
        

        # starts the game loop
        self.gameLoop()

    """ Method for creating the default UI used throughout all gamestates """
    def createDefaultUi(self):

        # create the chat window group
        self.uiManager.createGroup("ChatWindow", shownOnCreation=False)
        
    def defunctFunct(self):
        print("Worked")

    """ The main gameloop of the program """
    def gameLoop(self):

        # store the current time
        prevTime = time.time()
        #initialize lag to 0.0
        lag = 0.0
        # initialize the internal frame counters
        frames = 0
        updates = 0
        # get the time since the program was ran
        pTime = time.perf_counter()

        # loop while running is true
        while(self.running):
            # if one second has elapsed since the last time this block of code was ran
            if time.perf_counter() - pTime >= 1:
                print("{} frames per second".format(frames))
                print("{} updates per second".format(updates))
                # update the viewable frames and updates counter
                self.frames = frames
                self.updates = updates
                # reset the internal counters
                frames = 0
                updates = 0
                # update the elapsed time
                pTime = time.perf_counter()
            # calculate the time taken for the last loop
            cTime = time.time()
            elapsedTime = cTime - prevTime
            prevTime = cTime
            lag += elapsedTime
            # handles inputs as many times per second as possible
            self.handleInput()
            # loop to ensure that the game updates at the correct tick rate as defined by MS_PER_UPDATE
            while lag >= self.MS_PER_UPDATE:
                # update the gamestate manager
                self.gsManager.update()
                # update the lag
                lag -= self.MS_PER_UPDATE
                # increment the internal update counter
                updates += 1
            # render's the game as many times as possible per second, passing the time between updates to the renderer for linear interpolation
            self.gsManager.render(lag/self.MS_PER_UPDATE, self.frames)
            # increment the internal frame counter
            frames += 1

        # exits when the program is done
        pygame.quit()
        sys.exit(0)
            
    """ The function for handling game input """
    def handleInput(self):

        # loops through all inputs
        for event in pygame.event.get():
            # close game if x is pressed
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYUP:
                # attempts to map the key pressed to the correct function via the instance variable keyBindings
                try:
                    self.gsManager.mapInput(config.keyBindings[pygame.key.name(event.key).capitalize()])
                    #print(config.keyBindings[pygame.key.name(event.key).upper()])
                # if the current gamestate does not have a function for the key pressed, we do nothing
                except KeyError:
                    logging.warning(traceback.format_exc())
                
            elif event.type == pygame.MOUSEBUTTONUP:
                # try to call the mButtonUp function which is used for things that require mouse dragging etc
                try:
                    self.gsManager.cGamestate.mButtonUp()
                except AttributeError:
                    #print(traceback.format_exc())
                    logging.warning(traceback.format_exc())
                # try to call the checkButtonBounds function which checks to see if any buttons were pressed
                try:
                    self.gsManager.checkButtonBounds(pygame.mouse.get_pos())
                except:
                    #print(traceback.format_exc())
                    logging.warning(traceback.format_exc())
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # try to call the mButtonDow function which is used for objects that require handling of mouse dragging (scrolling etc)
                try:
                    self.gsManager.cGamestate.mButtonDown()
                except AttributeError:
                    logging.warning(traceback.format_exc())
                    #print(traceback.format_exc())

            # pass the event into the ui manager for seperate event handling
            self.uiManager.handleEvents(event.type)
    
        
