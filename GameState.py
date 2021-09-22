""" ---------- OSU MODULES ---------- """
import MainMenu
import config
import SoundHandler

""" ---------- PYTHON MODULES ---------- """
import queue
import pygame
import pygame.gfxdraw
import ctypes
import pickle
import copy
import traceback




# manages the current gamestate of the game
class gameStateManager:


    def __init__(self):


        # sets the initial gamestate to the main menu
        self.cGamestate = MainMenu.gsMenu(self)
        # creates the stack used for storing paused gamestates
        self.gsStack = queue.LifoQueue()
        # prevents the program from displaying the wrong res due to windows UI scaling
        ctypes.windll.user32.SetProcessDPIAware()

        # key functions that are applicable to all gamestates
        self.GLOBAL_KEY_MAP = {"keyToggleChat":self.showChat,
                               "keyToggleExtendedChat":self.showExtendedChat,
                               "keyScreenshot":self.screenshot}

        # tracks wether chat is toggled ( applicable to all gamestates )
        self.chatToggle = False

        # inializes the sound handler
        self.soundStream = SoundHandler.audioStream()

        self.font = pygame.cFont = pygame.font.SysFont('Arial', 40)

        # uses fullscreen width if in fullscreen        
        if int(config.currentSettings["Fullscreen"]) == 1:
            self.window = pygame.display.set_mode((int(config.currentSettings["WidthFullscreen"]), int(config.currentSettings["HeightFullscreen"])))
            pygame.display.toggle_fullscreen()
        else:
            self.window = pygame.display.set_mode(config.SCREEN_RESOLUTION)


    """hashes all relevant info about a gamestate, should be used when the time between resuming the gamestate is relatively large, or if the new gamestate
    requires a larger amount of processing power / memory
    """
    def suspendGamestate(self, NEW_GAMESTATE):
        # creates an obj file using the gamestate's UUID 
        filePath = config.DEFAULT_PATH + "/" + "%s.obj"%self.cGamestate.UUID
        # opens the file
        file = open(filePath, 'w')
        tempGstate = copy.deepcopy(self.cGamestate)
        # uses pickle to write the gamestate to the file
        pickle.dump(tempGstate, file)
        # adds the UUID to the stack
        self.gsStack.put(filePath)
        # deletes the gamestate and updates the cGamestate
        del(self.cGamestate,tempGstate)
        self.cGamestate = NEW_GAMESTATE


    """simply puts all the info to one side but keeps it stored within the program. Should be used for when the time between resuming is likely to be relatively short
    """
    def pauseGamestate(self, NEW_GAMESTATE):

        # add the last gamestate to the stack
        self.gsStack.put(self.cGamestate)
        del(self.cGamestate)
        self.cGamestate = NEW_GAMESTATE


    """ Completely changes the gamestate, removing all information about the previous one"""
    def newGamestate(self, NEW_GAMESTATE):

        del(self.cGamestate)
        self.cGamestate = NEW_GAMESTATE
    
    """ delete the current gamestate and bring the last paused gamestate back to the current gamestate"""
    def resumeGamestate(self):

        # gets the last paused gamestate
        tempGamestate = self.gsStack.pop()
        # if the tempGamestate is a string then it must be a UUID, signifying a cached gamestate
        if tempGamestate.isinstance(str):
            # load the gamestate back up from the file
            filePath = config.DEFAULT_PATH + "/" + "%s.obj"%tempGamestate
            del(self.cGamestate)
            self.cGamestate = pickle.load(filePath)
            
        else:
            del(self.cGamestate)
            self.cGamestate = tempGamestate


    def update(self):

        # update current gamestate
        self.cGamestate.update()
            

    def render(self, interpolation, frames):

        # blit the frame returned by the current gamestate's render method onto the main window
        self.window.blit(self.cGamestate.getRenderSnapshot(interpolation), (0,0))
        # draw the chat popup if it is enabled
        if self.chatToggle:
            pygame.draw.rect(self.window,(0,0,0),(200,150,100,50))
            
        # render the cursor at the current mouse position
        mX, mY = pygame.mouse.get_pos()
        pygame.gfxdraw.filled_circle(self.window, mX, mY, 20, (255,255,0))
        if frames >= 60:
            color = (0,255,0)
        else:
            color = (255,0,0)
        fps = self.font.render("{}".format(frames), True, color)
        self.window.blit(fps, (500,1000))
        # update the display
        pygame.display.update()


    def mapInput(self, inputs):

        # loop through all of the key inputs
        for inputEvent in inputs:
            #print(inputEvent)
            
            try:
                # check the global key table for any functions to be called
                self.GLOBAL_KEY_MAP[inputEvent]()
                # check the current gamestate key table for functions to be called

            except KeyError:
                pass

            try:
                self.cGamestate.KEY_MAP[inputEvent]()
            except KeyError:
                pass

    def checkButtonBounds(self, pos):
        #print("Checking Bounds")
        for button in self.cGamestate.buttons:
            if button.checkBounds(pos):
                return

        #print("no button pressed")
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
        
        

        


     

        
