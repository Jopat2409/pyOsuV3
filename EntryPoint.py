import config
import os
import ctypes
from win32api import GetSystemMetrics
import glob

"""
This class is for the initialization of the game, setting default variables settings
Since it is only ever called once there is no point in having it be a gamestate
"""


def loadSettings():

    with open("%s/osu!.cfg"%config.DEFAULT_PATH, "r", encoding='utf-8') as f:
        for line in f:
            cLine = line.split("=")
            if len(cLine) != 1:
                if cLine[0].startswith("key"):
                    if cLine[1].strip() in config.keyBindings:
                        config.keyBindings[cLine[1].strip()].append(cLine[0].strip())
                    else:  
                        config.keyBindings.update({cLine[1].strip():[cLine[0].strip()]})
                else:
                    config.currentSettings.update({cLine[0].strip():cLine[1].strip()})
    config.CURRENT_SCALING = getOsuPixelScaling()
    print(config.SCREEN_RESOLUTION)
    print(config.CURRENT_SCALING)


def getOsuPixelScaling():

    cScale = config.SCREEN_RESOLUTION[1] / config.DEFAULT_RESOLUTION[1]
    if (cScale * config.DEFAULT_RESOLUTION[0]) > config.SCREEN_RESOLUTION[0]:
        cScale = config.SCREEN_RESOLUTION / config.DEFAULT_RESOLUTION[0]
    #print("OsuPixelScale: " + str(cScale))
    return cScale




def startGame():
    ctypes.windll.user32.SetProcessDPIAware()
    config.DEFAULT_RESOLUTION = (640, 480)
    config.DEFAULT_PATH = os.path.dirname(os.path.realpath(__file__))
    config.SCREEN_RESOLUTION = (GetSystemMetrics(0), GetSystemMetrics(1))
    print("path:" + os.path.dirname(os.path.realpath(__file__)))
    # load all the user's default settings from the osu!.cfg
    loadSettings()
    # prevent the program from scaling due to windows default UI scaling
    
    # pygame v2 or higher is needed for a lot of the functions within this program
    try:
        import pygame
        if(pygame.version.vernum[0]) < 2:
            print("You do not have the correct version of pygame installed")
            return
    except ModuleNotFoundError:
        print("You do not have pygame installed you dummy")
        return
    
    pygame.init()
    pygame.mouse.set_visible(False)
    print(config.keyBindings)
    # we import maingame here as many for the links to assets will not work without being initialized first
    import MainGame
    currentProcess = MainGame.osuGame()

    

    




startGame()
