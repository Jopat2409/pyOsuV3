""" ---------- OSU MODULES ---------- """
import MainMenu  # for creating the initial gamestate
import config  # for accessing program-global variables
import SoundHandler  # for handling sound

""" ---------- PYTHON MODULES ---------- """
import queue  # for implementing the gamestate stack
import pygame  # for rendering and audio
import pygame.gfxdraw  # for anti-aliased rendering
import ctypes  # for bypassing windows UI scaling
import pickle  # for serializing gamestates
import copy  # for creating actual copies of gamestates
import traceback  # for getting error log
import logging  # for logging purposes


class gameStateManager:
    """
    Class that handles and runs all the functions and classes associated with the current gamestate
    All gamestates must contain at the least, a render, update and mapInput function
    """

    def __init__(self, ):

        # creates the stack used for storing paused gamestates
        self.gsStack = queue.LifoQueue()
        # prevents the program from displaying the wrong res due to windows UI scaling
        ctypes.windll.user32.SetProcessDPIAware()
        # key functions that are applicable to all gamestates
        self.GLOBAL_KEY_MAP = {"keyToggleChat": self.showChat,
                               "keyToggleExtendedChat": self.showExtendedChat,
                               "keyScreenshot": self.screenshot}
        # tracks wether chat is toggled ( applicable to all gamestates )
        self.chatToggle = False
        # calculate the size of the cursor based on the user's cursor size
        self.cursorSize = int(100 * float(config.currentSettings["CursorSize"]))

        # uses fullscreen width if in fullscreen        
        if int(config.currentSettings["Fullscreen"]) == 1:
            # flags - DOUBLEBUF for smoother rendering, FULLSCREEN for fullscreen, HWSURFACE for GPU rendering,
            # SRCALPHA for alpha pixel values
            self.window = pygame.display.set_mode(config.SCREEN_RESOLUTION, pygame.DOUBLEBUF |
                                                  pygame.FULLSCREEN | pygame.HWSURFACE | pygame.SRCALPHA, 32)
        else:
            # flags - DOUBLEBUF for smoother rendering, FULLSCREEN for fullscreen, HWSURFACE for GPU rendering,
            # SRCALPHA for alpha pixel values
            self.window = pygame.display.set_mode(config.SCREEN_RESOLUTION, pygame.DOUBLEBUF
                                                  | pygame.FULLSCREEN | pygame.HWSURFACE | pygame.SRCALPHA, 32)

        # inializes the sound handler
        self.soundStream = SoundHandler.audioStream()
        # initialize the sound handler
        self.font = pygame.cFont = pygame.font.SysFont('Arial', 40)
        # sets the initial gamestate to the main menu
        self.cGamestate = MainMenu.gsMenu(self)

    def suspendGamestate(self, NEW_GAMESTATE):
        """
        Hashes all relevant info about a gamestate, should be used when the time between resuming the gamestate is
        relatively large, or if the new gamestate Requires a larger amount of processing power / memory
        """
        # creates an obj file using the gamestate's UUID 
        filePath = f"{config.DEFAULT_PATH}/{self.cGamestate.UUID}.obj" + "/" + "%s.obj"
        # opens the file
        file = open(filePath, 'w')
        # create a copy of the gamestate to save
        tempGstate = copy.deepcopy(self.cGamestate)
        # uses pickle to write the gamestate to the file
        pickle.dump(tempGstate, file)
        # adds the UUID to the stack
        self.gsStack.put(filePath)
        # deletes the gamestate and updates the cGamestate
        del (self.cGamestate, tempGstate)
        self.cGamestate = NEW_GAMESTATE

    def pauseGamestate(self, NEW_GAMESTATE):
        """
        Simply puts all the info to one side but keeps it stored within the program. Should be used for when the time
        between resuming is likely to be relatively short
        """
        # add the last gamestate to the stack
        self.gsStack.put(self.cGamestate)
        del self.cGamestate
        self.cGamestate = NEW_GAMESTATE

    def newGamestate(self, NEW_GAMESTATE):
        """
        Completely changes the gamestate, removing all information about the previous one
        """
        del self.cGamestate
        self.cGamestate = NEW_GAMESTATE

    def resumeGamestate(self):
        """
        Delete the current gamestate and bring the last paused gamestate back to the current gamestate
        """
        # gets the last paused gamestate
        tempGamestate = self.gsStack.get()
        # if the tempGamestate is a string then it must be a UUID, signifying a cached gamestate
        if isinstance(tempGamestate, str):
            # load the gamestate back up from the file
            filePath = config.DEFAULT_PATH + "//" + "%s.obj" % tempGamestate
            del self.cGamestate
            self.cGamestate = pickle.load(filePath)

        else:
            del self.cGamestate
            self.cGamestate = tempGamestate

    def update(self):

        # update current gamestate
        self.cGamestate.update()

    def render(self, interpolation, frames):
        """
        Draws everything that needs to be drawn to the surface then updates the screen
        """
        # draw the current gamestate onto the main window
        self.cGamestate.getRenderSnapshot(interpolation, self.window)

        # set the fps indicator color to green if frames are above 60
        color = (0, 255, 255) if frames >= 60 else (255, 0, 0)
        # create the fps count surface
        fps = self.font.render("{}".format(frames), True, color)
        # draw the fps count to the bottom left of the screen
        self.window.blit(fps, (config.SCREEN_RESOLUTION[0] - fps.get_width(),
                               config.SCREEN_RESOLUTION[1] - fps.get_height()))

        # render the cursor at the current mouse position
        mX, mY = pygame.mouse.get_pos()  # get the position of the cursor

        pygame.gfxdraw.filled_circle(self.window, mX, mY, 20, (255, 255, 0))

        # update the display
        pygame.display.update()

    """
    Function to map inputs to gamestate-specific functions
    """

    def mapInput(self, inputs):

        # loop through all the key inputs
        for inputEvent in inputs:
            # print(inputEvent)
            try:
                # check the global key table for any functions to be called
                self.GLOBAL_KEY_MAP[inputEvent]()
                # check the current gamestate key table for functions to be called
            except KeyError:
                # warn the log that the key does not exist
                logging.warning(traceback.format_exc())

            try:
                # check the gamestate specific keymap for any events
                self.cGamestate.KEY_MAP[inputEvent]()
            except KeyError:
                # warn the log that the key does not exist
                logging.warning(traceback.format_exc())

    def checkButtonBounds(self, pos):

        for button in self.cGamestate.buttons:
            if button.checkBounds(pos):
                return
        try:
            self.cGamestate.buttonNotPressed()
        except AttributeError:
            logging.warning(traceback.format_exc())

    # method for showing chat overlay
    def showChat(self):
        print("Shown Chat")
        self.chatToggle = not self.chatToggle

    def showExtendedChat(self):

        self.chatToggle = not self.chatToggle
        print("Toggled Extended Chat")
        return

    def screenshot(self):
        # save a screenshot into the screenshots folder
        print("Saved a Screenshot")
        return
