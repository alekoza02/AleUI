from UI_ELEMENTS.base_element import BaseElementUI
from UI_ELEMENTS.shapes import RectAle, LineAle, CircleAle
from UI_ELEMENTS.event_tracker import EventTracker
from UI_ELEMENTS.element_scrollbar import ScrollBar
from UI_ELEMENTS.element_collapse_window import Collapse_Window
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
            self.scrollable_distance: float = None                  # maximum distance scrollable as value in pixels (obtained by testing the height of each element)
            self.scroll_update: int = 0                             # value extracted from the events (modify to match the excursion needed)
            self.scroll_speed = round(AppSizes().h_viewport / 50)  # sets the speed at which the elements move
            self.scroll_UI_element: ScrollBar = ScrollBar("98cw", "50ch", "1cw", "95ch", 'left-center', orientation='vertical')
            self.scroll_UI_element.parent_object = self

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

        # if is scrollable update the scroll UI element
        if self.scrollable:
            self.scroll_UI_element.analyze_coordinate(0, 0)

        for name, child in self.child_elements.items():

            # generally the only offset used will be the scroll, but in general might be used for pan
            offset_x = 0
            offset_y = 0

            # considers the scroll amount on independet elements
            # anchored elements will follow automatically
            if self.scrollable and child.anchor_mode == 'absolute':
                offset_y += self.scroll_delta

            child.analyze_coordinate(offset_x, offset_y)

        if self.scrollable:
            # update the maximum excursion of the scrollable element
            self.analyze_max_scroll_depth()
            # change the size of the UI scroll indicator
            self.scroll_UI_element.shape.shapes["indicator"].h.change_str_value(f"{min(abs((self.h.value - self.scrollable_distance) / self.h.value) * 100, 100)}ch")
            # change the position of the UI scroll indicator
            self.scroll_UI_element.shape.shapes["indicator"].y.change_str_value(f"{(100 - float(self.scroll_UI_element.shape.shapes["indicator"].h.lst_str_value[0][:-2])) * abs(self.scrolled)}ch")
            self.scroll_UI_element.analyze_coordinate()


        # test each child after the coordinate update if they are outside the bounding box
        self.analyze_children_outside_BB()


    def analyze_max_scroll_depth(self):
        max_value = -1e6
        for name, child in self.child_elements.items():
            tip = child.y.value + child.h.value
            if tip > max_value:
                max_value = tip
        self.scrollable_distance = max_value - self.scroll_delta - self.h.value
        
        # Controls negative distances
        if self.scrollable_distance < 0:
            self.scrollable_distance = 1e-6
        
        self.scrolled = self.scroll_delta / self.scrollable_distance


    def analyze_children_outside_BB(self):
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
        
        # adds scroll UI element if scrollable
        if self.scrollable:
            ris.extend(self.scroll_UI_element.get_render_objects())

        return ris
    

    def handle_events(self, events):

        # calculates the local position of the mouse relative to the container
        tracker = EventTracker()
        tracker.local_mouse_pos.append(np.subtract(tracker.mouse_pos, np.array([self.x.value, self.y.value])))

        # handle scroll (if enabled)
        if self.scrollable:

            self.scroll_UI_element.handle_events(events)

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


        # store previous state of all elements that may change their size
        old_states = [child.componenets["toggle"].get_state() for name, child in self.child_elements.items() if type(child) == Collapse_Window]

        # handle child events
        [element.handle_events(events) for index, element in self.child_elements.items()]
        
        new_state = [child.componenets["toggle"].get_state() for name, child in self.child_elements.items() if type(child) == Collapse_Window]


        update = False
        for o, n in zip(old_states, new_state):
            if o != n:
                update = True

        if update:
            self.analyze_coordinate()
