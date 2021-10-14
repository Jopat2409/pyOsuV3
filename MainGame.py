import GameState
import config
import time
import sys
import pygame
import traceback
import logging


# class that controls the whole game
class osuGame():

    def __init__(self):

        # defines how many times per second the game updates
        self.MS_PER_UPDATE = 1/500

        # initializes the class used for managing the current game state
        self.gsManager = GameState.gameStateManager()
        # set's the game's running state to TRUE
        self.running = True

        self.frames = 0
        self.updates = 0

        # starts the game loop
        self.gameLoop()



    def gameLoop(self):

        # initialized the prevTime and lag variables
        prevTime = time.time()
        lag = 0.0
        frames = 0
        updates = 0
        pTime = time.perf_counter()
        while(self.running):
            if time.perf_counter() - pTime >= 1:
                #print("{} frames per second".format(frames))
                #print("{} updates per second".format(updates))
                self.frames = frames
                self.updates = updates
                frames = 0
                updates = 0
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
                self.gsManager.update()
                lag -= self.MS_PER_UPDATE
                self.updates += 1
            # render's the game as many times as possible per second, passing the time between updates to the renderer for linear interpolation
            self.gsManager.render(lag/self.MS_PER_UPDATE, self.frames)
            frames += 1

        # exits when the program is done
        sys.exit(0)
            

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
    
        
