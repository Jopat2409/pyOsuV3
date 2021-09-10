

import MainMenu
import config
import queue
import pygame
import pygame.gfxdraw
import ctypes


class gameStateManager:


    def __init__(self):


        self.cGamestate = MainMenu.gsMenu(self)

        self.gsStack = queue.LifoQueue()
        ctypes.windll.user32.SetProcessDPIAware()
        
        self.GLOBAL_KEY_MAP = {"keyToggleChat":self.showChat,
                               "keyToggleExtendedChat":self.showExtendedChat,
                               "keyScreenshot":self.screenshot}

        self.chatToggle = False

        # uses fullscreen width if in fullscreen        
        if int(config.currentSettings["Fullscreen"]) == 1:
            self.window = pygame.display.set_mode((int(config.currentSettings["WidthFullscreen"]), int(config.currentSettings["HeightFullscreen"])))
            pygame.display.toggle_fullscreen()
        else:
            self.window = pygame.display.set_mode(config.SCREEN_RESOLUTION)


    """hashes all relevant info about a gamestate, should be used when the time between resuming the gamestate is relatively large, or if the new gamestate
    requires a large amount of processing power / memory
    """
    def suspendGamestate(self, NEW_GAMESTATE):
        filePath = config.DEFAULT_PATH + "/" + "%s.obj"%self.cGamestate.UUID
        file = open(filePath, 'w')
        pickle.dump(self.cGamestate, file)
        self.gsStack.put(self.cGamestate.UUID)
        del(self.cGamestate)
        self.cGamestate = NEW_GAMESTATE


    """simply puts all the info to one side but keeps it stored within the program. Should be used for when the time between resuming is likely to be relatively short
    """
    def pauseGamestate(self, NEW_GAMESTATE):

        self.gsStack.put(self.cGamestate)
        del(self.cGamestate)
        self.cGamestate = NEW_GAMESTATE



    def newGamestate(self, NEW_GAMESTATE):

        del(self.cGamestate)
        self.cGamestate = NEW_GAMESTATE
    
    """ delete the current gamestate and bring the last paused gamestate back to the current gamestate"""
    def resumeGamestate(self):

        tempGamestate = self.gsStack.pop()

        if temGamestate.isinstance(str):
            filePath = config.DEFAULT_PATH + "/" + "%s.obj"%tempGamestate
            del(self.cGamestate)
            self.cGamestate = pickle.load(filePath)
            
            # the paused gamestate has been suspended
        else:
            # the paused gamestate has been pushed to one side
            del(self.cGamestate)
            self.cGamestate = tempGamestate


    def update(self):

        # update current gamestate
        self.cGamestate.update()
            

    def render(self, interpolation):
        
        self.window.fill((255,255,255))
        self.window.blit(self.cGamestate.getRenderSnapshot(interpolation), (0,0))
        if self.chatToggle:
            pygame.draw.rect(self.window,(0,0,0),(200,150,100,50))

        mX, mY = pygame.mouse.get_pos()
        pygame.gfxdraw.filled_circle(self.window, mX, mY, 20, (200,200,0))
        pygame.display.update()


    def mapInput(self, inputs):

        for inputEvent in inputs:

            try:
                self.GLOBAL_KEY_MAP[inputEvent]()
                self.cGamestate.KEY_MAP[inputEvent]()
            except KeyError:
                pass

    def checkButtonBounds(self, pos):
        print("Checking Bounds")
        for button in self.cGamestate.buttons:
            if button.checkBounds(pos):
                return

        print("no button pressed")
        try:
            self.cGamestate.buttonNotPressed()
        except AttributeError:
            pass
            
        

    # method for showing chat overlay
    def showChat(self):

        self.chatToggle = not self.chatToggle
        pygame.display.set_mode((300,300))
        print("Toggled Chat")
        return

    def showExtendedChat(self):

        self.chatToggle = not self.chatToggle
        print("Toggled Extended Chat")
        return

    def screenshot(self):

        # save a screenshot into the screenshots folder
        print("Saved a Screenshot")
        return
        
        

        


     

        
