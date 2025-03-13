import pygame
import numpy as np
import ctypes
from UI_ELEMENTS.shapes import ComplexShape, RectAle, LineAle, CircleAle
from UI_ELEMENTS.smart_coordinate import SmartCoordinate

# Informations about the coordinates:
# Xpx: size in pixels
# Xvw: size in percentage of the viewport's width
# Xvh: size in percentage of the viewport's height
# Xsw: size in percentage of the screen's width
# Xsh: size in percentage of the screen's height
# Xcw: size in percentage of the container's width
# Xch: size in percentage of the container's height

# Informations about the origins:
# left-up: top-left corner
# center-up: top-center corner
# right-up: top-right corner        
# left-center: center-left corner
# center-center: center-center corner
# right-center: center-right corner
# left-down: bottom-left corner
# center-down: bottom-center corner
# right-down: bottom-right corner

class BaseElementUI:
    def __init__(self, x, y, w, h, origin='left-up', performant=False):
        self.x: SmartCoordinate = SmartCoordinate(x)
        self.y: SmartCoordinate = SmartCoordinate(y)
        self.w: SmartCoordinate = SmartCoordinate(w)
        self.h: SmartCoordinate = SmartCoordinate(h)
        self.origin = origin
        self.anchor_mode = 'absolute'

        self.shape: ComplexShape = ComplexShape()
        self.bounding_box: pygame.Rect = pygame.Rect(self.x.value, self.y.value, self.w.value, self.h.value)

        self.is_hover = False
        self.is_hover_old = False


    def set_parent(self, obj_origin: str, parent_object: 'BaseElementUI', parent_origin: str, offset_x: str, offset_y: str):
        '''
        Not implemented yet.
        '''
        self.origin = obj_origin
        self.anchor_mode = 'relative'
        self.parent_object = parent_object
        self.parent_origin = parent_origin
        self.offset_x = SmartCoordinate(offset_x)
        self.offset_y = SmartCoordinate(offset_y)


    def analyze_coordinate(self, w_screen, h_screen, w_viewport, h_viewport, w_container=None, h_container=None, offset_x=0, offset_y=0) -> None:

        if self.anchor_mode == 'relative':
            pos_info = self.parent_object.get_xy_of_origin(self.parent_origin)
            self.offset_x.update_value(w_screen, h_screen, w_viewport, h_viewport, w_container, h_container, 0)
            self.offset_y.update_value(w_screen, h_screen, w_viewport, h_viewport, w_container, h_container, 0)
            
            self.x.lst_str_value = [f"{self.offset_x.value + pos_info[0]}px"]
            self.y.lst_str_value = [f"{self.offset_y.value + pos_info[1]}px"]


        # The offset position due to the container position should be ignored in 'relative' mode
        upd_offset_x = 0 if self.anchor_mode == 'relative' else offset_x
        upd_offset_y = 0 if self.anchor_mode == 'relative' else offset_y

        self.x.update_value(w_screen, h_screen, w_viewport, h_viewport, w_container, h_container, upd_offset_x)
        self.w.update_value(w_screen, h_screen, w_viewport, h_viewport, w_container, h_container, 0)
        self.y.update_value(w_screen, h_screen, w_viewport, h_viewport, w_container, h_container, upd_offset_y)
        self.h.update_value(w_screen, h_screen, w_viewport, h_viewport, w_container, h_container, 0)

        self.x.origin_correction(self.origin, self.w.value, "x")
        self.y.origin_correction(self.origin, self.h.value, "y")

        self.bounding_box = pygame.Rect(self.x.value, self.y.value, self.w.value, self.h.value)
        self.shape.update_shapes(self.x.value, self.y.value, self.w.value, self.h.value)
    

    def get_xy_of_origin(self, origin):
        match origin:
            case "left-up": return np.array([self.x.value, self.y.value])
            case "center-up": return np.array([self.x.value + self.w.value // 2, self.y.value])
            case "right-up": return np.array([self.x.value + self.w.value, self.y.value])
            case "left-center": return np.array([self.x.value, self.y.value + self.h.value // 2])
            case "center-center": return np.array([self.x.value + self.w.value // 2, self.y.value + self.h.value // 2])
            case "right-center": return np.array([self.x.value + self.w.value, self.y.value + self.h.value // 2])
            case "left-down": return np.array([self.x.value, self.y.value + self.h.value])
            case "center-down": return np.array([self.x.value + self.w.value // 2, self.y.value + self.h.value])
            case "right-down": return np.array([self.x.value + self.w.value, self.y.value + self.h.value])
            case _: raise SyntaxError(f"Invalid origin: {origin}")


    def get_render_objects(self):
        return self.shape.get_shapes()


    def handle_events(self, events):
        ...
