from UI_ELEMENTS.base_element import BaseElementUI
from UI_ELEMENTS.shapes import RectAle, LineAle, CircleAle
from UI_ELEMENTS.element_button_toggle import Button_toggle
from UI_ELEMENTS.element_text_label import Label_text
from UI_ELEMENTS.event_tracker import EventTracker


class Collapse_Window(BaseElementUI):
    def __init__(self, x, y, w, h, achor=None, title="Collapsable window", performant=False):
        super().__init__(x, y, w, h, achor, performant)

        self.has_child_or_components = True

        self.use_tab_for_selection = True                           # TODO: give the possibility to disable this function (For example in containers with only viewports)
        
        self.shape.add_shape("bg", RectAle("0cw", "0ch", "100cw", "100ch", [20, 20, 20], 0, 2))
        self.componenets: dict[str, Label_text | Button_toggle] = {
            "_toggle" : Button_toggle("1vw", "1vh", "2.5cw", "2.5cw", "lu"),
            "_title" : Label_text("2vw 2.5cw", "1vh", "30cw", "2.5cw", "lu", text=title, text_centered_x=False, text_tag_support=False, render_bg=False)
        }

        for key, value in self.componenets.items():
            value.parent_object = self

        self.child_elements: dict[str, BaseElementUI] = {}
        self.child_indices: list[str] = []

        self.h_closed = h
        self.h_opened = "2vh 2.5cw"


    @property
    def total_children(self):
        ris = {**self.componenets, **self.child_elements}
        ris.pop("_title")
        return ris

    
    @property
    def total_children_indices(self):
        ris = [key for key in self.total_children.keys() if key != "_title"]
        return ris


    def add_element(self, name, element):
        self.child_elements[name] = element
        self.child_elements[name].parent_object = self
        self.child_elements[name].name = name
        self.child_elements[name].depth_level = self.depth_level + 1


    def analyze_coordinate(self, offset_x=0, offset_y=0):
        super().analyze_coordinate(offset_x, offset_y)

        for name, child in self.componenets.items():
            child.analyze_coordinate(self.x.value, self.y.value)
        
        for name, child in self.child_elements.items():
            child.analyze_coordinate(self.x.value, self.y.value)


    def get_smart_offset_toggle_zone(self):
        """
        Return the right-down corner of the bounding box of the toggle zone, if an object is put inside this zone the program might encour in unexpected behaviour.
        """
        return "2vw 32.5cw", "1vh 2.5cw"

    
    def get_render_objects(self):
        if self.is_enabled:
            ris = []
            
            # adds himself
            ris.extend(super().get_render_objects())
            for name, obj in self.componenets.items():            
                ris.extend(obj.get_render_objects())

            # adds childrens
            if self.componenets["_toggle"].get_state():
                for name, obj in self.child_elements.items():
                    ris.extend(obj.get_render_objects())
                
            return ris
        else:
            return []


    def handle_events(self, events):
        if self.is_enabled:
            # handle self components events
            [element.handle_events(events) for index, element in self.componenets.items()]

            self.update_open_closure()

            # handle child events
            if self.componenets["_toggle"].get_state():
                [element.handle_events(events) for index, element in self.child_elements.items()]

    
    def update_open_closure(self):
        # check for open / close the window
        old_h = self.h.lst_str_value
        if self.componenets["_toggle"].get_state():
            self.h.change_str_value(self.h_closed)
        else:
            self.h.change_str_value(self.h_opened)
        
        # request for update open / close call
        if old_h != self.h.lst_str_value:
            if not self.parent_object is None:
                self.parent_object.analyze_coordinate()
