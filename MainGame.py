import GameState
import config
import time
import sys
import pygame
import traceback



class osuGame():




    def __init__(self):

        self.MS_PER_UPDATE = 1/60

        self.gsManager = GameState.gameStateManager()
        self.running = True

        self.gameLoop()



    def gameLoop(self):

        prevTime = time.time()
        lag = 0.0
        
        while(self.running):

            cTime = time.time()
            elapsedTime = cTime - prevTime
            prevTime = cTime
            lag += elapsedTime
            self.handleInput()
            while lag >= self.MS_PER_UPDATE:
                self.gsManager.update()
                lag -= self.MS_PER_UPDATE
            self.gsManager.render(lag/self.MS_PER_UPDATE)

        sys.exit(0)
            

    def handleInput(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYUP:
                try:
                    self.gsManager.mapInput(config.keyBindings[pygame.key.name(event.key).upper()])
                    #print(config.keyBindings[pygame.key.name(event.key).upper()])
                except KeyError:
                    pass
            elif event.type == pygame.MOUSEBUTTONUP:
                try:
                    self.gsManager.cGamestate.mButtonUp()
                except AttributeError:
                    pass
                try:
                    self.gsManager.checkButtonBounds(pygame.mouse.get_pos())
                except:
                    pass
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("Mouse button prseeded own")
                try:
                    self.gsManager.cGamestate.mButtonDown()
                except AttributeError:
                    pass
                    print(traceback.format_exc())
    
        
