import pygame
from pygame import gfxdraw

"""
Provides basic wrappers for pygame
i have no clue why i didnt write this before lol
"""




def DrawImage(DestinationSurface, ImagePath, Destination, NewSize=None):
    newImage = None
    try:
        if NewSize:
            newImage = pygame.transform.scale(pygame.image.load(ImagePath).convert())
        else:
            newImage = pygame.image.load(ImagePath).convert()
    except FileNotFoundError:
        print(f"ERROR, file {ImagePath} not found!")
        return
    DestinationSurface.blit(ImagePath, Destination)


def DrawText(DestinationSurface, Text, Position, Color=(0, 0, 0), Font=None):
    if Font:
        Font.render(Text, True, Color, Position)
        return


