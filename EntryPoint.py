""" ---------- OSU MODULES ---------- """
import config

""" ---------- PYTHON MODULES ---------- """
import os
import ctypes
from win32api import GetSystemMetrics
import glob


"""
This class is for the initialization of the game, setting default variables settings
Since it is only ever called once there is no point in having it be a gamestate
"""


# loads the user's saved settings from their config file
def loadSettings():

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
    cScale = config.SCREEN_RESOLUTION[1] / config.DEFAULT_RESOLUTION[1]
    # check to make sure that scaling to this height would not cause the beatmap pane to bleed over the edge of the screen
    if (cScale * config.DEFAULT_RESOLUTION[0]) > config.SCREEN_RESOLUTION[0]:
        # update the cScale if that would be a problem
        cScale = config.SCREEN_RESOLUTION / config.DEFAULT_RESOLUTION[0]
    #print("OsuPixelScale: " + str(cScale))
    return cScale




def startGame():

    # prevent the program from scaling due to windows default UI scaling
    ctypes.windll.user32.SetProcessDPIAware()
    # set osu's default resolution
    config.DEFAULT_RESOLUTION = (640, 480)
    # get the base install path of the program
    config.DEFAULT_PATH = os.path.dirname(os.path.realpath(__file__))
    # store the current screen resolution
    config.SCREEN_RESOLUTION = (GetSystemMetrics(0), GetSystemMetrics(1))
    #print("path:" + os.path.dirname(os.path.realpath(__file__)))
    # load all the user's default settings from the osu!.cfg
    # pygame v2 or higher is needed for a lot of the functions within this program
    # no pygame, no run
    try:
        import pygame
        if(pygame.version.vernum[0]) < 2:
            print("You do not have the correct version of pygame installed")
            return
    except ModuleNotFoundError:
        print("You do not have pygame installed. Terminating program...")
        return
    loadSettings()
    
    
    
    
    pygame.init()
    # set the mouse cursor to invisible due to the program using it's own cursor
    pygame.mouse.set_visible(False)
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
