import os
# Disable pygame welcome message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from pygame.locals import DOUBLEBUF, RESIZABLE, FULLSCREEN
import numpy as np
import ctypes

from UI_ELEMENTS.shapes import RectAle, LineAle, CircleAle, SurfaceAle
from UI_ELEMENTS.event_tracker import EventTracker

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
            self.w_screen: int = 1920
            self.w_viewport: int = 800
            self.h_screen: int = 1080
            self.h_viewport: int = 600
            self.initialized: bool = True  # Ensure it doesn't reinitialize

class App:
    def __init__(self, debug=False):
        self.running: bool
        self.debug: bool = debug
        self.UI: dict[str, Container] = {}
        self.render_buffer: list = []
        self.sizes = AppSizes()


    def launch(self):
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
        self.root_window = pygame.display.set_mode((self.sizes.w_viewport, self.sizes.h_viewport), DOUBLEBUF | RESIZABLE)


    def close(self):
        self.running = False


    def update(self):
        pygame.display.set_caption(f"FPS: {self.clock.get_fps():.2f}")
        
        self.get_events()
        self.render()

        self.clock.tick(self.max_fps)  


    def update_coords_UI_elements(self):
        for nome, elemento in self.UI.items():
            elemento.analyze_coordinate()


    def render(self):        
        self.root_window.fill((25, 25, 25))
        self.parse_UI_elements()
        self.render_elements()

        # Swap buffers to display
        pygame.display.flip()


    def parse_UI_elements(self):
        self.render_buffer = []
        for nome, elemento in self.UI.items():
            self.render_buffer.extend(elemento.get_render_objects())
        

    def render_elements(self):

        for object in self.render_buffer:
            if type(object) == RectAle:
                if object.is_opengl:
                    pygame.draw.rect(self.root_window, **object.get_mapped_attributes())  
                else:
                    pygame.draw.rect(self.root_window, **object.get_attributes())  
            elif type(object) == LineAle:
                if object.is_opengl:
                    pygame.draw.line(self.root_window, **object.get_mapped_attributes())   
                else:
                    pygame.draw.line(self.root_window, **object.get_attributes())   
            elif type(object) == CircleAle:
                if object.is_opengl:
                    pygame.draw.circle(self.root_window, **object.get_mapped_attributes())
                else:
                    pygame.draw.circle(self.root_window, **object.get_attributes())
            elif type(object) == SurfaceAle:
                if object.is_opengl:
                    self.root_window.blit(**object.get_mapped_attributes())
                else:
                    self.root_window.blit(**object.get_attributes())

        self.render_buffer = []


    def get_events(self):
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
