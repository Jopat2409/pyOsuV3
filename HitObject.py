""" ---------- OSU MODULES ---------- """
import config
import BeatmapFrame
import SkinLoader
""" ---------- PYTHON MODULES ---------- """
import pygame
import pygame.gfxdraw





"""
Encapsulates the render function and data storage of a hit circle
Originally planned to be more data oriented, may implement in future
"""
class hitCircle:


    def __init__(self, _object):

        # set the scaled x value of the center of the hit object
        self.x = config.xOffset + int(config.CURRENT_SCALING * int(_object[0]))
        # set the scaled y value of the center of the hit object
        self.y = config.yOffset + int(config.CURRENT_SCALING * int(_object[1]))
        # set the timing point hit object
        self.timingPoint = int(_object[2])

        
    def render(self, cPos, surface):

        # blit the hit circle image to the position
        surface.blit(SkinLoader.beatmapMap["hitCircle"], (self.x - BeatmapFrame.circleSize, self.y - BeatmapFrame.circleSize))
        # blit the hit circle overlay image to the position
        surface.blit(SkinLoader.beatmapMap["hitCircleOverlay"], (self.x - BeatmapFrame.circleSize, self.y - BeatmapFrame.circleSize))
        # interpolate the amount of time through the hit window the current time is, to work out the radius of the approach circle
        aOffset = int(BeatmapFrame.circleSize + BeatmapFrame.approachCircleSize * ((self.timingPoint-cPos) / BeatmapFrame.fadeInStart))
        for i in range(5):
            # draw 5 circles incrememntally smaller, as pygame does not have a feature for thickness on circles
            pygame.gfxdraw.aacircle(surface, self.x, self.y, aOffset+i, BeatmapFrame.currentComboColor)
       

"""
Encapsulates the render function and data storage of a slider object
Originally planned to be more data oriented, may implement in future
"""
class slider:


    def __init__(self, _object):
        
        # split the slider data 
        tempSliderData = _object[5].split("|")
        # work out the slider type from the correct bit
        self.sliderType = tempSliderData[0]
        # set the scaled x value of the center of the starting circle
        self.x = config.xOffset + int(config.CURRENT_SCALING * int(_object[0]))
        # set the scaled y value of the center of the starting circle
        self.y = config.yOffset + int(config.CURRENT_SCALING * int(_object[1]))
        # set the timing point hit object
        self.timingPoint = int(_object[2])
        #print(tempSliderData)
        # if the slider is a linear slider
        if self.sliderType == "L":
            # get the end position from the correct data
            endPos = tempSliderData[1].split(":")
            # scale the ending x position
            self.endX = config.xOffset + int(config.CURRENT_SCALING * int(endPos[0]))
            # scale the ending y position
            self.endY = config.yOffset + int(config.CURRENT_SCALING * int(endPos[1]))
        
        # if the slider is a bezier or perfect circle
        elif self.sliderType == "B" or self.sliderType == "P":
            #
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
        



