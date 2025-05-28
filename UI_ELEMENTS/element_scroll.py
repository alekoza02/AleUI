from UI_ELEMENTS.base_element import BaseElementUI
from UI_ELEMENTS.shapes import RectAle, LineAle, CircleAle

DO_NOT_EXECUTE = False
if not DO_NOT_EXECUTE:
    import pygame
    from pygame.event import Event
    from UI_ELEMENTS.event_tracker import EventTracker
    from UI_ELEMENTS.element_text_label import Label_text


class Scroll(BaseElementUI):
    def __init__(self, x, y, w, h, origin='left-up', title="click me"):
        super().__init__(x, y, w, h, origin)

        self.shape.add_shape("bg", RectAle("0cw", "0ch", "100cw", "100ch", [40, 40, 40], 0, 0))
        self.shape.add_shape("bg_selectable", RectAle("0cw", "7.5ch", "100cw", "100ch -7.5ch", [50, 50, 50], 0, 0))
        
        self.componenets: dict[str, Label_text] = {
            "_title" : Label_text("0px", "0px", "100cw", "7.5ch", "left-up", text=title, text_tag_support=False, render_bg=False, text_centered_x=False)
        }

        for key, value in self.componenets.items():
            value.parent_object = self
        

    def handle_events(self, events: list['Event']):
            
        if self.is_enabled:
            # handle self components events
            [element.handle_events(events) for index, element in self.componenets.items()]

            # get the latest events and relative positions
            tracker = EventTracker()

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.bounding_box.collidepoint(tracker.get_local_mouse_pos(self.get_parent_local_offset())):
                        # self.callback()
                        ...

            # Hover block #
            if self.bounding_box.collidepoint(tracker.get_local_mouse_pos(self.get_parent_local_offset())):
                self.is_hover_old = self.is_hover
                self.is_hover = True
            else:
                self.is_hover_old = self.is_hover
                self.is_hover = False
            
            
            if self.is_hover and self.is_hover != self.is_hover_old:
                self.shape.shapes["bg"].color += 5
                self.shape.shapes["bg_selectable"].color += 10
            elif not self.is_hover and self.is_hover != self.is_hover_old:
                self.shape.shapes["bg"].color -= 5
                self.shape.shapes["bg_selectable"].color -= 10
            # Hover block #


    def launch_tab_action(self):
        ...

    
    def analyze_coordinate(self, offset_x=0, offset_y=0):
        super().analyze_coordinate(offset_x, offset_y)
    
        for name, child in self.componenets.items():
            child.analyze_coordinate(self.x.value, self.y.value)


    def get_render_objects(self):
        if self.is_enabled:
            ris = []
            
            # adds himself
            ris.extend(super().get_render_objects())
            for name, obj in self.componenets.items():            
                ris.extend(obj.get_render_objects())

            return ris
        else:
            return []
        

    def __repr__(self):
        return f"Scroll element containing {None} elements and showing {None} objects. Starting index is {None}"