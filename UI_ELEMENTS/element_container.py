from UI_ELEMENTS.base_element import BaseElementUI
from UI_ELEMENTS.shapes import RectAle, LineAle, CircleAle
from UI_ELEMENTS.event_tracker import EventTracker
from pygame import Surface
import numpy as np
from AleUI import AppSizes

DO_NOT_EXECUTE = False
if DO_NOT_EXECUTE:
    import pygame

class Container(BaseElementUI):
    def __init__(self, x, y, w, h, achor=None, performant=False, scrollable=False):
        super().__init__(x, y, w, h, achor, performant)

        self.scrollable = scrollable
        if self.scrollable:
            self.scrolled: float = 0.0                              # normalized value of scrolled distance so far between [0, 1]
            self.scrollable_distance: float = 0.0                   # maximum distance scrollable as value in pixels (obtained by testing the height of each element)
            self.scroll_update: int = 0                             # value extracted from the events (modify to match the excursion needed)
            self.scroll_speed = round(AppSizes().h_viewport / 200)  # sets the speed at which the elements move

        self.clip_canvas = Surface((self.w.value, self.h.value))
        
        self.child_elements: dict[str, BaseElementUI] = {}


    @property
    def scroll_delta(self):
        '''
        Returns the value in pixel of the scroll update times the scroll speed.

        ```
        return round(self.scroll_update * self.scroll_speed)
        ```
        '''
        return round(self.scroll_update * self.scroll_speed)


    def add_element(self, name, element):
        self.child_elements[name] = element
        self.child_elements[name].parent_object = self


    def analyze_coordinate(self):
        super().analyze_coordinate()
        self.clip_canvas = Surface((self.w.value, self.h.value))

        for name, child in self.child_elements.items():

            # generally the only offset used will be the scroll, but in general might be used for pan
            offset_x = 0
            offset_y = 0

            # considers the scroll amount on independet elements
            # anchored elements will follow automatically
            if self.scrollable and child.anchor_mode == 'absolute':
                offset_y += self.scroll_delta

            child.analyze_coordinate(offset_x, offset_y)

        # update the maximum excursion of the scrollable element
        self.analyze_max_scroll_depth()

        # if the container is scrollable, test each child after the coordinate update if they are outside the bounding box
        self.analyze_children_outside_BB()


    def analyze_max_scroll_depth(self):
        max_value = -1e6
        if self.scrollable:
            for name, child in self.child_elements.items():
                tip = child.y.value + child.h.value
                if tip > max_value:
                    max_value = tip
            self.scrollable_distance = max_value - self.scroll_delta
            self.scrolled = self.scroll_delta / self.scrollable_distance


    def analyze_children_outside_BB(self):
        if self.scrollable:
            for name, child in self.child_elements.items():
                if child.y.value + child.h.value > self.y.value and child.y.value < self.y.value + self.h.value:
                    child.ask_enable_disable_element(True, 1)
                else:
                    child.ask_enable_disable_element(False, 1)

    
    def get_render_objects(self):
        ris = []
        
        # adds himself
        ris.extend(super().get_render_objects())

        # adds childrens
        for name, obj in self.child_elements.items():
            ris.extend(obj.get_render_objects())
        
        return ris
    

    def handle_events(self, events):

        # calculates the local position of the mouse relative to the container
        tracker = EventTracker()
        tracker.local_mouse_pos.append(np.subtract(tracker.mouse_pos, np.array([self.x.value, self.y.value])))

        # handle scroll (if enabled)
        if self.scrollable:
            old_scroll = self.scroll_update
            if self.bounding_box.collidepoint(tracker.mouse_pos) and tracker.scrolled != 0:
                scrollato = tracker.get_scroll_info()
                tracker.scrolled -= scrollato
                self.scroll_update += scrollato

                # control to not overshoot (negative case)
                if self.scroll_update >= 0:
                    self.scroll_update = 0
                
                # control to not overshoot (positive case)
                if abs(self.scroll_delta) > abs(self.scrollable_distance):
                    self.scroll_update = - self.scrollable_distance / self.scroll_speed

            if old_scroll != self.scroll_update:
                self.analyze_coordinate()
        
        # handle child events
        [element.handle_events(events) for index, element in self.child_elements.items()]