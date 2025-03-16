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
        self.toggled = False


    def get_state(self):
        return self.toggled                                                             


    def handle_events(self, events: list['Event']):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.bounding_box.collidepoint(event.pos):
                    self.toggled = not self.toggled


        # Hover block #
        tracker = EventTracker()
        if self.bounding_box.collidepoint(tracker.mouse_pos):
            self.is_hover_old = self.is_hover
            self.is_hover = True
        else:
            self.is_hover_old = self.is_hover
            self.is_hover = False
        
        
        if self.is_hover and self.is_hover != self.is_hover_old:
            self.shape.shapes["bg"].color += 10
        elif not self.is_hover and self.is_hover != self.is_hover_old:
            self.shape.shapes["bg"].color -= 10
        # Hover block #