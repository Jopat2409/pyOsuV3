""" ---------- OSU MODULES ---------- """
import config  # for program-global variables
import BeatmapFrame  # for getting the current beatmap information

""" ---------- PYTHON MODULES ---------- """
import pygame  # for rendering
import pygame.gfxdraw  # for anti-aliased rendering

"""
Provides encapsulation for osu hit objects
"""


class hitCircle:
    """
    Encapsulates the render function and data storage of a hit circle
    Originally planned to be more data oriented, may implement in future
    """

    def __init__(self, _object):
        # set the scaled x value of the center of the hit object
        self.x = config.xOffset + int(config.CURRENT_SCALING * int(_object[0]))
        # set the scaled y value of the center of the hit object
        self.y = config.yOffset + int(config.CURRENT_SCALING * int(_object[1]))
        # set the timing point hit object
        self.timingPoint = int(_object[2])

    def render(self, cPos, surface):
        pygame.gfxdraw.filled_circle(surface, self.x, self.y, BeatmapFrame.circleSize, (255, 255, 255))
        pygame.gfxdraw.filled_circle(surface, self.x, self.y, int(BeatmapFrame.circleSize * 0.9),
                                     BeatmapFrame.currentComboColor)
        # interpolate the amount of time through the hit window the current time is, to work out the radius of the
        # approach circle
        aOffset = int(BeatmapFrame.circleSize +
                      BeatmapFrame.approachCircleSize * ((self.timingPoint - cPos) / BeatmapFrame.fadeInStart))
        for i in range(5):
            # draw 5 circles incrememntally smaller, as pygame does not have a feature for thickness on circles
            pygame.gfxdraw.aacircle(surface, self.x, self.y, aOffset + i, BeatmapFrame.currentComboColor)


class slider:
    """
    Encapsulates the render function and data storage of a slider object
    Originally planned to be more data oriented, may implement in future
    """

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
        # print(tempSliderData)
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
            # initializes the points of the slider with the initial x and y position
            self.points = [(self.x, self.y)]
            # gets the remaining points
            nextPoints = tempSliderData[1::]
            for i in nextPoints:
                # append the point's x and y value to the self.points array
                tempPoint = i.split(":")
                tempX = int(int(tempPoint[0]) * config.CURRENT_SCALING) + config.xOffset
                tempY = int(int(tempPoint[1]) * config.CURRENT_SCALING) + config.yOffset
                self.points.append((tempX, tempY))

    """
    Renders the slider
    cPos: current time within the beatmap
    surface: surface to draw to
    """

    def render(self, cPos, surface):
        # draw the slider head as a normal hit circle
        pygame.gfxdraw.filled_circle(surface, self.x, self.y, BeatmapFrame.circleSize, BeatmapFrame.currentComboColor)
        pygame.gfxdraw.filled_circle(surface, self.x, self.y, int(BeatmapFrame.circleSize * 0.9), (0, 0, 0))
        # draw the approach circle
        aOffset = int(BeatmapFrame.circleSize + BeatmapFrame.approachCircleSize * (
                    (self.timingPoint - cPos) / BeatmapFrame.fadeInStart))
        for i in range(5):
            pygame.gfxdraw.aacircle(surface, self.x, self.y, aOffset + i, BeatmapFrame.currentComboColor)

        # if the slider is a linear slider
        if self.sliderType == "L":
            # draw and anti-aliased line between the start and end positions
            pygame.draw.aaline(surface, (255, 255, 255), (self.x, self.y), (self.endX, self.endY))
        # if the slider is a bezier or perfect circle
        elif self.sliderType == "B" or self.sliderType == "P":
            # draw a bezier curve using the points
            pygame.gfxdraw.bezier(surface, self.points, 5, (255, 255, 255))


class spinner:
    """
    Encapsulates the render function and data storage of a spinner object
    Originally planned to be more data oriented, may implement in future
    """

    def __init__(self, _object):
        # set the x and y of the object (theoretically should be center of screen)
        self.x = config.xOffset + int(config.CURRENT_SCALING * int(_object[0]))
        self.y = config.yOffset + int(config.CURRENT_SCALING * int(_object[1]))
        # store the timing point
        self.timingPoint = int(_object[2])

    def render(self, cPos, surface):
        """
        Render the spinner
        cPos: current position in time
        surface: surface to render to
        """
        # draw a small circle at the center of the spinner
        pygame.gfxdraw.filled_circle(surface, self.x, self.y, int(BeatmapFrame.circleSize / 5),
                                     BeatmapFrame.currentComboColor)
        # draw a large circle about the center of the smaller circle
        pygame.gfxdraw.aacircle(surface, self.x, self.y, BeatmapFrame.circleSize * 5, BeatmapFrame.currentComboColor)
