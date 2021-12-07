import pygame
from UiObjects import FLAGS as flags
import os

class UidGenerator:

    def __init__(self, UID_LENGTH=6):

        self.UID_LENGTH = UID_LENGTH

        self._usableIds = [str(1).zfill(self.UID_LENGTH)]

    def getNextId(self):

        nextId = self._usableIds.pop()
        if not self._usableIds:
            self._usableIds.append(str(int(nextId)+1).zfill(self.UID_LENGTH))
        return nextId

    def returnId(self, _id):

        self._usableIds.append(_id)
        

class UiHandler:

    def __init__(self):

        self.ID_GEN = UidGenerator()

        # self._components[flags.COMPONENT] = {id:component}
        self._components = [{} for flag in flags]

        self.defaultTexture = pygame.image.load(os.path.join("c:/Users/Joe/Documents/GitHub/pyOsuV3/UiManager/","assets", "ape.jpg")).convert()

        self.eventMap ={
            pygame.MOUSEBUTTONUP:self.onMouseRelease,
            pygame.MOUSEBUTTONDOWN:self.onMousePress

        }

        self.lastMousePos = pygame.mouse.get_pos()
        self.activeMouseComponent = None

    """
    Adds a basic element to the UI
    imageUrl: url of image to display
    postion: tuple containing (x,y)
    customRect: used for scaling
    SHOW: used for default showing status
    """
    def addElement(self, imageUrl, position, customRect=None, SHOW=1):

        # generate an id for the element
        newId = self.ID_GEN.getNextId()
        
        #try and load the image provided
        try:
            image = pygame.image.load(imageUrl).convert()
        except FileNotFoundError:
            # if the image cant be found, use the default texture if no custom size is set
            if not customRect:
                image = self.defaultTexture
            # else resize the default texture to the correct size
            else:
                image = pygame.image.transform(self.defaultTexture, (customRect.w, customRect.h))

        # add the render component for rednering the ui object
        self._components[flags.UX_RENDER].update({newId:[image,position,SHOW]})
        # add the position element for detecting collisions
        self._components[flags.UX_POS].update({newId:image.get_rect()})
        
    
        # return the new Id to the user so they can manipulate the element later
        return newId
    

    def handleEvent(self, pygameEvent):

        eventType = pygameEvent.type
        if eventType in self.eventMap:
            self.eventMap[eventType]()
        


    def addEvent(self, _id, eventFlag, eventData):

        if eventFlag not in flags:
            return
        
        self._components[eventFlag].update({_id:eventData})
    

    def render(self, surface):

        for _object in self._components[flags.UX_RENDER].values():
            if _object[2]:
                surface.blit(_object[0], _object[1])

    def update(self):
        
        if self.checkMouseMove():
            self.getActiveMouseComponent()
            self.onMouseMove()
        
        
    """ -------------- FUNCTIONS TO DO WITH MOUSE INPUT HANDLING -----------------"""
    def onMousePress(self):
        pass

    def onMouseRelease(self):
        if self.activeMouseComponent and self.activeMouseComponent in self._components[flags.UX_ONCLICK]:
            self._components[flags.UX_ONCLICK][self.activeMouseComponent]()

    def onMouseMove(self):
        pass

    def checkMouseMove(self):
        mousePos = pygame.mouse.get_pos()
        if mousePos == self.lastMousePos:
            return False
        else:
            self.lastMousePos = mousePos
            return True
    
    """
    Gets the current component that is applicable to mouse functions
    """
    def getActiveMouseComponent(self):
        # get the current mouse position
        currentMousePos = pygame.mouse.get_pos()
        # referenece to the position components
        tempPositionComponents = self._components[flags.UX_POS]

        # iterate through the key,value pair objects 
        for objectId, _object in tempPositionComponents.items():
            # if the mouse position is within the current mouse position
            if _object.collidepoint(currentMousePos):
                # set the active mouse component
                self.activeMouseComponent = objectId
                return

        self.activeMouseComponent = None
    


    """ --------------------------------------------------------------------------"""

