from UI_ELEMENTS.base_element import BaseElementUI
from UI_ELEMENTS.shapes import RectAle, SurfaceAle
from math import ceil

DO_NOT_EXECUTE = False
if not DO_NOT_EXECUTE:
    import pygame
    from pygame.event import Event
    from UI_ELEMENTS.event_tracker import EventTracker
    from UI_ELEMENTS.element_text_label import Label_text
    from UI_ELEMENTS.element_button_toggle import Button_toggle


class Scroll(BaseElementUI):
    def __init__(self, x, y, w, h, origin='left-up', values=[], values_state=[], title="click me"):
        super().__init__(x, y, w, h, origin)

        self.shape.add_shape("bg", RectAle("0cw", "0ch", "100cw", "100ch", [40, 40, 40], 0, 0))
        self.shape.add_shape("bg_selectable", RectAle("0cw", "7.5ch", "100cw", "100ch -7.5ch", [50, 50, 50], 0, 0))
        
        self.componenets: dict[str, Label_text] = {
            "_title" : Label_text("3px", "0px", "100cw", "7.5ch", "left-up", text=title, text_tag_support=False, render_bg=False, text_centered_x=False)
        }

        for key, value in self.componenets.items():
            value.parent_object = self
        
        self.values = ["OUT OF RANGE", *values, "OUT OF RANGE"]
        self.values_state = [False, *values_state, False]
        self.values_options_height = 30  # unit in pixels
        self.values_options_number = 1   # avoid edge cases 
        self.values_first_visible_option = 0

        self.pixels_scrolled = 0       


    def handle_events(self, events: list['Event']):
            
        if self.is_enabled:
            # handle self components events
            [element.handle_events(events) for index, element in self.componenets.items()]
            
            # handle values options events
            [element.handle_events(events) for element in self.values_options]
            
            # handle values options events
            [element.handle_events(events) for element in self.values_representations]

            # get the latest events and relative positions
            tracker = EventTracker()

            if tracker.scrolled != 0 and self.bounding_box.collidepoint(tracker.get_local_mouse_pos(self.get_parent_local_offset())) and len(self.values) > self.values_options_number:
                
                if (tracker.scrolled > 0 and self.values_first_visible_option == 0):
                
                    for option, representation in zip(self.values_options, self.values_representations):
                        
                        option.y.lst_str_value[0] = f"{0}px"
                        representation.y.lst_str_value[0] = f"{0}px"

                    for child in self.values_options:
                        child.analyze_coordinate(self.x.value, self.y.value)
                    
                    for child in self.values_representations:
                        child.analyze_coordinate(self.x.value, self.y.value)


                elif (tracker.scrolled < 0 and self.values_first_visible_option == len(self.values) - self.values_options_number): 
                
                    for option, representation in zip(self.values_options, self.values_representations):
                        
                        old_y = option.y.lst_str_value[0] # Il primo valore è sempre rappresentato in px
                        new_y = max(int(old_y[:-2]) + int(tracker.scrolled * 2), (self.shape.shapes["bg_selectable"].h.value) - (self.values_options_number - 2) * self.values_options_height) # Smooth transition to max height

                        option.y.lst_str_value[0] = f"{new_y:.0f}px"
                        representation.y.lst_str_value[0] = f"{new_y:.0f}px"

                    for child in self.values_options:
                        child.analyze_coordinate(self.x.value, self.y.value)
                    
                    for child in self.values_representations:
                        child.analyze_coordinate(self.x.value, self.y.value)
                
                else:

                    set_index = 0
                    for index, option, representation in zip(range(len(self.values_options)), self.values_options, self.values_representations):
                        
                        old_y = option.y.lst_str_value[0] # Il primo valore è sempre rappresentato in px
                        new_y = int(old_y[:-2]) + int(tracker.scrolled * 2) # Il multiplier di tracker.scrolled indica la velocità
                        position_overflow = new_y // self.values_options_height
                        
                        if index == 0: set_index = position_overflow
                        
                        if position_overflow >= 1:
                            new_y -= position_overflow * self.values_options_height
                        elif position_overflow <= 0:
                            new_y -= position_overflow * self.values_options_height

                        option.y.lst_str_value[0] = f"{new_y}px"
                        representation.y.lst_str_value[0] = f"{new_y}px"
                        
                    if set_index >= 1: # Scroll in alto
                        self.set_first_index(self.values_first_visible_option - set_index)        
                    elif set_index <= 0: # Scroll in basso
                        self.set_first_index(self.values_first_visible_option - set_index)                        

                    for child in self.values_options:
                        child.analyze_coordinate(self.x.value, self.y.value)
                    
                    for child in self.values_representations:
                        child.analyze_coordinate(self.x.value, self.y.value)


            # update the number of visible options
            self.get_values_status()
            self.hide_unecessary_values()
            self.update_representations_appearence()

            # Hover block #
            if self.bounding_box.collidepoint(tracker.get_local_mouse_pos(self.get_parent_local_offset())):
                self.is_hover_old = self.is_hover
                self.is_hover = True
            else:
                self.is_hover_old = self.is_hover
                self.is_hover = False
            
            
            if self.is_hover and self.is_hover != self.is_hover_old:
                self.shape.shapes["bg"].color += 5
            elif not self.is_hover and self.is_hover != self.is_hover_old:
                self.shape.shapes["bg"].color -= 5
            # Hover block #


    def launch_tab_action(self):
        ...

    
    def analyze_coordinate(self, offset_x=0, offset_y=0):
        super().analyze_coordinate(offset_x, offset_y)
    
        for name, child in self.componenets.items():
            child.analyze_coordinate(self.x.value, self.y.value)
        
        number_changed = self.determine_number_of_visible_options()

        if number_changed:
            self.generate_values_options()
            
        for child in self.values_options:
            child.analyze_coordinate(self.x.value, self.y.value)
        
        for child in self.values_representations:
            child.analyze_coordinate(self.x.value, self.y.value)


    def get_render_objects(self):
        if self.is_enabled:
            ris = []
            
            # adds himself
            ris.extend(super().get_render_objects())
            
            # adds its components
            for name, obj in self.componenets.items():            
                ris.extend(obj.get_render_objects())
            
            # adds the values options
            for obj in self.values_options:            
                ris.extend(obj.get_render_objects())
            
            # adds the values options
            for obj in self.values_representations:            
                ris.extend(obj.get_render_objects())
            
            return ris
        else:
            return []
        

    def __repr__(self):
        return f"Scroll element containing {len(self.values)} elements and showing {self.values_options_number} objects. Starting index is {0}"
    

    def determine_number_of_visible_options(self) -> bool:
        old_values = self.values_options_number
        self.values_options_number =  ceil(self.shape.shapes["bg_selectable"].h.value / self.values_options_height) + 1
        return old_values != self.values_options_number
    

    def generate_values_options(self):
        self.values_options = [Button_toggle("2px", f"0px {self.values_options_height * (i - 1)}px 2px 7.5ch", f"{self.values_options_height - 4}px", f"{self.values_options_height - 4}px", "left-up", initial_status=False) for i in range(self.values_options_number)]
        self.values_representations = [Label_text("40px", f"0px {self.values_options_height * (i - 1)}px 2px 7.5ch", "100cw -45px", f"{self.values_options_height - 4}px", "left-up", text="", render_bg=False, text_centered_x=False) for i in range(self.values_options_number)]

        for value in self.values_options + self.values_representations:
            value.parent_object = self
            value.shape.set_clip_rect_parent(self.shape.shapes["bg_selectable"])

        self.update_visible_options()
        self.update_representations_appearence()

    
    def hide_unecessary_values(self):
        for i in range(len(self.values) - 1, self.values_options_number):
            self.values_options[i].ask_enable_disable_element(False, 2)
            self.values_representations[i].ask_enable_disable_element(False, 2)


    def get_values_status(self):
        self.values_state[self.values_first_visible_option : self.values_first_visible_option + self.values_options_number] = [button.get_state() for button in self.values_options]
        return self.values_state
    

    def update_representations_appearence(self):
        
        def update_single_element(state, label):
            color = "aaffaa" if state else "aaaaaa"
            string = label.text
            
            starting_index = string.find("\\#")

            if starting_index == -1:
                label.change_text(f"\\#{color}{{" + string + "}")
            else:
                old_state = None
                if string.find("aaaaaa") != -1:
                    old_state = False
                if string.find("aaffaa") != -1:
                    old_state = True

                if old_state != state:
                    string = string[:starting_index] + f"\\#{color}" + string[starting_index + 8:]
                    label.change_text(string)

        for state, label in zip(self.values_state[self.values_first_visible_option : self.values_first_visible_option + self.values_options_number], self.values_representations):
            update_single_element(state, label)
    

    def set_first_index(self, value):
        if value < 0 or value > len(self.values) - self.values_options_number + 1:
            return
        
        old_index = self.values_first_visible_option
        self.values_first_visible_option = value

        if old_index != self.values_first_visible_option:
            self.update_visible_options()
            

    def update_visible_options(self):
        
        for value_index in range(self.values_options_number):

            # General button case
            if value_index + self.values_first_visible_option < len(self.values):

                value = self.values[value_index + self.values_first_visible_option]
                state = self.values_state[value_index + self.values_first_visible_option]

                self.values_options[value_index].set_state(state)
                self.values_representations[value_index].change_text(value)