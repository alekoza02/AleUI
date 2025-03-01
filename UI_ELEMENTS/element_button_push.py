from UI_ELEMENTS.base_element import BaseElementUI
from UI_ELEMENTS.shapes import RectAle, LineAle, CircleAle


class Button_push(BaseElementUI):
    def __init__(self, x, y, w, h, origin=None, performant=False):
        super().__init__(x, y, w, h, origin, performant)

        self.shape.add_shape("bg", RectAle("0cw", "0ch", "100cw", "100ch", [40, 40, 40], 0, 0))

