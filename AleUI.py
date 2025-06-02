import os
# Disable pygame welcome message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from pygame.locals import DOUBLEBUF, RESIZABLE, FULLSCREEN
import numpy as np
import ctypes
import psutil
from time import strftime

from UI_ELEMENTS.shapes import RectAle, LineAle, CircleAle, SurfaceAle
from UI_ELEMENTS.event_tracker import EventTracker
from UI_ELEMENTS.CPU_data import CPU_performance

DO_NOT_EXECUTE = False
if DO_NOT_EXECUTE:
    from UI_ELEMENTS.base_element import BaseElementUI
    from UI_ELEMENTS.element_container import Container


class AppSizes:
    _shared_state = {}  # Shared state across instances

    def __init__(self):
        self.__dict__ = self._shared_state  # Make all instances share the same state

        # Initialize only once
        if not hasattr(self, "initialized"):
            self._w_screen: int = 1920
            self._w_viewport: int = 800
            self._h_screen: int = 1080
            self._h_viewport: int = 600
            self.initialized: bool = True  # Ensure it doesn't reinitialize


    @property
    def w_screen(self):
        return int(self._w_screen)
    
    @w_screen.setter
    def w_screen(self, new_w_screen):
        self._w_screen = new_w_screen
    
    @property
    def h_screen(self):
        return int(self._h_screen)
    
    @h_screen.setter
    def h_screen(self, new_h_screen):
        self._h_screen = new_h_screen
    
    @property
    def w_viewport(self):
        return int(self._w_viewport)
    
    @w_viewport.setter
    def w_viewport(self, new_w_viewport):
        self._w_viewport = new_w_viewport
    
    @property
    def h_viewport(self):
        return int(self._h_viewport)
    
    @h_viewport.setter
    def h_viewport(self, new_h_viewport):
        self._h_viewport = new_h_viewport



class App:
    def __init__(self, debug=False):
        self.running: bool
        self.debug: bool = debug
        self.UI: dict[str, Container] = {}
        self.render_buffer: dict[str, list[BaseElementUI]] = {}
        self.sizes = AppSizes()

        self.CPU_statistic = [0 for _ in range(300)] 
        self.CPU_usage = CPU_performance()
        self.CPU_start_time = 0
        self.CPU_end_time = 0
        self.CPU: str = ""
        self.MEMORY: str = ""
        self.TIME: str = ""
        self.FPS: str = ""
        self.BATTERY: str = ""


    def launch(self, program_name="AleUI"):
        '''
        Starting the program, initializes the root window.
        '''
        # Init attributes
        self.running: bool = True
        self.fullscreen: bool = False
        self.max_fps: int = 0
        self.current_fps: int = 0

        # Init pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        self.event_tracker: EventTracker = EventTracker()

        # DPI aware (windows)
        ctypes.windll.user32.SetProcessDPIAware()
        screen_info = pygame.display.Info()
        scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100

        # Screen's settings
        self.sizes.w_screen = int(screen_info.current_w * scale_factor)
        self.sizes.h_screen = int(screen_info.current_h * scale_factor)

        self.sizes.w_viewport, self.sizes.h_viewport = self.sizes.w_screen * 0.9, self.sizes.h_screen * 0.9

        # Window generation
        self.root_window = pygame.display.set_mode((self.sizes.w_viewport, self.sizes.h_viewport), DOUBLEBUF | RESIZABLE | pygame.HWSURFACE)

        # Cosmetics of the windows bar
        pygame.display.set_icon(pygame.image.load("TEXTURES/desktopp.ico"))  # Carica un'icona personalizzata
        pygame.display.set_caption(program_name)  # Cambia il titolo della finestra

        hwnd = pygame.display.get_wm_info()["window"]
        value = 1  # 0 = chiaro, 1 = scuro
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(ctypes.c_int(value)), 4)

        

    def close(self):
        self.running = False


    def update(self):
        self.current_fps = self.clock.get_fps()
        
        self.update_pc_attributes()
        self.get_events()
        self.render()

        self.event_tracker.dt = self.clock.tick(self.max_fps)  


    def update_coords_UI_elements(self):
        for nome, elemento in self.UI.items():
            elemento.analyze_coordinate()


    def render(self):        
        self.parse_UI_elements()
        self.render_elements()

        # Swap buffers to display
        pygame.display.flip()


    def parse_UI_elements(self):
        self.render_buffer = {}
        for nome, elemento in self.UI.items():
            self.render_buffer[nome] = elemento.get_render_objects()
        

    def render_elements(self):

        # color the background of the app
        self.root_window.fill((25, 25, 25))

        for key, single_render_buffer in self.render_buffer.items():
            # color the background of containers
            self.UI[key].clip_canvas.fill(self.UI[key].bg)
            
            active_clip_rect = None

            for object in single_render_buffer:

                attributes = object.get_attributes()
                
                # setup of the clipping region
                if attributes["clip_rect"] != active_clip_rect:
                    active_clip_rect = attributes["clip_rect"]
                    self.UI[key].clip_canvas.set_clip(active_clip_rect)

                if type(object) == RectAle:
                    pygame.draw.rect(self.UI[key].clip_canvas, **{k: v for k, v in attributes.items() if k != 'clip_rect'})  
                    
                elif type(object) == LineAle:
                    pygame.draw.line(self.UI[key].clip_canvas, **{k: v for k, v in attributes.items() if k != 'clip_rect'})   
                
                elif type(object) == CircleAle:
                    pygame.draw.circle(self.UI[key].clip_canvas, **{k: v for k, v in attributes.items() if k != 'clip_rect'})
                
                elif type(object) == SurfaceAle:
                    self.UI[key].clip_canvas.blit(**{k: v for k, v in attributes.items() if k != 'clip_rect'})

            def blit_partial_surfaces(): 
                '''Function made purely to monitor blit performances.'''       
                self.root_window.blit(self.UI[key].clip_canvas, (self.UI[key].x.value, self.UI[key].y.value))
            blit_partial_surfaces()

        self.render_buffer = {}


    def get_events(self):
        self.event_tracker.reset()
        self.event_tracker.track_special_keys()
        
        events = pygame.event.get()

        for event in events:

            # Update singleton state
            self.event_tracker.track_mouse_events(event)
            self.event_tracker.track_keyboard_events(event)

            if event.type == pygame.QUIT:
                self.close()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    # Toggle fullscreen on F11 (for example)
                    self.toggle_fullscreen()

            if event.type == pygame.VIDEORESIZE:
                # if not self.fullscreen:
                self.sizes.w_viewport, self.sizes.h_viewport = event.w, event.h
                self.update_coords_UI_elements()

        for index, item in self.UI.items():
            item.handle_events(events)


    def toggle_fullscreen(self):
        if self.fullscreen:
            self.sizes.w_viewport, self.sizes.h_viewport = self.sizes.w_screen * 0.9, self.sizes.h_screen * 0.9
            self.root_window = pygame.display.set_mode((self.sizes.w_viewport, self.sizes.h_viewport), DOUBLEBUF | RESIZABLE)
            self.update_coords_UI_elements()
        else:
            self.sizes.w_viewport, self.sizes.h_viewport, = self.sizes.w_screen, self.sizes.h_screen
            self.root_window = pygame.display.set_mode((self.sizes.w_viewport, self.sizes.h_viewport), DOUBLEBUF | FULLSCREEN)
            self.update_coords_UI_elements()
            
        self.fullscreen = not self.fullscreen


    def update_pc_attributes(self):
        
        valore = self.CPU_usage.get_usage()
        if not valore is None:
            self.CPU_statistic.pop(0)    
            self.CPU_statistic.append(valore)    
 
        if self.CPU_start_time == 0:
            self.CPU_start_time = pygame.time.get_ticks()
        self.CPU_end_time = pygame.time.get_ticks() 
            
        elapsed_time = self.CPU_end_time - self.CPU_start_time

        if elapsed_time > 500:

            self.MEMORY = f' Memory: {psutil.Process().memory_info().rss / 1024**2:>7.2f} MB' 
            
            if psutil.Process().memory_info().rss / 1024**2 > 4000:
                self.MEMORY = r"\#dc143c{" + self.MEMORY.testo + "}"
            
            # -----------------------------------------------------------------------------
            
            self.CPU_start_time = 0
            self.CPU_end_time = 0

            self.CPU = f" CPU: {sum(self.CPU_statistic) / len(self.CPU_statistic):>3.0f}%"

            if sum(self.CPU_statistic) / len(self.CPU_statistic) > 30 and sum(self.CPU_statistic) / len(self.CPU_statistic) <= 70:
                self.CPU = r"\#ffdd60{" + self.CPU + "}"

            if sum(self.CPU_statistic) / len(self.CPU_statistic) > 70:
                self.CPU = r"\#dc143c{" + self.CPU + "}"

            # -----------------------------------------------------------------------------
        
            self.FPS = f"FPS: {self.current_fps:>6.2f}" 
            
            if self.current_fps < 60 and self.current_fps >= 24:
                self.FPS = r"\#ffdd60{" + self.FPS + "}"

            if self.current_fps < 24:
                self.FPS = r"\#dc143c{" + self.FPS + "}"
        
            # -----------------------------------------------------------------------------
        
            self.TIME = f" {strftime("%X, %x")}"

            # -----------------------------------------------------------------------------

            battery = psutil.sensors_battery()

            if battery:
                
                simbolo_corretto = ""
                caso_simbolo = battery.percent // 10
                
                match caso_simbolo:
                    case 0: simbolo_corretto = "󰢟" if battery.power_plugged else "󰂎";   # 0%
                    case 1: simbolo_corretto = "󰢜" if battery.power_plugged else "󰁺";   # 10%
                    case 2: simbolo_corretto = "󰂆" if battery.power_plugged else "󰁻";   # 20%
                    case 3: simbolo_corretto = "󰂇" if battery.power_plugged else "󰁼";   # 30%
                    case 4: simbolo_corretto = "󰂈" if battery.power_plugged else "󰁽";   # 40%
                    case 5: simbolo_corretto = "󰢝" if battery.power_plugged else "󰁾";   # 50%
                    case 6: simbolo_corretto = "󰂉" if battery.power_plugged else "󰁿";   # 60%
                    case 7: simbolo_corretto = "󰢞" if battery.power_plugged else "󰂀";   # 70%
                    case 8: simbolo_corretto = "󰂊" if battery.power_plugged else "󰂁";   # 80%
                    case 9: simbolo_corretto = "󰂋" if battery.power_plugged else "󰂂";   # 90%
                    case 10: simbolo_corretto = "󰂅" if battery.power_plugged else "󰁹";  # 100%


                self.BATTERY = f"{simbolo_corretto} {battery.percent:>3}%"

                if battery.percent < 20 and battery.percent >= 10:
                    self.BATTERY = r"\#ffdd60{" + self.BATTERY + "}"

                if battery.percent < 10:
                    self.BATTERY = r"\#dc143c{" + self.BATTERY + "}"

            
            try:
                self.UI["STATS"].child_elements["CPU"].change_text(self.CPU)
                self.UI["STATS"].child_elements["MEMORY"].change_text(self.MEMORY)
                self.UI["STATS"].child_elements["FPS"].change_text(self.FPS)
                self.UI["STATS"].child_elements["TIME"].change_text(self.TIME)
                self.UI["STATS"].child_elements["BATTERY"].change_text(self.BATTERY)
            except KeyError:
                ...