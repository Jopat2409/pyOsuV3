import config
import pygame
import pygame.gfxdraw


class HitCircle:

    def __init__(self, hitObject):
        
        self.x = int(int(hitObject[0]) * config.CURRENT_SCALING)+config.xOffset
        self.y = int(int(hitObject[1]) * config.CURRENT_SCALING)
        self.timingPoint = int(hitObject[2])
    

    def render(self, surface, radius, aCircleRadius, xOffset):

        pygame.gfxdraw.filled_circle(surface, self.x, self.y, radius, (255,255,255))
        pygame.gfxdraw.filled_circle(surface, self.x, self.y, int(radius*0.9), (0,0,0))
        if aCircleRadius > radius:
            for i in range(0,5):
                pygame.gfxdraw.aacircle(surface, self.x, self.y, aCircleRadius+i, (255,255,255))


class Slider:

    def __init__(self, hitObject):
        
        sliderInfo = hitObject[5::]
        self.type = sliderInfo[0][1]
        if self.type == "L":
            self.x = int(int(hitObject[0])*config.CURRENT_SCALING) + config.xOffset
            self.y = int(int(hitObject[1])*config.CURRENT_SCALING)
            self.timingPoint = int(hitObject[2])
            tempPoints = sliderInfo[0].split("|")[1]
            self.endX = int(int(tempPoints[0])*config.CURRENT_SCALING)+config.xOffset
            self.endY = int(int(tempPoints[1])*config.CURRENT_SCALING)
        
        elif self.type == "B":
            self.timingPoint = int(hitObject[2])
            self.points = [(int(int(hitObject[0])*config.CURRENT_SCALING), int(int(hitObject[1])*config.CURRENT_SCALING))]
            
            tempPoints = sliderInfo[0].split("|")
            for p in tempPoints[1::]:
                point = p.split(":")
                self.points.append((int(int(point[0])*config.CURRENT_SCALE)+config.xOffset,
                                    int(int(point[1])*config.CURRENT_SCALE)
                ))
        elif self.type == "P":

            
            
    def render(self, surface, radius, aCircleRadius, xOffset):
        pygame.gfxdraw.filled_circle(surface, self.x, self.y, radius, (255,255,255))
        pygame.gfxdraw.filled_circle(surface, self.x, self.y, int(radius*0.9), (0,0,0))
        if aCircleRadius > radius:
            for i in range(0,5):
                pygame.gfxdraw.aacircle(surface, self.x, self.y, aCircleRadius+i, (255,255,255))
        
        if self.type == "L":
            pygame.draw.aaline(surface, (255,255,255), (self.x + xOffset, self.y), (self.endX, self.endY))
        elif self.type == "B":
            pygame.gfxdraw.bezier(surface, self.points, 5, (255,255,255))


class Spinner:

    def __init__(self, hitObject):

        self.parseObject(hitObject)

hitObjectMap = {0:HitCircle,
                1:Slider,
                3:Spinner
                }

def parseHitObject(hitObject):
    # split the object by the commas (since each hit object is stored as a csv array)
    parsedArray  = hitObject.split(",")
    osType = "{0:b}".format(int(parsedArray[3]))
    osType = osType[::-1]
    for i in range(len(osType)):
        if osType[i] == "1":
            try:
                return hitObjectMap[i]()
            except KeyError:
                pass