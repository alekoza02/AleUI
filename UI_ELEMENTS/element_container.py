from UI_ELEMENTS.base_element import BaseElementUI
from UI_ELEMENTS.shapes import RectAle, LineAle, CircleAle


class Container(BaseElementUI):
    def __init__(self, x, y, w, h, achor=None, performant=False):
        super().__init__(x, y, w, h, achor, performant)

        self.child_elements: dict[str, BaseElementUI] = {}
        self.shape.add_shape("bg", RectAle("0cw", "0ch", "100cw", "100ch", [100, 100, 155], 0, 0))


    def add_element(self, name, element):
        self.child_elements[name] = element
        self.child_elements[name].parent_object = self


    def analyze_coordinate(self):
        super().analyze_coordinate()

        for name, child in self.child_elements.items():
            child.analyze_coordinate(self.x.value, self.y.value)

    
    def get_render_objects(self):
        ris = []
        
        # adds himself
        ris.extend(super().get_render_objects())

        # adds childrens
        for name, obj in self.child_elements.items():
            ris.extend(obj.get_render_objects())
        
        return ris
    

    def handle_events(self, events):
        [element.handle_events(events) for index, element in self.child_elements.items()]