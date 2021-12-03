import pygame
import UiMain
import UiObjects
import os
from UiObjects import FLAGS as flags

pygame.init()

def doSomething():
    print("worked")

def hover():
    print("hovering")


sf = pygame.display.set_mode((1000,700))
sf.fill(0)
ui = UiMain.UiHandler()

apeButton = ui.addElement([pygame.image.load(os.path.join("assets", "ape.jpg")), (10,10), 1])
ui.addEvent(apeButton, flags.UX_ONCLICK, doSomething)
ui.addEvent(apeButton, flags.UX_ONHOVER, hover)

while(True):

    for event in pygame.event.get():
        
        pygame.display.flip()
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        else:
            ui.handleEvent(event)
        ui.update()
        ui.render(sf)
