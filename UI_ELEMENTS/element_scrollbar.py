from UI_ELEMENTS.base_element import BaseElementUI
from UI_ELEMENTS.shapes import RectAle, LineAle, CircleAle
from UI_ELEMENTS.event_tracker import EventTracker
import numpy as np
from AleUI import AppSizes
import pygame

DO_NOT_EXECUTE = False
if DO_NOT_EXECUTE:
    ...

class ScrollBar(BaseElementUI):
    def __init__(self, x, y, w, h, origin='left-up', performant=False, starting_value=0.0, min_value=0.0, max_value=1.0, orientation='horizontal'):
        super().__init__(x, y, w, h, origin, performant)

        self.has_child_or_components = False

        self.min_value = min_value
        self.max_value = max_value
        self.value = starting_value 
        self.delta_value = 0

        self.orientation = orientation
        
        self.shape.add_shape("bg", RectAle("0cw", "0ch", "100cw", "100ch", [50, 50, 50], 0, 0))
        self.shape.add_shape("indicator", RectAle("0cw", "0ch", "100cw", "5ch", [100, 100, 100], 0, 0))


        self.keep_updating = False

    
    def handle_events(self, events):
        if self.is_enabled:
            # get the latest events and relative positions 
            tracker = EventTracker()
        
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.bounding_box.collidepoint(tracker.local_mouse_pos[-1]):
                        self.keep_updating = True
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.keep_updating = False

            # if self.indicatore.selezionato:
            #     self.indicatore.handle_events(events)
            #     try:
            #         self.value = self.get_value_normalized(float(self.indicatore.get_text(real_time=True)))
            #     except Exception:
            #         ...
            # else:
            #     self.indicatore.change_text(f"{self.get_value():.3f}")

            self.delta_value = 0
            if self.keep_updating:
                
                old_value = self.value

                if self.orientation == 'vertical':
                    self.value = (tracker.local_mouse_pos[-1][1] - self.y.value) / self.h.value
                elif self.orientation == 'horizontal':
                    self.value = (tracker.local_mouse_pos[-1][0] - self.x.value) / self.w.value

                if self.value < 0:
                    self.value = 0      
                if self.value > 1:
                    self.value = 1  

                self.delta_value = self.value - old_value

                self.shape.shapes["indicator"].y.change_str_value(f"{(100 - float(self.shape.shapes["indicator"].h.lst_str_value[0][:-2])) * abs(self.value)}ch")
                self.analyze_coordinate()   