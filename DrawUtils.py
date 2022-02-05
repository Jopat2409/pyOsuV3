import pygame

"""
Provides basic wrappers for pygame
i have no clue why i didnt write this before lol
"""

def DrawImage(DestinationSurface, ImagePath, Destination, NewSize=None):
    try:
        if NewSize:
            newImage = pygame.transform.scale(pygame.image.load(ImagePath).convert(), NewSize)
        else:
            newImage = pygame.image.load(ImagePath).convert()
    except FileNotFoundError:
        print(f"ERROR, file {ImagePath} not found!")
        return
    DestinationSurface.blit(newImage, Destination)


def DrawText(DestinationSurface, Text, Position, Color=(0, 0, 0), Font=None):
    if Font:
        DestinationSurface.blit(Font.render(Text, True, Color, Position), Position)
        return
