from UI_ELEMENTS.base_element import BaseElementUI
from UI_ELEMENTS.shapes import RectAle, LineAle, CircleAle
from UI_ELEMENTS.event_tracker import EventTracker
import numpy as np
from AleUI import AppSizes

DO_NOT_EXECUTE = False
if DO_NOT_EXECUTE:
    import pygame


class ScrollBar(BaseElementUI):
    def __init__(self, x, y, w, h, origin='left-up', performant=False, starting_value=0.0, min_value=0.0, max_value=1.0, orientation='horizontal'):
        super().__init__(x, y, w, h, origin, performant)

        self.min_value = min_value
        self.max_value = max_value
        self.value = starting_value 

        self.orientation = orientation
        
        self.shape.add_shape("bg", RectAle("0cw", "0ch", "100cw", "100ch", [50, 50, 50], 0, 0))
        self.shape.add_shape("indicator", RectAle("0cw", "0ch", "100cw", "5ch", [100, 100, 100], 0, 0))

    