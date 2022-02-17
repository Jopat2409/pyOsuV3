import config
import pygame


class gsBeatmapResults:

    def __init__(self, beatmapResults: dict):

        self.m_results = beatmapResults
        self.m_font =  pygame.font.SysFont('Arial', 25)

    


    def DrawResult(self, result, surface, position):

        fText = self.font.render(f"{result[0]: result[1]}", True, (0, 0, 0))
        surface.blit(fText, position)

        

    def getRenderSnapshot(self, surface, interpolation):

        xPos = config.SCREEN_RESOLUTION[0] * (2/5)
        yPos = config.SCREEN_RESOLUTION[1] * (1/3)
        for index,rType in enumerate(self.m_results):
            self.DrawResult((rType, self.m_results[rType]), surface, (xPos, yPos*index*20))
        
