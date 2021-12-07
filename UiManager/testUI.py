import pygame
import UiMain
import UiObjects
import os
from UiObjects import FLAGS as flags
import time

pygame.init()

def doSomething():
    print("Clicked")

def hover():
    print("hovering")


sf = pygame.display.set_mode((1000,700))
sf.fill(0)
ui = UiMain.UiHandler()

apeButton = ui.addElement(os.path.join("c:/Users/Joe/Documents/GitHub/pyOsuV3/UiManager/","assets", "ape.jpg"), (10,10), 1)
ui.addEvent(apeButton, flags.UX_ONCLICK, doSomething)
ui.addEvent(apeButton, flags.UX_ONHOVER, hover)

updates = 0
prevTime = time.time()
while(True):

    eTime = time.time() - prevTime

    if time.time() - prevTime >= 1:
        prevTime = time.time()
        print(updates)
        updates = 0


    for event in pygame.event.get():
        
        pygame.display.flip()
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        else:
            ui.handleEvent(event)
    ui.update()
    ui.render(sf)
    updates+=1
