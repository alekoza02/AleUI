from UI_ELEMENTS.base_element import BaseElementUI
from UI_ELEMENTS.element_text_label import Label_text
from UI_ELEMENTS.shapes import RectAle, LineAle, CircleAle
from UI_ELEMENTS.animations import BaseAnimation
from MATH.utils import MateUtils
import pyperclip
import numpy as np

DO_NOT_EXECUTE = False
if not DO_NOT_EXECUTE:
    import pygame
    from pygame.event import Event
    from UI_ELEMENTS.event_tracker import EventTracker


class Entry(BaseElementUI):
    def __init__(self, x, y, w, h, origin=None, initial_text="Entry text"):
        super().__init__(x, y, w, h, origin)

        self.shape.reset()
        self.shape.add_shape("_highlight", RectAle("0cw -1px", "0ch -1px", "100cw 2px", "100ch 2px", [100, 100, 100], 1, 2))
        self.shape.add_shape("bg", RectAle("0cw", "0ch", "100cw", "100ch", [70, 70, 70], 0, 0))
        self.shape.add_shape("active", RectAle("1px", "1px", "100cw -2px", "100ch -2px", [70, 70, 70], 0, 0))
        
        self.offset_grafico_testo = 5
        self.shape.add_shape("pointer", RectAle(f"{self.offset_grafico_testo}px", "12.5ch", "2px", "75ch", [245, 10, 10], 0, 0))
        self.shape.add_shape("highlighted", RectAle("0px", "12.5ch", "0px", "75ch", MateUtils.hex2rgb("91b1ff"), 0, 0))
        
        self.componenets: dict[str, Label_text] = {
            "_title" : Label_text(f"{self.offset_grafico_testo}px", "0ch", f"100cw -{2 * self.offset_grafico_testo}px", "100ch", "left-up", text=initial_text, text_tag_support=False, text_centered_x=False, render_bg=False)
        }

        for key, value in self.componenets.items():
            value.parent_object = self

        self.toggled = False

        self.active_color = [138, 167, 245]


        # IMPORTED
        self.puntatore_pos = 0
        self.old_puntatore_pos = 0
        self.old_highlight_region: list[int] = [0, 0]
        self.highlight_region: list[int] = [0, 0]

        self.hover = False

        self.testo = initial_text
        self.previous_text: str = ""

        self.lunghezza_max = 20
        self.solo_numeri = False
        self.num_valore_minimo = 0
        self.num_valore_massimo = 1000
        self.is_hex = False
        self.input_error = False
        self.return_previous_text = False

        self.animazione_puntatore = BaseAnimation(1000, "loop")
        self.animazione_puntatore.attiva = True


    
    def get_state(self):
        return self.toggled                                                             


    def analyze_coordinate(self, offset_x=0, offset_y=0):
        super().analyze_coordinate(offset_x, offset_y)

        for name, child in self.componenets.items():
            child.analyze_coordinate(self.x.value, self.y.value)


    def handle_events(self, events: list['Event']):


        event_tracker: EventTracker = EventTracker()

        if self.is_enabled:
            if self.toggled:

                # handle self components events
                [element.handle_events(events) for index, element in self.componenets.items()]

                self.return_previous_text = True
                '''TO BE CONTINUED'''
                self.eventami_scrittura(events)
            

                if self.solo_numeri:
                    numero_equivalente = MateUtils.inp2flo(self.testo, None)

                    if numero_equivalente is None:
                        self.color_text = np.array([255, 0, 0])
                    else:
                        self.color_text = np.array([200, 200, 200])
            else:
                self.return_previous_text = False
                self.previous_text = self.testo


            if event_tracker.dragging and self.toggled:
                self.highlight_region[0] = self.get_puntatore_pos(event_tracker.get_local_mouse_pos(self.get_parent_local_offset())[0])
                self.highlight_region[1] = self.get_puntatore_pos(event_tracker.get_local_drag_start_pos(self.get_parent_local_offset())[0])
                self.update_puntatore_pos(event_tracker.get_local_mouse_pos(self.get_parent_local_offset()))
                self.animazione_puntatore.riavvia()


            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.change_state(self.bounding_box.collidepoint(event_tracker.get_local_mouse_pos(self.get_parent_local_offset())))

                    if self.toggled:
                        self.animazione_puntatore.riavvia()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB: 
                    self.handle_deselection()



            # Hover block #
            if self.bounding_box.collidepoint(event_tracker.get_local_mouse_pos(self.get_parent_local_offset())):
                self.is_hover_old = self.is_hover
                self.is_hover = True
            else:
                self.is_hover_old = self.is_hover
                self.is_hover = False
            
            
            if self.is_hover and self.is_hover != self.is_hover_old:
                self.shape.shapes["active"].color += 10
                self.shape.shapes["bg"].color += 10
                self.hover_sound(self.hover)
            elif not self.is_hover and self.is_hover != self.is_hover_old:
                self.shape.shapes["active"].color -= 10
                self.shape.shapes["bg"].color -= 10
            # Hover block #


    def change_state(self, new_state=None):

        if new_state is None:
            self.toggled = not self.toggled
        else:
            self.toggled = new_state
        
        if self.toggled: self.shape.change_shape_color("active", self.active_color)
        else: self.shape.change_shape_color("active", self.shape.shapes["bg"].color)


    def handle_deselection(self):
        self.change_state(False)
        return super().handle_deselection()


    def launch_tab_action(self):
        self.change_state()


    def get_render_objects(self):
        if self.is_enabled:
            ris = []

            # pointer flickering
            event = EventTracker()
            self.animazione_puntatore.update(event.dt)

            # updates the position of the pointer      
            if self.old_puntatore_pos != self.puntatore_pos:      
                offset_puntatore_pos = self.componenets["_title"].font.font_pixel_dim[0] * self.puntatore_pos
                self.old_puntatore_pos = self.puntatore_pos
                self.shape.shapes["pointer"].x.change_str_value(f"{self.offset_grafico_testo + offset_puntatore_pos}px")
                self.analyze_coordinate()

            # updates the visibility of the pointer
            self.shape.change_shape_visibility("pointer", (self.toggled and self.animazione_puntatore.dt < 500))

            # updates the size of the highlighted region
            if self.old_highlight_region[0] != self.highlight_region[0] or self.old_highlight_region[1] != self.highlight_region[1]:
                new_x_start = self.componenets["_title"].font.font_pixel_dim[0] * self.highlight_region[0]
                new_x_end = self.componenets["_title"].font.font_pixel_dim[0] * self.highlight_region[1]
                if new_x_start > new_x_end:
                    new_x_start, new_x_end = new_x_end, new_x_start

                new_w = abs(new_x_start - new_x_end)

                self.old_highlight_region = [i for i in self.highlight_region]
                self.shape.shapes["highlighted"].x.change_str_value(f"{self.offset_grafico_testo + new_x_start}px")
                self.shape.shapes["highlighted"].w.change_str_value(f"{new_w}px")
                self.analyze_coordinate()
                

            # adds himself
            ris.extend(super().get_render_objects())

            # adds text label
            for name, obj in self.componenets.items():            
                ris.extend(obj.get_render_objects())

            return ris
        else:
            return []

            

    '''
    IMPORTED BLOCK
    '''

    # def check_for_lost_focus(self, events, force_closure=False):

    #     if force_closure:
    #         self.toggled = False
    #         self.return_previous_text = False
    #         _ = self.get_text()         # update of the value to avoid lost info 

    #     for event in events:
    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             if event.button == 1:
    #                 if self.bounding_box.collidepoint(event.pos):
                        
    #                     if self.toggled:
    #                         self.highlight_region = [0, 0]
    #                         self.update_puntatore_pos(event.pos)
    #                     else:    
    #                         self.toggled = True
    #                         self.highlight_region = [len(self.testo), 0]
    #                         self.puntatore_pos = len(self.testo)

    #                     self.animazione_puntatore.riavvia()

    #                 else:
    #                     self.toggled = False
    #                     self.highlight_region = [0, 0]
                        

    #         if event.type == pygame.MOUSEBUTTONUP:
    #             if event.button == 1:
    #                 if self.bounding_box.collidepoint(event.pos):
    #                     if self.toggled:
    #                         if self.do_stuff and not self.sound_select is None: self.sound_select.play()
    #                         self.animazione_puntatore.riavvia()


    def eventami_scrittura(self, events: list['Event']):
        
        if self.is_enabled:
        
            event_tracker = EventTracker()

            old_text = self.testo

            def move_selected(dir: bool, amount: int = 1):
                if dir:
                    if self.highlight_region == [0, 0]:
                        self.highlight_region = [self.puntatore_pos, self.puntatore_pos]

                    if self.highlight_region[0] < len(self.testo):
                        self.highlight_region[0] += amount
                
                else:
                    if self.highlight_region == [0, 0]:
                        self.highlight_region = [self.puntatore_pos, self.puntatore_pos]

                    if self.highlight_region[0] > 0:
                        self.highlight_region[0] -= amount


            def find_ricercatore(self: Entry, dir: bool):

                elenco_ricercatori = [" ", "\\", "/", ",", ".", "-", "{", "}", "[", "]", "(", ")"]

                if dir:
                    # movimento verso destra
                    dst = len(self.testo)
                    for ricercatore in elenco_ricercatori:
                        candidato = self.testo.find(ricercatore, self.puntatore_pos + 1)
                        if candidato >= 0:
                            dst = min(candidato, dst)

                else:
                    # movimento verso sinistra
                    dst = 0
                    for ricercatore in elenco_ricercatori:
                        candidato = self.testo[:self.puntatore_pos].rfind(ricercatore)
                        if candidato >= 0:
                            dst = max(candidato, dst)

                return dst


            reset_animation = False


            # SINGOLI TASTI
            # --------------------------------------------------------------------------------------------------------------------------
            lunghezza_testo_execute = False

            if self.lunghezza_max is None:
                lunghezza_testo_execute = True
            
            elif len(self.testo) < self.lunghezza_max:
                lunghezza_testo_execute = True

            for event in events:
                
                if event.type == pygame.TEXTINPUT:

                    if lunghezza_testo_execute:
                        apertura = ""
                        chiusura = ""

                        if event.text == '{' or event.text == "[" or event.text == "(" or event.text == '"':
                            apertura = event.text
                            match event.text:
                                case "{": chiusura = "}"
                                case "[": chiusura = "]"
                                case "(": chiusura = ")"
                                case '"': chiusura = '"'



                        if self.highlight_region != [0, 0]:

                            min_s = min(self.highlight_region[0], self.highlight_region[1])
                            max_s = max(self.highlight_region[0], self.highlight_region[1])
                            
                            if apertura != "":
                                self.testo = self.testo[:min_s] + apertura + self.testo[min_s : max_s] + chiusura + self.testo[max_s:]
                                self.highlight_region[0] += 1
                                self.highlight_region[1] += 1
                                self.puntatore_pos += 1

                            else:
            
                                self.testo = self.testo[:min_s] + event.text + self.testo[max_s:]
                                self.puntatore_pos = len(self.testo[:min_s]) + len(event.text)
                                self.highlight_region = [0, 0]

                        else:
                            if apertura != "":
                                self.testo = self.testo[:self.puntatore_pos] + apertura + chiusura + self.testo[self.puntatore_pos:]
                            else:
                                self.testo = self.testo[:self.puntatore_pos] + event.text + self.testo[self.puntatore_pos:]
            
                            self.puntatore_pos += len(event.text)

                        
                        reset_animation = True
                
                if event.type == pygame.KEYDOWN:
                    # SOUND / AUDIO
                    # self.sound_typing.play()
                    
                    # copia, incolla e taglia       
                    if event_tracker.ctrl and event.key == pygame.K_c:
                        
                        min_s = min(self.highlight_region[0], self.highlight_region[1])
                        max_s = max(self.highlight_region[0], self.highlight_region[1])

                        pyperclip.copy(self.testo[min_s : max_s])
                    
                        self.highlight_region = [0, 0]

                    if lunghezza_testo_execute:
                        if event_tracker.ctrl and event.key == pygame.K_v:
                        
                            incolla = pyperclip.paste()
                            self.testo = f"{self.testo[:self.puntatore_pos]}{incolla}{self.testo[self.puntatore_pos:]}"
                            self.puntatore_pos = len(self.testo[:self.puntatore_pos]) + len(incolla)

                            self.highlight_region = [0, 0]
                    
                    if event_tracker.ctrl and event.key == pygame.K_x:
                        
                        if self.highlight_region != [0, 0]:
                            min_s = min(self.highlight_region[0], self.highlight_region[1])
                            max_s = max(self.highlight_region[0], self.highlight_region[1])

                            pyperclip.copy(self.testo[min_s : max_s])
                        
                            self.highlight_region = [0, 0]
                            
                            self.testo = self.testo[:min_s] + self.testo[max_s:]
                            self.puntatore_pos = len(self.testo[:min_s])
    

                    # HOME and END
                    if event.key == pygame.K_HOME:
                        if event_tracker.shift:
                            self.highlight_region = [self.puntatore_pos, 0]
                        else:
                            self.highlight_region = [0, 0]
                        self.puntatore_pos = 0
                        reset_animation = True

                    

                    if event.key == pygame.K_END:
                        if event_tracker.shift:
                            self.highlight_region = [self.puntatore_pos, len(self.testo)]
                        else:
                            self.highlight_region = [0, 0]
                        self.puntatore_pos = len(self.testo)
                        reset_animation = True

                    
                    # ESC
                    if event.key == pygame.K_ESCAPE:
                        self.highlight_region = [0, 0]


                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        reset_animation = True

                        if self.highlight_region[1] - self.highlight_region[0] != 0:

                            min_s = min(self.highlight_region[0], self.highlight_region[1])
                            max_s = max(self.highlight_region[0], self.highlight_region[1])

                            self.testo = self.testo[:min_s] + self.testo[max_s:]

                            self.puntatore_pos = min_s
                            self.highlight_region = [0, 0]

                        
                        elif event.key == pygame.K_DELETE:
                            if self.puntatore_pos < len(self.testo):
                                self.testo = self.testo[:self.puntatore_pos] + self.testo[self.puntatore_pos + 1:]

                        elif event.key == pygame.K_BACKSPACE:

                            if event_tracker.ctrl:

                                nuovo_puntatore = find_ricercatore(self, 0)

                                text2eli = self.testo[nuovo_puntatore : self.puntatore_pos]
                                self.puntatore_pos = nuovo_puntatore
                                self.testo = self.testo[:nuovo_puntatore] + self.testo[nuovo_puntatore:].replace(text2eli, "", 1)
                                
                            else:
                                if self.puntatore_pos != 0:
                                    self.testo = self.testo[:self.puntatore_pos-1] + self.testo[self.puntatore_pos:]
                                if self.puntatore_pos > 0:
                                    self.puntatore_pos -= 1
                            

                    if event.key == pygame.K_LEFT:

                        if self.puntatore_pos > 0:
                            
                            if event_tracker.ctrl:
                                
                                puntatore_left = find_ricercatore(self, 0)
                                
                                if event_tracker.shift:

                                    move_selected(0, self.puntatore_pos - puntatore_left)
                
                                else:
                                    reset_animation = True
                                    self.highlight_region = [0, 0]

                                self.puntatore_pos = puntatore_left

                            else: 

                                if event_tracker.shift:

                                    move_selected(0)
                
                                else:
                                    reset_animation = True
                                    self.highlight_region = [0, 0]

                                self.puntatore_pos -= 1


                    if event.key == pygame.K_RIGHT:

                        if self.puntatore_pos < len(self.testo):
                            
                            if event_tracker.ctrl:
                                
                                puntatore_right = find_ricercatore(self, 1)
                                
                                if event_tracker.shift:

                                    move_selected(1, puntatore_right - self.puntatore_pos)
                
                                else:
                                    reset_animation = True
                                    self.highlight_region = [0, 0]

                                self.puntatore_pos = puntatore_right

                            else: 

                                if event_tracker.shift:

                                    move_selected(1)
                
                                else:
                                    reset_animation = True
                                    self.highlight_region = [0, 0]

                                self.puntatore_pos += 1

                        else:
                            reset_animation = True
                            self.highlight_region = [0, 0]


            if event_tracker.backspace:
                event_tracker.acc_backspace += event_tracker.dt
                if event_tracker.acc_backspace > 500:
                    if self.puntatore_pos != 0:
                        self.testo = self.testo[:self.puntatore_pos-1] + self.testo[self.puntatore_pos:]
                    if self.puntatore_pos > 0:
                        self.puntatore_pos -= 1
                        reset_animation = True
                    event_tracker.acc_backspace -= 50
            else: 
                event_tracker.acc_backspace = 0

            if event_tracker.left:
                event_tracker.acc_left += event_tracker.dt
                if event_tracker.acc_left > 500:
                    reset_animation = True 
                    if self.puntatore_pos > 0:
                        self.puntatore_pos -= 1
                        if event_tracker.shift:
                            move_selected(0)
                    event_tracker.acc_left -= 50
            else: 
                event_tracker.acc_left = 0
            
            if event_tracker.right:
                event_tracker.acc_right += event_tracker.dt
                if event_tracker.acc_right > 500:
                    reset_animation = True
                    if self.puntatore_pos < len(self.testo):
                        self.puntatore_pos += 1
                        if event_tracker.shift:
                            move_selected(1)
                    event_tracker.acc_right -= 50
            else: 
                event_tracker.acc_right = 0

            if reset_animation:
                self.animazione_puntatore.riavvia()

            if old_text != self.testo:
                self.componenets["_title"].change_text(self.testo)

                # check for good measure
                if self.puntatore_pos > len(self.testo):
                    self.puntatore_pos = len(self.testo)


    def update_puntatore_pos(self, pos: tuple[int]):
        x, y = pos
        
        self.puntatore_pos = self.get_puntatore_pos(x)


    def get_puntatore_pos(self, x: int):
        ris = round((x - self.x.value - self.offset_grafico_testo) / (self.componenets["_title"].font.font_pixel_dim[0]))

        if ris > len(self.testo):
            ris = len(self.testo)
        elif ris < 0:
            ris = 0

        return ris
    

    def change_text(self, text):
        self.testo = text


    def get_text(self, real_time=False) -> str:
        
        if real_time:
            return f"{self.testo}"

        if self.return_previous_text:
            restituisco = f"{self.previous_text}"
        else:
            restituisco = f"{self.testo}"
        
        if self.solo_numeri:
            numero_equivalente = MateUtils.inp2flo(restituisco, None)

            if numero_equivalente is None:
                self.color_text = np.array([255, 0, 0])
                return self.num_valore_minimo

            else:
                self.color_text = np.array((200, 200, 200))

                if not self.num_valore_minimo is None and numero_equivalente > self.num_valore_massimo:
                    self.change_text(f"{self.num_valore_massimo}")
                    return self.get_text()
                elif not self.num_valore_massimo is None and numero_equivalente < self.num_valore_minimo:
                    self.change_text(f"{self.num_valore_minimo}")
                    return self.get_text()
                else:
                    return restituisco


        elif self.is_hex:
            if MateUtils.hex2rgb(restituisco, std_return=None) is None:
                self.color_text = np.array([255, 0, 0])
                return "aaaaaa"
            else:
                self.color_text = np.array([200, 200, 200])
                return restituisco

        else:
            return restituisco