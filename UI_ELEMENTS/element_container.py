from UI_ELEMENTS.base_element import BaseElementUI
from UI_ELEMENTS.shapes import RectAle, LineAle, CircleAle
from UI_ELEMENTS.event_tracker import EventTracker

DO_NOT_EXECUTE = False
if DO_NOT_EXECUTE:
    import pygame

class Container(BaseElementUI):
    def __init__(self, x, y, w, h, achor=None, performant=False, scrollable=False):
        super().__init__(x, y, w, h, achor, performant)

        self.scrollable = scrollable
        if self.scrollable:
            self.scrolled: float = 0.0              # normalized value of scrolled distance so far between [0, 1]
            self.scrollable_distance: float = 0.0   # maximum distance scrollable as value in pixels (obtained by testing the height of each element)
            self.scroll_update: int = 0             # value extracted from the events (modify to match the excursion needed)

        self.child_elements: dict[str, BaseElementUI] = {}
        self.shape.add_shape("bg", RectAle("0cw", "0ch", "100cw", "100ch", [100, 100, 155], 0, 0))


    def add_element(self, name, element):
        self.child_elements[name] = element
        self.child_elements[name].parent_object = self


    def analyze_coordinate(self):
        super().analyze_coordinate()

        for name, child in self.child_elements.items():

            offset_x = self.x.value
            offset_y = self.y.value

            # considers the scroll amount on independet elements
            # anchored elements will follow automatically
            if self.scrollable and child.anchor_mode == 'absolute':
                scroll_iteration = self.scroll_update
                print(f"Analyzed: {scroll_iteration = }")
                offset_y += scroll_iteration * 10

            child.analyze_coordinate(offset_x, offset_y)
        
    
    def get_render_objects(self):
        ris = []
        
        # adds himself
        ris.extend(super().get_render_objects())

        # adds childrens
        for name, obj in self.child_elements.items():
            ris.extend(obj.get_render_objects())
        
        return ris
    

    def handle_events(self, events):
        # handle scroll (if enabled)
        if self.scrollable:
            tracker = EventTracker()
            if self.bounding_box.collidepoint(tracker.mouse_pos) and tracker.scrolled != 0:
                scrollato = tracker.get_scroll_info()
                print(f"Obtained scroll amount of: {scrollato = }")
                tracker.scrolled -= scrollato
                print(f"Removed from Singleton: {tracker.scrolled = }")
                self.scroll_update += scrollato
                print(f"Updated self.scroll_update: {self.scroll_update = }")
        
            if self.scroll_update != 0:
                self.analyze_coordinate()
        
        # handle child events
        [element.handle_events(events) for index, element in self.child_elements.items()]