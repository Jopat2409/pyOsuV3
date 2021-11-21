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
import logging
import SkinLoader


"""
Class that handles and runs all of the functions and classes associated with the current gamestate
All gamestates must contain at the least, a render, update and mapInput function
"""
class gameStateManager:

    def __init__(self):

        # creates the stack used for storing paused gamestates
        self.gsStack = queue.LifoQueue()
        # key functions that are applicable to all gamestates
        self.GLOBAL_KEY_MAP = {"keyToggleChat":self.showChat,
                               "keyToggleExtendedChat":self.showExtendedChat,
                               "keyScreenshot":self.screenshot}
        # tracks whether chat is toggled ( applicable to all gamestates )
        self.chatToggle = False
        # works out the size in pixels of the cursor, based off of the CursorSize setting in .cfg
        self.cursorSize = int(100 * float(config.currentSettings["CursorSize"]))

        # uses fullscreen width if in fullscreen        
        if int(config.currentSettings["Fullscreen"]) == 1:
            # DOUBLEBUF for fluid rendering, FULLSCREEN for fullscreen, HWSURFACE for GPU rendering, SRCALPHA for alpha pixels
            self.window = pygame.display.set_mode(config.SCREEN_RESOLUTION, pygame.DOUBLEBUF | pygame.FULLSCREEN | pygame.HWSURFACE | pygame.SRCALPHA, 32 )
        else:
            # DOUBLEBUF for fluid rendering, HWSURFACE for GPU rendering, SRCALPHA for alpha pixels
            self.window = pygame.display.set_mode(config.SCREEN_RESOLUTION, pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.SRCALPHA, 32 )

        # prevents the program from displaying the wrong res due to windows UI scaling
        ctypes.windll.user32.SetProcessDPIAware()
        # initializes the default font
        self.font = pygame.cFont = pygame.font.SysFont('Arial', 40)
        # inializes the sound handler
        self.soundStream = SoundHandler.audioStream()
        # sets the initial gamestate to the main menu
        self.cGamestate = MainMenu.gsMenu(self)

    def setUiManager(self, uiManager):
        self.uiManager = uiManager

    """
    hashes all relevant info about a gamestate, should be used when the time between resuming the gamestate is relatively large, or if the new gamestate
    requires a larger amount of processing power / memory
    """
    def suspendGamestate(self, NEW_GAMESTATE):
        # creates an obj file using the gamestate's UUID 
        filePath = config.DEFAULT_PATH + "/" + "%s.obj"%self.cGamestate.UUID
        # opens the file
        file = open(filePath, 'w')
        # create a copy of the gamestate to save
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
        tempGamestate = self.gsStack.get()
        # if the tempGamestate is a string then it must be a UUID, signifying a cached gamestate
        if isinstance(tempGamestate, str):
            # load the gamestate back up from the file
            filePath = config.DEFAULT_PATH + "//" + "%s.obj"%tempGamestate
            del(self.cGamestate)
            self.cGamestate = pickle.load(filePath)
            
        else:
            del(self.cGamestate)
            self.cGamestate = tempGamestate


    def update(self):

        # update current gamestate
        self.cGamestate.update()
            
    """
    Draws everything that needs to be drawn to the surface then updates the screen
    """
    def render(self, interpolation, frames):

        # draw the current gamestate onto the main menu
        self.cGamestate.getRenderSnapshot(interpolation, self.window)
        # draw the chat popup if it is enabled
        if self.chatToggle:
            pygame.draw.rect(self.window,(0,0,0),(200,150,100,50))
            
        # render the UI
        self.uiManager.render(self.window)
        # set the fps indicator color to green if frames are above 60
        color = (0,255,255) if frames >= 60 else (255,0,0)
        # create the fps count surface
        fps = self.font.render("{}".format(frames), True, color)
        # draw the fps count to the bottom left of the screen
        self.window.blit(fps, (config.SCREEN_RESOLUTION[0]-fps.get_width(),config.SCREEN_RESOLUTION[1]-fps.get_height()))

        # render the cursor at the current mouse position
        mX, mY = pygame.mouse.get_pos() # get the position of the cursor
        mX -= self.cursorSize / 2       # factor in the cursor radius
        mY -= self.cursorSize / 2       # ""
        # blit the cursor to the x and y calculated 
        self.window.blit(SkinLoader.imageMap["cursor"], (mX, mY))
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
                logging.warning(traceback.format_exc())

            try:
                self.cGamestate.KEY_MAP[inputEvent]()
            except KeyError:
                logging.warning(traceback.format_exc())

    def checkButtonBounds(self, pos):
        #print("Checking Bounds")
        for button in self.cGamestate.buttons:
            if button.checkBounds(pos):
                return

        #print("no button pressed")
        try:
            self.cGamestate.buttonNotPressed()
        except AttributeError:
            logging.warning(traceback.format_exc())
            
        

    # method for showing chat overlay
    def showChat(self):
        print("Shown Chat")
        self.chatToggle = not self.chatToggle
        if not self.chatToggle:
            self.uiManager.hideGroup("ChatWindow")
        else:
            self.uiManager.showGroup("ChatWindow")

    def showExtendedChat(self):

        self.chatToggle = not self.chatToggle
        print("Toggled Extended Chat")
        return

    def screenshot(self):

        # save a screenshot into the screenshots folder
        print("Saved a Screenshot")
        return
        
        

        


     

        
