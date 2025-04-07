from UI_ELEMENTS.base_element import BaseElementUI
from UI_ELEMENTS.shapes import RectAle, LineAle, CircleAle

DO_NOT_EXECUTE = False
if not DO_NOT_EXECUTE:
    import pygame
    from pygame.event import Event
    from UI_ELEMENTS.event_tracker import EventTracker


class Button_toggle(BaseElementUI):
    def __init__(self, x, y, w, h, origin=None, performant=False):
        super().__init__(x, y, w, h, origin, performant)

        self.shape.add_shape("bg", RectAle("0cw", "0ch", "100cw", "100ch", [40, 40, 40], 0, 0))
        self.shape.add_shape("active", RectAle("0cw 5px", "0ch 5px", "100cw -10px", "100ch -10px", [40, 40, 40], 0, 0))

        self.active_color = [100, 100, 100]
        self.toggled = False


    def get_state(self):
        return self.toggled                                                             


    def handle_events(self, events: list['Event']):
        if self.is_enabled:
            # get the latest events and relative positions 
            tracker = EventTracker()

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.bounding_box.collidepoint(tracker.get_local_mouse_pos(self.get_parent_local_offset())):
                        self.change_state()

            # Hover block #
            if self.bounding_box.collidepoint(tracker.get_local_mouse_pos(self.get_parent_local_offset())):
                self.is_hover_old = self.is_hover
                self.is_hover = True
            else:
                self.is_hover_old = self.is_hover
                self.is_hover = False
            
            
            if self.is_hover and self.is_hover != self.is_hover_old:
                self.shape.shapes["active"].color += 10
                self.shape.shapes["bg"].color += 10
            elif not self.is_hover and self.is_hover != self.is_hover_old:
                self.shape.shapes["active"].color -= 10
                self.shape.shapes["bg"].color -= 10
            # Hover block #


    def change_state(self):
        self.toggled = not self.toggled
        if self.toggled: self.shape.change_shape_color("active", self.active_color)
        else: self.shape.change_shape_color("active", self.shape.shapes["bg"].color)


    def launch_tab_action(self):
        self.change_state()