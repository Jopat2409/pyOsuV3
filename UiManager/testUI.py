import pygame
import UiMain
import UiObjects
import os

pygame.init()

def doSomething():
    print("worked")


sf = pygame.display.set_mode((1000,700))
sf.fill(0)
ui = UiMain.UiHandler()

ui.addElement(UiObjects.Image(os.path.join("assets", "ape.jpg"), 10, 10,function=doSomething))

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
