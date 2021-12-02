
import pygame

class Image:

    def __init__(self, imagePath, x, y, function=None):
        
        self.dataObjects = {"UI_RENDER":[pygame.image.load(imagePath).convert(),(x,y)]}
        if function:
            self.dataObjects.update({"UI_FUNCPRESS":[self.dataObjects["UI_RENDER"][0].get_rect(),function]})


    def getData(self):

        return self.dataObjects
