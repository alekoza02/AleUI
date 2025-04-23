import os
# Disable pygame welcome message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from pygame.locals import DOUBLEBUF, RESIZABLE, FULLSCREEN, OPENGL
from OpenGL.GL import *


VERTEX_SHADER = """
#version 330 core
layout (location = 0) in vec2 position;
layout (location = 1) in vec4 in_color;
out vec4 v_color;
uniform vec2 screen_size;

void main() {
    vec2 normalized = position / screen_size * 2.0 - 1.0;
    normalized.y = -normalized.y; // Invert Y axis
    gl_Position = vec4(normalized, 0.0, 1.0);
    v_color = in_color;
}
"""
FRAGMENT_SHADER = """
#version 330 core
in vec4 v_color;
out vec4 FragColor;
void main() {
    FragColor = v_color;
}
"""

import numpy as np
from math import cos, sin

import ctypes
import psutil
from time import strftime

from UI_ELEMENTS.shapes import RectAle, LineAle, CircleAle, SurfaceAle
from UI_ELEMENTS.event_tracker import EventTracker
from UI_ELEMENTS.CPU_data import CPU_performance
from UI_ELEMENTS.resolution_structure import AppSizes
from UI_ELEMENTS.shapes import ComplexShape, RectAle, CircleAle, LineAle

DO_NOT_EXECUTE = False
if DO_NOT_EXECUTE:
    from UI_ELEMENTS.base_element import BaseElementUI
    from UI_ELEMENTS.element_container import Container


class App:
    def __init__(self, debug=False, program_name="AleUI"):
        self.running: bool
        self.debug: bool = debug
        self.UI: dict[str, Container] = {}
        self.render_buffer: dict[str, list[RectAle | CircleAle | LineAle]] = {}

        self.CPU_statistic = [0 for _ in range(300)] 
        self.CPU_usage = CPU_performance()
        self.CPU_start_time = 0
        self.CPU_end_time = 0
        self.CPU: str = ""
        self.MEMORY: str = ""
        self.TIME: str = ""
        self.FPS: str = ""
        self.BATTERY: str = ""

        info = self.detect_gpu_backend()
        if debug: 
            print("SYSTEM CHECK, RESULTS FOR GPU CALLS")
            for key, value in info.items(): 
                print(f"{key} : {value}")

        # self.is_opengl = False # Temporary developement on CPU
        self.is_opengl = info['has_opengl'] and not info['is_software_renderer'] and info['suitable_for_modern_opengl']
        self.sizes = AppSizes(self.is_opengl)

        if self.is_opengl:
            self.launch_GPU_based(program_name=program_name)
        else:
            self.launch_CPU_based(program_name=program_name)


    @staticmethod
    def detect_gpu_backend(min_gl_version=(3, 3)) -> dict:
        info = {
            "has_opengl": False,
            "is_software_renderer": True,
            "vendor": None,
            "renderer": None,
            "version": None,
            "reason": "No problems detected",
            "suitable_for_modern_opengl": False,
        }

        try:
            pygame.display.init()
            pygame.display.set_mode((1, 1), pygame.OPENGL | pygame.HIDDEN)

            vendor = glGetString(GL_VENDOR)
            renderer = glGetString(GL_RENDERER)
            version = glGetString(GL_VERSION)

            if not (vendor and renderer and version):
                info["reason"] = "Missing GL_* strings"
                return info

            vendor   = vendor.decode().strip()
            renderer = renderer.decode().strip().lower()
            version  = version.decode().strip()

            info["has_opengl"] = True
            info["vendor"] = vendor
            info["renderer"] = renderer
            info["version"] = version

            # Heuristic: check if it's software renderer
            sw_keywords = [
                "llvmpipe", "softpipe", "software rasterizer",
                "mesa x11", "microsoft", "gdi generic", "swiftshader",
                "angle (software)", "angle (swiftshader)"
            ]
            if any(kw in renderer for kw in sw_keywords):
                info["is_software_renderer"] = True
                info["reason"] = f"Renderer string contains fallback: {renderer}"
            else:
                info["is_software_renderer"] = False

            # Check for minimum GL version (for modern OpenGL)
            try:
                major, minor = map(int, version.split(".")[:2])
                if (major, minor) >= min_gl_version:
                    info["suitable_for_modern_opengl"] = True
            except:
                info["reason"] += " | Failed to parse GL version."

        except Exception as e:
            info["reason"] = f"OpenGL init failed: {e}"

        finally:
            pygame.display.quit()

        return info



    def launch_GPU_based(self, program_name):
        '''
        Initializes GPU-based rendering using OpenGL.
        '''
        # Init attributes
        self.running = True
        self.fullscreen = False
        self.max_fps = 0
        self.current_fps = 0

        pygame.init()
        self.clock = pygame.time.Clock()
        self.event_tracker = EventTracker()

        # DPI Aware (Windows)
        ctypes.windll.user32.SetProcessDPIAware()
        screen_info = pygame.display.Info()
        scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100

        self.sizes.w_screen = int(screen_info.current_w * scale_factor)
        self.sizes.h_screen = int(screen_info.current_h * scale_factor)
        self.sizes.w_viewport = int(self.sizes.w_screen * 0.9)
        self.sizes.h_viewport = int(self.sizes.h_screen * 0.9)

        # Create OpenGL window
        self.root_window = pygame.display.set_mode(
            (self.sizes.w_viewport, self.sizes.h_viewport),
            DOUBLEBUF | OPENGL | RESIZABLE
        )

        # === SHADER SETUP ===
        self.shader = create_shader_program(VERTEX_SHADER, FRAGMENT_SHADER)
        glUseProgram(self.shader)

        # Setup global uniforms
        screen_size_loc = glGetUniformLocation(self.shader, "screen_size")
        glUniform2f(screen_size_loc, self.sizes.w_viewport, self.sizes.h_viewport)

        glClearColor(0.1, 0.1, 0.1, 1.0)

        # Icon and window title
        pygame.display.set_icon(pygame.image.load("TEXTURES/desktopp.ico"))
        pygame.display.set_caption(program_name)

        hwnd = pygame.display.get_wm_info()["window"]
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(ctypes.c_int(1)), 4)

        # === GPU Buffer Setup ===
        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

        # Position attribute
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(0))

        # Color attribute
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(8))

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)


    def launch_CPU_based(self, program_name):
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
        if self.is_opengl:
            self.render_elements_GPU()
        else:
            self.render_elements_CPU()

        pygame.display.flip() # Swap buffers to display


    def parse_UI_elements(self):
        pygame.display.set_caption(f"{self.current_fps:.2f} FPS")
        self.render_buffer = {}
        for nome, elemento in self.UI.items():
            self.render_buffer[nome] = []

            if self.is_opengl:
                self.render_buffer[nome].extend([RectAle(0, 0, self.UI[nome].w.value, self.UI[nome].h.value, self.UI[nome].bg, 0, 0, is_opengl=True)])
            self.render_buffer[nome].extend(elemento.get_render_objects())
        

    def render_elements_CPU(self):

        # color the background of the app
        self.root_window.fill((25, 25, 25))

        for key, single_render_buffer in self.render_buffer.items():
            # color the background of containers
            self.UI[key].clip_canvas.fill(self.UI[key].bg)
            
            for object in single_render_buffer:

                attributes = object.get_attributes()                

                if type(object) == RectAle:
                    pygame.draw.rect(self.UI[key].clip_canvas, **attributes)  
                    
                elif type(object) == LineAle:
                    pygame.draw.line(self.UI[key].clip_canvas, **attributes)   
                
                elif type(object) == CircleAle:
                    pygame.draw.circle(self.UI[key].clip_canvas, **attributes)
                
                elif type(object) == SurfaceAle:
                    self.UI[key].clip_canvas.blit(**attributes)

            def blit_partial_surfaces(): 
                '''Function made purely to monitor blit performances.'''       
                self.root_window.blit(self.UI[key].clip_canvas, (self.UI[key].x.value, self.UI[key].y.value))
            blit_partial_surfaces()

        self.render_buffer = {}
    
    
    def render_elements_GPU(self):
        '''
        Gathers draw instructions and renders all elements using VBO.
        '''
        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(self.shader)

        # === RACCOLTA DATI ===
        vertices = []

        for key, buffer in self.render_buffer.items():
            
            # color the background of containers
            x_offset, y_offset = self.UI[key].x.value, self.UI[key].y.value 

            for obj in buffer:
                attributes = obj.get_attributes()

                if isinstance(obj, RectAle):
                    x, y = attributes["position"]
                    x, y = x + x_offset, y + y_offset
                    w, h = attributes["size"]
                    r, g, b = attributes["color"]
                    a = 1.0

                    vertices.extend([
                        # 1st triangle
                        x,     y,     r, g, b, a,
                        x + w, y,     r, g, b, a,
                        x + w, y + h, r, g, b, a,
                        # 2nd triangle
                        x,     y,     r, g, b, a,
                        x + w, y + h, r, g, b, a,
                        x,     y + h, r, g, b, a
                    ])

                elif isinstance(obj, LineAle):
                    x1, y1 = attributes["start"]
                    x1, y1 = x1 + x_offset, y1 + y_offset
                    x2, y2 = attributes["end"]
                    x2, y2 = x2 + x_offset, y2 + y_offset
                    r, g, b, a = attributes["color"]

                    vertices.extend([
                        x1, y1, r, g, b, a,
                        x2, y2, r, g, b, a
                    ])

                elif isinstance(obj, CircleAle):
                    cx, cy = attributes["center"]
                    cx, cy = cx + x_offset, cy + y_offset
                    radius = attributes["radius"]
                    r, g, b, a = attributes["color"]
                    num_segments = 36
                    for i in range(num_segments):
                        theta1 = 2 * np.pi * i / num_segments
                        theta2 = 2 * np.pi * (i + 1) / num_segments
                        x1, y1 = cx + radius * np.cos(theta1), cy + radius * np.sin(theta1)
                        x2, y2 = cx + radius * np.cos(theta2), cy + radius * np.sin(theta2)
                        vertices.extend([
                            cx, cy, r, g, b, a,
                            x1, y1, r, g, b, a,
                            x2, y2, r, g, b, a
                        ])


        # === UPLOAD + DRAW ===
        if vertices:
            vertex_data = np.array(vertices, dtype=np.float32)
            glBindVertexArray(self.VAO)
            glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
            glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_DYNAMIC_DRAW)
            glDrawArrays(GL_TRIANGLES, 0, len(vertex_data) // 6)
            glBindVertexArray(0)



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
                self.resize_update(event.w, event.h)

        for index, item in self.UI.items():
            item.handle_events(events)


    def toggle_fullscreen(self):
        if self.fullscreen:
            flags = DOUBLEBUF | RESIZABLE
            if self.is_opengl:
                flags |= OPENGL
            self.sizes.w_viewport, self.sizes.h_viewport = self.sizes.w_screen * 0.9, self.sizes.h_screen * 0.9
            self.root_window = pygame.display.set_mode((self.sizes.w_viewport, self.sizes.h_viewport), flags)
        else:
            flags = DOUBLEBUF | FULLSCREEN
            if self.is_opengl:
                flags |= OPENGL
            self.sizes.w_viewport, self.sizes.h_viewport, = self.sizes.w_screen, self.sizes.h_screen
            self.root_window = pygame.display.set_mode((self.sizes.w_viewport, self.sizes.h_viewport), flags)
            
        self.resize_update(self.sizes.w_viewport, self.sizes.h_viewport)
        self.fullscreen = not self.fullscreen


    def resize_update(self, new_w, new_h):
        glViewport(0, 0, new_w, new_h)
        self.update_coords_UI_elements()

        # === AGGIORNA UNIFORME NELLO SHADER ===
        screen_size_loc = glGetUniformLocation(self.shader, "screen_size")
        glUseProgram(self.shader)
        glUniform2f(screen_size_loc, new_w, new_h)


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


def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(shader).decode()
        raise RuntimeError(f"Shader compilation failed: {error}")
    return shader

def create_shader_program(vertex_shader_source, fragment_shader_source):
    vertex_shader = compile_shader(vertex_shader_source, GL_VERTEX_SHADER)
    fragment_shader = compile_shader(fragment_shader_source, GL_FRAGMENT_SHADER)
    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        error = glGetProgramInfoLog(program).decode()
        raise RuntimeError(f"Shader linking failed: {error}")
    return program
