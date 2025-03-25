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

        self.has_child_or_components = False

        # self.child_elements: dict[str, BaseElementUI] = {}
        # self.child_indices: list[str] = []

        # self.use_tab_for_selection = True                           # TODO: give the possibility to disable this function (For example in containers with only viewports)
        # self.element_highlighted = -1
        # self.element_selected = -1

        # self.componenets: dict[str, Label_text | Button_toggle] = {
        #     "toggle" : Button_toggle("1vw", "1vh", "2.5cw", "2.5cw", "lu"),
        #     "title" : Label_text("2vw 2.5cw", "1vh", "30cw", "2.5cw", "lu", text=title, text_centered_x=False, text_tag_support=False, render_bg=False)
        # }

        # for key, value in self.componenets.items():
        #     value.parent_object = self

        self.min_value = min_value
        self.max_value = max_value
        self.value = starting_value 

        self.orientation = orientation
        
        self.shape.add_shape("bg", RectAle("0cw", "0ch", "100cw", "100ch", [50, 50, 50], 0, 0))
        self.shape.add_shape("indicator", RectAle("0cw", "0ch", "100cw", "5ch", [100, 100, 100], 0, 0))

    