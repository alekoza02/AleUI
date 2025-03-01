import os
# Disable pygame welcome message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from pygame.locals import DOUBLEBUF, RESIZABLE, FULLSCREEN
import numpy as np
import ctypes

from UI_ELEMENTS.shapes import RectAle, LineAle, CircleAle, SurfaceAle

DO_NOT_EXECUTE = False
if DO_NOT_EXECUTE:
    from UI_ELEMENTS.base_element import BaseElementUI

class App:
    def __init__(self, debug=False):
        self.running: bool
        self.debug: bool = debug
        self.UI: dict[str, BaseElementUI] = {}
        self.render_buffer: list = []


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

        # DPI aware (windows)
        ctypes.windll.user32.SetProcessDPIAware()
        screen_info = pygame.display.Info()
        scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100

        # Screen's settings
        self.w_screen: int = int(screen_info.current_w * scale_factor)
        self.h_screen: int = int(screen_info.current_h * scale_factor)

        self.w, self.h = self.w_screen * 0.9, self.h_screen * 0.9

        # Window generation
        self.root_window = pygame.display.set_mode((self.w, self.h), DOUBLEBUF | RESIZABLE)


    def close(self):
        self.running = False


    def update(self):
        pygame.display.set_caption(f"FPS: {self.clock.get_fps():.2f}")
        
        self.get_events()
        self.render()

        self.clock.tick(self.max_fps)  


    def update_coords_UI_elements(self):
        for nome, elemento in self.UI.items():
            elemento.analyze_coordinate(self.w_screen, self.h_screen, self.w, self.h, None, None)


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
                pygame.draw.rect(self.root_window, **object.get_attributes())  
            elif type(object) == LineAle:
                pygame.draw.line(self.root_window, **object.get_attributes())   
            elif type(object) == CircleAle:
                pygame.draw.circle(self.root_window, **object.get_attributes())
            elif type(object) == SurfaceAle:
                self.root_window.blit(**object.get_attributes())

        self.render_buffer = []


    def get_events(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.close()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    # Toggle fullscreen on F11 (for example)
                    self.toggle_fullscreen()

            if event.type == pygame.VIDEORESIZE:
                # if not self.fullscreen:
                self.w, self.h = event.w, event.h
                self.update_coords_UI_elements()


    def toggle_fullscreen(self):
        if self.fullscreen:
            self.w, self.h = self.w_screen * 0.9, self.h_screen * 0.9
            self.root_window = pygame.display.set_mode((self.w, self.h), DOUBLEBUF | RESIZABLE)
            self.update_coords_UI_elements()
        else:
            self.w, self.h, = self.w_screen, self.h_screen
            self.root_window = pygame.display.set_mode((self.w, self.h), DOUBLEBUF | FULLSCREEN)
            self.update_coords_UI_elements()
            
        self.fullscreen = not self.fullscreen
