

DEFAULT_PATH = ""
CURRENT_SCALING = 1
xOffset = 0
yOffset = 0
keyBindings = {}
currentSettings = {}

safeMode = False

useOsuTextures = True

currentMods = []



"""
Allows creation of unique identifiers for objects
Allows for the repurposing of identifiers that have gone out of scope
NOTE not currently used but could see use in the UI 
"""
class idGenerator:



    def __init__(self):

        self.idStack = [0]


    def returnID(self, ID):

        self.idStack.append(ID)

    def getID(self):

        if len(self.idStack) == 1:
            value = self.idStack.pop()
            self.idStack.append(value+1)
            return value
        else:
            return self.idStack.pop()

    def resetGenerator(self):

        self.idStack = [0]

idGen = idGenerator()

""" COLORS """

bmFrame = {"ComboColor":(255,255,255)}

WHITE = (255,255,255)
PINK  = (255,102,170)
BLUE = (0,0,255)
