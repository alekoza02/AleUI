import pygame
import numpy as np
import ctypes
from UI_ELEMENTS.shapes import ComplexShape, RectAle, LineAle, CircleAle
from UI_ELEMENTS.smart_coordinate import SmartCoordinate

from AleUI import AppSizes 

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
        self.shape.add_shape("_highlight", RectAle("0cw -1px", "0ch -1px", "100cw 2px", "100ch 2px", [100, 100, 100], 1, 2))
        self.bounding_box: pygame.Rect = pygame.Rect(self.x.value, self.y.value, self.w.value, self.h.value)

        self.componenets: dict[str, BaseElementUI] = {}     # this attribute determines if an element has other elements for its working
        self.child_elements: dict[str, BaseElementUI] = {}     # this attribute determines if an element has child elements

        self.has_child_or_components = False
        self.element_highlighted = None
        self.element_selected = None

        self.is_hover = False
        self.is_hover_old = False

        self.parent_object: None | BaseElementUI = None

        self.is_enabled = True
        self.is_highlighted = False
        self.is_selected = False
        self.commands_stack = {}


        self.depth_level = None


    @property
    def total_children(self):
        return {**self.componenets, **self.child_elements}

    
    @property
    def total_children_indices(self):
        return [key for key in self.total_children.keys()]


    def ask_enable_disable_element(self, enable: bool=True, priority: int=1):
        '''
        Give a bigger priority to overcome other commands.
        '''
        self.commands_stack[priority] = enable

        max_priority = -1
        result = enable
        for priority, comand in self.commands_stack.items():
            if priority > max_priority and comand == False:
                max_priority = priority
                result = comand

        self.is_enabled = result


    def set_parent(self, anchor_object: 'BaseElementUI', parent_origin: str, offset_x: str, offset_y: str):
        '''
        Not implemented yet.
        '''
        self.anchor_mode = 'relative'
        self.anchor_object = anchor_object
        self.anchor_origin = parent_origin
        self.offset_x = SmartCoordinate(offset_x)
        self.offset_y = SmartCoordinate(offset_y)


    def analyze_coordinate(self, offset_x=0, offset_y=0) -> None:

        sizes = AppSizes()
        w_screen = sizes.w_screen
        h_screen = sizes.h_screen
        w_viewport = sizes.w_viewport
        h_viewport = sizes.h_viewport

        if not self.parent_object is None:
            w_container, h_container = self.parent_object.w.value, self.parent_object.h.value
        else:
            w_container, h_container = None, None

        if self.anchor_mode == 'relative':
            pos_info = self.anchor_object.get_xy_of_origin(self.anchor_origin)
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
        if self.is_enabled:
            output_shapes = self.shape.get_shapes()

            # removes the _highlight element, which by initialization is always the first one to be created
            if not (self.is_highlighted or self.is_selected): 
                output_shapes.pop(0) 
            
            # sets the color of the selection
            elif self.is_selected: 
                output_shapes[0].color = [200, 150, 100]

            # sets the color of the highligh
            elif self.is_highlighted: 
                # print(f"{self = }")
                output_shapes[0].color = [100, 100, 100]

            return output_shapes
        else:
            return []
        

    def handle_events(self, events):
        ...

    def launch_tab_action(self):
        ...


    # -------------------------------------------------------------------------------------------------------------------------
    # REGION OF RECURSIVE CHILDREN ELEMENTS
    # -------------------------------------------------------------------------------------------------------------------------
    
    def get_highlighted_element(self) -> 'BaseElementUI':
        return self.total_children[self.total_children_indices[self.element_highlighted]]
        
    def get_highlighted_element_index(self) -> str:
        return self.total_children_indices[self.element_highlighted]


    def _event_handle_select_highlight_movements(self, events):

        # Stato di tutti i tasti
        keys = pygame.key.get_pressed()
    
        for event in events:
            # MOVE WITH TAB & SHIFT + TAB
            if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB: 

                # always initialized to None, this is the inizialization of the first element
                if self.element_highlighted is None:
                    self.element_highlighted = -1

                # find the highlighted element
                highlighted_child = self.get_highlighted_element()
                
                # if the child is selected
                if highlighted_child.is_selected:
                    # if the child doesn't have other children
                    if not highlighted_child.has_child_or_components:
                        # removes selection (just in case) and moves to the next element and highlights
                        self._event_remove_selection()
                        self.highlight_next_element(keys)
                    # if the child has other children
                    else:
                        # calls the same funcion on the child
                        highlighted_child._event_handle_select_highlight_movements(events)
                # if the child is NOT selected
                else:
                    # highlights the next element
                    self.highlight_next_element(keys)


            # SELECT OR EXECUTE WITH ENTER
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:

                if not self.element_highlighted is None:
                    
                    highlighted_child = self.get_highlighted_element()
                    
                    if highlighted_child.is_selected:
                        if highlighted_child.has_child_or_components:
                            highlighted_child._event_handle_select_highlight_movements(events)
                        else:
                            # executes default behaviour (unique for each class)
                            self._event_execute_child_element(self.get_highlighted_element_index())
                    else:
                        # selects the element
                        highlighted_child.is_selected = True
                        # if the element has childs puts the highlight on the first one
                        if highlighted_child.has_child_or_components:
                            list(highlighted_child.total_children.values())[0].is_highlighted = True
                            highlighted_child.element_highlighted = 0
                

            # DESELECT WITH ESCAPE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:

                if not self.element_highlighted is None:

                    highlighted_child = self.get_highlighted_element()
                    
                    if highlighted_child.is_selected:
                        if highlighted_child.has_child_or_components:
                            # checks if there's at least one child selected 
                            check_if_exist_selected = [item.is_selected for item in list(highlighted_child.total_children.values())]
                            if sum(check_if_exist_selected) > 0:
                                highlighted_child._event_handle_select_highlight_movements(events)
                            else:
                                # if there's no selected, removes the highlight and selection
                                self._event_remove_selection()
                                for key, element in highlighted_child.total_children.items():
                                    element.is_highlighted = False
                        else:
                            self._event_remove_selection()
                    
                    else:
                        highlighted_child.is_highlighted = False
                        self.element_highlighted = None
                        

    def _event_execute_child_element(self, key):
        self.total_children[key].is_selected = True
        self.total_children[key].is_highlighted = True
        self.total_children[key].launch_tab_action()


    def _event_highlight_child_element(self, key):
        for name, value in self.total_children.items():
            value.is_highlighted = key == name


    def _event_reset_tab_movements(self):
        if self.has_child_or_components:
            for key, value in self.total_children.items():
                value._event_reset_tab_movements()
        
        self.is_highlighted = False
        self.is_selected = False
        self.element_highlighted = None
        self.element_selected = None


    def _event_remove_selection(self):
        if not self.element_highlighted is None:
            highlighted_child = self.get_highlighted_element()
                
            if highlighted_child.is_selected:
                highlighted_child.is_selected = False


    def highlight_next_element(self, keys):
        if keys[pygame.K_LSHIFT]:
            # go to previous
            if self.element_highlighted == 0:
                self.element_highlighted = len(self.total_children) - 1
            else:
                self.element_highlighted -= 1
        else:
            # go to next
            if self.element_highlighted + 1 == len(self.total_children):
                self.element_highlighted = 0
            else:
                self.element_highlighted += 1

        self._event_highlight_child_element(self.get_highlighted_element_index())