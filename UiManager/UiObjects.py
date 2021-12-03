import pygame
from enum import IntEnum,unique




@unique
class FLAGS(IntEnum):
    UX_RENDER       = 0
    UX_POS          = 1
    UX_ONCLICK      = 2
    UX_ONHOVER      = 3
    UX_ALLOWDRAG    = 4
    UX_ALLOWSLIDE   = 5
    
