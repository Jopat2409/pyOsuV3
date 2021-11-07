
import pygame
import config


class uiGroup:

    def __init__(self, SHOWN=True, alpha=0, position=(0,0), dimensions=config.SCREEN_RESOLUTION):

        # determines wether or not a group is visible
        self.SHOWN = SHOWN
        # array of UiElements
        self.containedElements = []
        # position that the UI griup will be blitted to
        self.position = position
        # dimensions of the UI group
        self.dimensions = dimensions
    

    def render(self, window):


        for element in self.containedElements:
            element.render(window)




""" Class for managing the creation of UIs for pygame v2 """
class uiManager:

    def __init__(self, flags=None, mainTheme=None):

        # speicifies the json file that is used for colours
        self.theme = mainTheme
        
        # sets the flags for the UI manager
        self.flags = flags
        self.flagMap = {pygame.MOUSEBUTTONUP:"CLICKABLE"}

        self.eventHandleFunct = {"CLICKABLE": self.handlePresses}


        # dict containing all of the user-defined groups - format {groupID:Group instance}
        self.elementGroups = {"default":uiGroup(SHOWN=True, alpha=0)}

    def handlePresses(self, elementGroup):
        mousePos = pygame.mouse.get_pos()
        for element in elementGroup:
            if element.relativeRect.collidepoint(mousePos):
                element.function()
                return

 
    """ Create a group that elements can be added to. """
    def createGroup(self, group, alpha=0, shownOnCreation=True):
        if group in self.elementGroups:
            print("A group with that name already exists")
            return
        # creates group with corresponding ID, alpha etc
        tempGroup = uiGroup(alpha=alpha, SHOWN=shownOnCreation)
        self.elementGroups.update({group:tempGroup})

    """ Add an element to a specified group / the default layer if no group is specified"""
    def addElement(self, element, group="default"):
        try:
            self.elementGroups[group].containedElements.append(element)
        except KeyError:
            print("A group with that name does not exist")
        
        for group in self.elementGroups:
            for element_ in self.elementGroups[group].containedElements:
                print(f"{group} contains {element_}")
        return element
    
    def showGroup(self, group):
        self.elementGroups[group].SHOWN = True
    
    def hideGroup(self, group):
        self.elementGroups[group].SHOWN = False

    def render(self, window):

        for group in self.elementGroups:
            tempGroup = self.elementGroups[group]
            if not tempGroup.SHOWN:
                continue
            tempGroup.render(window)
        
    

    def handleEvents(self, event):
        elementsToHandle = []
        try:
            tempFlag = self.flagMap[event]
        except KeyError:
            return
        for group in self.elementGroups:
            if not self.elementGroups[group].SHOWN:
                continue
            elementsToHandle += [i for i in self.elementGroups[group].containedElements if tempFlag in i.flags]
        
        self.eventHandleFunct[tempFlag](elementsToHandle)
    
            




