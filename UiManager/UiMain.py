import pygame




class UiHandler:


    def __init__(self):

        self.flagObjects = {"UI_RENDER":[],                 # flag to render
                            "UI_FUNCPRESS":[],              # flag that allows functions to be called when pressed [rect,funct]
                            "UI_DRAG":[],                   # [rect,active=False]
                            "UI_TEXTINPUT":[]}                   

        self.activeObjects = {"UI_DRAG":None,
                              "UI_TEXTINPUT":[]}

    def update(self):
        cMousePos = pygame.mouse.get_pos()

        # update drag objects
        if not self.activeObjects["UI_DRAG"]:
            pass
        else:
            self.activeObjects["UI_DRAG"][0].center = cMousePos
            print(self.flagObjects["UI_DRAG"])

    
    def handleEvent(self, event):
        mousePos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handleButtonPress(mousePos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.handleButtonRelease(mousePos)


    def handleButtonRelease(self, eventPos):

        # loop through every mouse function object
        for _mouseObject in self.flagObjects["UI_FUNCPRESS"]:
            if _mouseObject[0].collidepoint(eventPos):
                _mouseObject[1]()
                break
        for _dragObject in self.flagObjects["UI_DRAG"]:
            if _dragObject.collidepoint(eventPos):
                _dragObject[1] = False
                self.currentActiveObjects.update({"UI_DRAG":None})


    def render(self, surface):

        for _renderObject in self.flagObjects["UI_RENDER"]:
            if isinstance(_renderObject[0], pygame.Surface):
                surface.blit(_renderObject[0], _renderObject[1])

    def handleButtonPress(self, eventPos):

        for _dragObject in self.flagObjects["UI_DRAG"]:
            if _dragObject.collidepoint(eventPos):
                _dragObject[1] = True
                _dragObject[2] = eventPos
                self.activeObjects.update({"UI_DRAG":_dragObject})
                break


    def addElement(self, uiElement):

        data = uiElement.getData()
        for flag,_object in data.items():
            try:
                self.flagObjects[flag].append(_object)
            except KeyError:
                self.flagObjects.update({flag:_object})

        
        
