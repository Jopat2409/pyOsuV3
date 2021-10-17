import config
import pygame
import pygame.gfxdraw
import BeatmapFrame






class hitCircle:


    def __init__(self, _object):

        self.x = config.xOffset + int(config.CURRENT_SCALING * int(_object[0]))
        self.y = config.yOffset + int(config.CURRENT_SCALING * int(_object[1]))
        self.timingPoint = int(_object[2])

        
    def render(self, cPos, surface):
        pygame.gfxdraw.filled_circle(surface, self.x, self.y, BeatmapFrame.circleSize, BeatmapFrame.currentComboColor)
        pygame.gfxdraw.filled_circle(surface, self.x, self.y, int(BeatmapFrame.circleSize*0.9), (0,0,0))
        aOffset = int(BeatmapFrame.circleSize + BeatmapFrame.approachCircleSize * ((self.timingPoint-cPos) / BeatmapFrame.fadeInStart))
        for i in range(5):
            pygame.gfxdraw.aacircle(surface, self.x, self.y, aOffset+i, BeatmapFrame.currentComboColor)
       


class slider:


    def __init__(self, _object):

        tempSliderData = _object[5].split("|")
        self.sliderType = tempSliderData[0]

        self.x = config.xOffset + int(config.CURRENT_SCALING * int(_object[0]))
        self.y = config.yOffset + int(config.CURRENT_SCALING * int(_object[1]))
        self.timingPoint = int(_object[2])
        #print(tempSliderData)
        if self.sliderType == "L":
            endPos = tempSliderData[1].split(":")
            self.endX = config.xOffset + int(config.CURRENT_SCALING * int(endPos[0]))
            self.endY = config.yOffset + int(config.CURRENT_SCALING * int(endPos[1]))
        elif self.sliderType == "B" or self.sliderType == "P":
            self.points = [(self.x, self.y)]
            nextPoints = tempSliderData[1::]
            for i in nextPoints:
                tempPoint = i.split(":")
                tempX = int(int(tempPoint[0]) * config.CURRENT_SCALING) + config.xOffset
                tempY = int(int(tempPoint[1]) * config.CURRENT_SCALING) + config.yOffset
                self.points.append((tempX, tempY))
            

    def render(self, cPos, surface):
        pygame.gfxdraw.filled_circle(surface, self.x, self.y, BeatmapFrame.circleSize, BeatmapFrame.currentComboColor)
        pygame.gfxdraw.filled_circle(surface, self.x, self.y, int(BeatmapFrame.circleSize*0.9), (0,0,0))
        aOffset = int(BeatmapFrame.circleSize + BeatmapFrame.approachCircleSize * ((self.timingPoint-cPos) / BeatmapFrame.fadeInStart))
        for i in range(5):
            pygame.gfxdraw.aacircle(surface, self.x, self.y, aOffset+i, BeatmapFrame.currentComboColor)

        if self.sliderType == "L":
            pygame.draw.aaline(surface, (255,255,255), (self.x, self.y), (self.endX, self.endY))
        elif self.sliderType == "B" or self.sliderType == "P":
            pygame.gfxdraw.bezier(surface, self.points, 5, (255,255,255))
            


class spinner:


    def __init__(self, _object):

        self.x = config.xOffset + int(config.CURRENT_SCALING * int(_object[0]))
        self.y = config.yOffset + int(config.CURRENT_SCALING * int(_object[1]))
        self.timingPoint = int(_object[2])


    def render(self, cPos, surface):
        pygame.gfxdraw.filled_circle(surface, self.x, self.y, int(BeatmapFrame.circleSize/5), BeatmapFrame.currentComboColor)
        pygame.gfxdraw.aacircle(surface, self.x, self.y, BeatmapFrame.circleSize*5, BeatmapFrame.currentComboColor)
        
