""" ---------- OSU MODULES ---------- """
import config                               # for program global variables

""" ---------- PYTHON MODULES ---------- """
import os                                   # for joining directories
import ctypes                               # for btypassing windows' UI scaling
from win32api import GetSystemMetrics       # for getting system resolution
import logging                              # for logging errors 
import sys
import glob                                 # for finding cfg file 
from shutil import copyfile                 # for copying cfg file

"""
This class is for the initialization of the game, setting default variables settings
Since it is only ever called once there is no point in having it be a gamestate
"""


# loads the user's saved settings from their config file
def loadSettings():

    if not os.path.isfile("%s/osu!.cfg"%config.DEFAULT_PATH):
        # get the path of the user's local installation file
        osuPath = os.path.join(os.getenv('LocalAppData'), "osu!")
        # check if it exists, if not then exit as we cannot extract the needed data
        if not os.isdir(osuPath):
            print("Cannot find a local installation of osu!.... ending program.")
            sys.exit(0)
        # loop through config files in the osu local path
        for file in glob.glob(os.join(osuPath, "*.cfg")):
            # copy the first cfg file found to "osu!.cfg" then break out of the for loop
            copyfile(os.join(osuPath, file), os.join(config.DEFAULT_PATH, "osu!.cfg"))
            break
        

    # loop through all lines in the config file
    with open("%s/osu!.cfg"%config.DEFAULT_PATH, "r", encoding='utf-8') as f:
        for line in f:
            # split the line into a list laid out in the form ["setting", "value"]
            cLine = line.split("=")
            if len(cLine) != 1:
                # if the line starts with "key" then it is a key binding which is saved in a different dictionary called keyBindings
                if cLine[0].startswith("key"):
                    # checks to see if the key already has a function attached to it. If it does, it appends it to the list of functions
                    # this is due to keys doing different things in different gamestates
                    if cLine[1].strip() in config.keyBindings:
                        config.keyBindings[cLine[1].strip()].append(cLine[0].strip())
                    else:  
                        config.keyBindings.update({cLine[1].strip():[cLine[0].strip()]})
                # if the line does not contain a key binding, put it into the currentSettings dictionary
                else:
                    config.currentSettings.update({cLine[0].strip():cLine[1].strip()})
    # set the scaling value which is used to scale osuPixel values
    config.CURRENT_SCALING = getOsuPixelScaling()
    config.SCALED_RESOLUTION = (int(config.DEFAULT_RESOLUTION[0]*config.CURRENT_SCALING), int(config.DEFAULT_RESOLUTION[1]*config.CURRENT_SCALING))
    #print(config.SCREEN_RESOLUTION)
    #print(config.CURRENT_SCALING)


def getOsuPixelScaling():

    # get the scale factor between the current height and the default height (480)
    cScale = (config.SCREEN_RESOLUTION[1]-100) / config.DEFAULT_RESOLUTION[1]
    # check to make sure that scaling to this height would not cause the beatmap pane to bleed over the edge of the screen
    if (cScale * config.DEFAULT_RESOLUTION[0]) > config.SCREEN_RESOLUTION[0]:
        # update the cScale if that would be a problem
        cScale = config.SCREEN_RESOLUTION / config.DEFAULT_RESOLUTION[0]
    #print("OsuPixelScale: " + str(cScale))
    return cScale




def startGame():

    try:
        import pygame
        if(pygame.version.vernum[0]) < 2:
            print("You do not have the correct version of pygame installed, try installing pygame 2 and try again")
            return
    except ModuleNotFoundError:
        print("You do not have pygame installed. Terminating program...")
        return
    pygame.init()
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    # create the logger that will be used throught the program
    logging.basicConfig(filename='log.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    # prevent the program from scaling due to windows default UI scaling
    ctypes.windll.user32.SetProcessDPIAware()
    # set osu's default resolution
    config.DEFAULT_RESOLUTION = (640, 480)
    # get the base install path of the program
    config.DEFAULT_PATH = os.path.dirname(os.path.realpath(__file__))
    # store the current screen resolution
    config.SCREEN_RESOLUTION = (GetSystemMetrics(0), GetSystemMetrics(1))
    print(f"The resolution of your screen is {config.SCREEN_RESOLUTION}")
    # load all the user's default settings from the osu!.cfg
    loadSettings()
    # store the working skin directory
    config.cSkinDirectory = skinFolder = os.path.join(config.DEFAULT_PATH, "skins", config.currentSettings["Skin"])
    
    
    
    
    # set the mouse cursor to invisible due to the program using it's own cursor
    pygame.mouse.set_visible(False)
    config.xOffset = int((config.SCREEN_RESOLUTION[0] - config.DEFAULT_RESOLUTION[0]*config.CURRENT_SCALING)/2)
    config.yOffset = 50
    #print(config.keyBindings)
    # we import maingame here as many for the links to assets will not work without being initialized first
    import MainGame
    
    # start the main program
    currentProcess = MainGame.osuGame()

    
# start the whole program if this file is directly ran
if __name__ == "__main__":
    ans = str(input("Run in safe mode? y/n "))
    if ans == "y":
        config.safeMode = True
    startGame()
