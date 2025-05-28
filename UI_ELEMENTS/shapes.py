from UI_ELEMENTS.smart_coordinate import SmartCoordinate
from pygame import Rect, Surface, SRCALPHA
from MATH.utils import MateUtils
import numpy as np

class ComplexShape:
    def __init__(self):
        self.shapes: dict[str, RectAle] = {}
        self.shapes_active_map: dict[str, bool] = {}
        

    def add_shape(self, key, shape):
        self.shapes[key] = shape
        self.shapes_active_map[key] = True
        

    def update_shapes(self, new_x, new_y, new_w, new_h):
        for key, shape in self.shapes.items():
            shape.update(new_x, new_y, new_w, new_h)


    def change_shape_visibility(self, key, visibility):
        self.shapes_active_map[key] = visibility


    def change_shape_color(self, key, color):
        self.shapes[key].color = np.array(color)


    def get_shapes(self):
        return [i for booleano, i in zip(self.shapes_active_map.values(), self.shapes.values()) if booleano]
    
    
    def reset(self):
        self.shapes: dict[str, RectAle] = {}
        self.shapes_active_map: dict[str, bool] = {}


class RectAle:
    def __init__(self, x, y, w, h, color, width, border_radius):
        self.x: SmartCoordinate = SmartCoordinate(x)
        self.y: SmartCoordinate = SmartCoordinate(y)
        self.w: SmartCoordinate = SmartCoordinate(w)
        self.h: SmartCoordinate = SmartCoordinate(h)
        self.color = np.array(color)
        self.width = width
        self.border_radius = border_radius
        self.rect = Rect(0, 0, 0, 0)


    def change_coordinates(self, x: str | None = None, y: str | None = None, w: str | None = None, h: str | None = None):
        if not x is None:
            self.x: SmartCoordinate = SmartCoordinate(x)
        if not y is None:
            self.y: SmartCoordinate = SmartCoordinate(y)
        if not w is None:
            self.w: SmartCoordinate = SmartCoordinate(w)
        if not h is None:
            self.h: SmartCoordinate = SmartCoordinate(h)


    def update(self, x_container, y_container, w_container, h_container):
        self.x.update_value(None, None, None, None, w_container, h_container, x_container)
        self.y.update_value(None, None, None, None, w_container, h_container, y_container)
        self.w.update_value(None, None, None, None, w_container, h_container, 0)
        self.h.update_value(None, None, None, None, w_container, h_container, 0)

        self.rect.x = self.x.value 
        self.rect.y = self.y.value
        self.rect.w = self.w.value
        self.rect.h = self.h.value


    def get_attributes(self):
        return {
            "color" : self.color,
            "rect" : self.rect,
            "width" : self.width,
            "border_radius" : self.border_radius
        }
    
    


class LineAle:
    def __init__(self, xs, ys, xe, ye, color, width):
        self.x_start: SmartCoordinate = SmartCoordinate(xs)
        self.x_end: SmartCoordinate = SmartCoordinate(xe)
        self.y_start: SmartCoordinate = SmartCoordinate(ys)
        self.y_end: SmartCoordinate = SmartCoordinate(ye)
        self.color = np.array(color)
        self.width = width
        self.start_pos = (0, 0)
        self.end_pos = (0, 0)


    def update(self, x_container, y_container, w_container, h_container):
        self.x_start.update_value(None, None, None, None, w_container, h_container, x_container)
        self.y_start.update_value(None, None, None, None, w_container, h_container, y_container)
        self.x_end.update_value(None, None, None, None, w_container, h_container, x_container)
        self.y_end.update_value(None, None, None, None, w_container, h_container, y_container)

        self.start_pos = (self.x_start.value, self.y_start.value)
        self.end_pos = (self.x_end.value, self.y_end.value)
        

    def get_attributes(self):
        return {
            "color" : self.color,
            "start_pos" : self.start_pos,
            "end_pos" : self.end_pos,
            "width" : self.width,
        }



class CircleAle:
    def __init__(self, x, y, radius, color, width):
        self.x: SmartCoordinate = SmartCoordinate(x)
        self.y: SmartCoordinate = SmartCoordinate(y)
        self.radius: SmartCoordinate = SmartCoordinate(radius)
        self.color = np.array(color)
        self.width = width
        self.center = (0, 0)


    def update(self, x_container, y_container, w_container, h_container):
        self.x.update_value(None, None, None, None, w_container, h_container, x_container)
        self.y.update_value(None, None, None, None, w_container, h_container, y_container)
        self.radius.update_value(None, None, None, None, w_container, h_container)
        
        self.center = (self.x.value, self.y.value)
        

    def get_attributes(self):
        return {
            "color" : self.color,
            "center" : self.center,
            "radius" : self.radius.value,
            "width" : self.width,
        }
    


class SurfaceAle:
    def __init__(self, x, y, w, h):
        self.x: SmartCoordinate = SmartCoordinate(x)
        self.y: SmartCoordinate = SmartCoordinate(y)
        self.w: SmartCoordinate = SmartCoordinate(w)
        self.h: SmartCoordinate = SmartCoordinate(h)
        self.surface: Surface = Surface((self.w.value, self.h.value), SRCALPHA)


    def update(self, x_container, y_container, w_container, h_container):
        self.x.update_value(None, None, None, None, w_container, h_container, x_container)
        self.y.update_value(None, None, None, None, w_container, h_container, y_container)
        self.w.update_value(None, None, None, None, w_container, h_container, 0)
        self.h.update_value(None, None, None, None, w_container, h_container, 0)
        
        self.surface = Surface((self.w.value, self.h.value), SRCALPHA)


    def fill(self, *args):
        self.surface.fill(*args)
    
    
    def blit(self, *args):
        self.surface.blit(*args)


    def get_attributes(self):
        return {
            "source" : self.surface,
            "dest" : (self.x.value, self.y.value),
        }