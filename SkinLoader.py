from pygame import image
import config
import pygame
import os

global currentSkinDirectory
currentSkinDirectory = skinFolder = os.path.join(config.DEFAULT_PATH, "skins", config.currentSettings["Skin"])
print(currentSkinDirectory)



def loadImageMaps():
    # image map will be used to store all images needed in every gamestate, for example cursor, profile picture etc
    global currentSkinDirectory
    global imageMap
    cursor = pygame.image.load(os.path.join(currentSkinDirectory, "cursor@2x.png"))
    cWidth = int(cursor.get_width() * float(config.currentSettings["CursorSize"]))
    imageMap = {"cursor":pygame.transform.scale(cursor, (cWidth, cWidth))}

    # used for all the images needed in a particular gamestate. When the gamestate is ended, a temp file will be saved with the dict stored so loading is much quicker
    global stateMap
    stateMap = {}

    global beatmapMap
    beatmapMap = {}

def loadBeatmapImages():

    global currentSkinDirectory
    tempImgMap = {}

    tempImgMap.update({"pauseBack":pygame.image.load(os.path.join(currentSkinDirectory, "Pause-back@2x.png")).convert(),
                        "pauseRetry":pygame.image.load(os.path.join(currentSkinDirectory, "Pause-retry@2x.png")).convert(),
                        "pauseContinue":pygame.image.load(os.path.join(currentSkinDirectory, "Pause-continue@2x.png")).convert(),
                        "pauseOverlay":pygame.transform.scale(pygame.image.load(os.path.join(currentSkinDirectory, "pause-overlay@2x.png")).convert_alpha(),config.SCREEN_RESOLUTION),
                        "playOverlay":pygame.transform.scale(pygame.image.load(os.path.join(currentSkinDirectory, "scorebar-bg@2x.png")).convert_alpha(),config.SCREEN_RESOLUTION)})
    
    global beatmapMap
    beatmapMap.update({"approachCircle":pygame.image.load(os.path.join(currentSkinDirectory, "approachcircle@2x.png")),
                       "hitCircle":pygame.image.load(os.path.join(currentSkinDirectory, "hitcircle@2x.png")),
                       "hitCircleOverlay":pygame.image.load(os.path.join(currentSkinDirectory, "hitcircleoverlay@2x.png"))})
    
    global stateMap
    stateMap.update(tempImgMap)


def loadBeatmapSelectImages():

    global stateMap
    stateMap = {}

    stateMap.update({"selectOverlay":pygame.transform.scale(pygame.image.load(os.path.join(currentSkinDirectory, "selection-mode@2x.png")).convert_alpha(),config.SCREEN_RESOLUTION)})