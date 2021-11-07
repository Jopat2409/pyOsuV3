
import pygame



class horizontalSlider:

    
    def __init__(self, relativeRect, width, manager, start_value = 0, end_value = 100, flags=[]):

        # starting value of the slider
        self.startValue = start_value
        # ending value of the slider
        self.endValue = end_value

        self.rect = relativeRect

        self.flags = ["DRAGABLE"]

        self.loadThemes()
        self.dimensions = (self.rect.w, self.rect.h)

        self.startCoords = [self.rect.topLeft[0], self.rect.centery]
        self.endCoords = [self.rect.topLeft[0] + self.dimensions[0], self.rect.centery]

        self.parentManager = manager

        # initialize the current value to halfway accross the slider
        self.currentValue = int((start_value + end_value) / 2)

        
    
    def loadThemes(self):

        if self.parentManager.theme == None:
            self.attributes = {"sliderBodyColor": (255,255,255),
            "sliderThickness":5,
            "sliderHeadColor":(0,0,255),
            "sliderHeadThickness":20}
            
    

    def render(self, window):

        pygame.draw.line(window, self.attributes["sliderBodyColor"], self.startCoords, self.endCoords, self.attributes["sliderThickness"])
        linePos = int(self.startCoords[0] + self.width*(self.cValue / (self.endValue - self.startValue)))
        pygame.draw.circle(window, self.attributes["sliderHeadColor"], (linePos, self.startCoords[1]), self.attributes["sliderHeadThickness"], 0)
        


class Image:


    def __init__(self, imgSrc, relativeRect, flags=[], funct=None):

        self.function = funct
        self.relativeRect = relativeRect
        self.dimensions = (self.relativeRect.w, self.relativeRect.h)
        self.flags = flags
        self.IMG =  pygame.image.load(imgSrc).convert_alpha()
        self.IMG = pygame.transform.scale(self.IMG, self.dimensions)
        

        
    

    def render(self, window):
        window.blit(self.IMG, (self.relativeRect[0], self.relativeRect[1]))


class Button:


    def __init__(self, relativeRect, text, funct, manager):

        self.relativeRect = relativeRect
        self.dimensions = (self.relativeRect.w, self.relativeRect.h)
        self.function = funct
        self.parentManager = manager
        self.loadThemes()

        self.flags = ["CLICKABLE"]
        

        self.font = pygame.font.SysFont('Arial', 25)

        self.buttonText = self.font.render(text, True, self.attributes["fontColor"])

        self.fTopLeft = (int(self.relativeRect.centerx - (self.buttonText.get_width() / 2)), int(self.relativeRect.centery - (self.buttonText.get_height() / 2)))


    def loadThemes(self):
        
        if self.parentManager.theme == None:
            self.attributes = {"fontColor": (255,255,255),
            "fontSize":0.5,
            "borderColor":(0,0,0),
            "bgColor":(100,100,100),
            "bgColor.hover":(150,150,150)}
    
    def render(self, window):

        
        pygame.draw.rect(window, self.attributes["bgColor"], self.relativeRect)
        pygame.draw.rect(window, self.attributes["borderColor"], self.relativeRect, 5)
        window.blit(self.buttonText, self.fTopLeft)