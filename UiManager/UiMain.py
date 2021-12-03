import pygame
from UiObjects import FLAGS as flags

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
        
        self._components = [{} for i in flags]
        self.idGen = UidGenerator()



    def addElement(self, renderComponent):

        newId = self.idGen.getNextId()
        
        self._components[flags.UX_RENDER].update({newId:renderComponent})
        self._components[flags.UX_POS].update({newId:renderComponent[0].get_rect()})

        self._componentHandlers = {pygame.MOUSEBUTTONDOWN:self.handleMousePress,
                                   pygame.MOUSEBUTTONUP:self.handleMouseRelease}

        return newId

    def removeElement(self, _id):

        for _componentDict in self.components:
            del _componentDict[_id]

        self.idGen.returnId(_id)

    def handleEvent(self, event):
        if event.type in self._componentHandlers:
            self._componentHandlers[event.type]()
        

    def render(self, surface):

        for renderObject in self._components[flags.UX_RENDER].values():
            if renderObject[2]:
                surface.blit(renderObject[0], renderObject[1])

    def addEvent(self, _id, eventType, function):
        
        if eventType in flags:
            eventRect = self._components[flags.UX_POS][_id]
            self._components[eventType].update({_id:[eventRect,function]})
    def handleMouseEvent(self, uxElement):
        mPos = pygame.mouse.get_pos()
        for _object in self._components[uxElement].values():
            if _object[0].collidepoint(mPos):
                _object[1]
            

    def handleMouseRelease(self):
        self.handleMouseEvent(flags.UX_ONCLICK)

    def handleMousePress(self):
        mPos = pygame.mouse.get_pos()
        pass

    def update(self):
        self.handleMouseMove(self)

    def handleMouseMove(self):

        self.handleMouseEvent(flags.UX_ONHOVER)
        
