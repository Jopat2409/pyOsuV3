

DEFAULT_PATH = ""
keyBindings = {}
currentSettings = {}



# program entity ID generation

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



WHITE = (255,255,255)
PINK  = (255,102,170)
BLUE = (0,0,255)
