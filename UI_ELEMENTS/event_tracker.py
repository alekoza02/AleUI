import pygame
import time
import numpy as np

class EventTracker:
    _shared_state = {}  # Shared state across instances

    def __init__(self):
        self.__dict__ = self._shared_state  # Make all instances share the same state

        # Initialize only once
        if not hasattr(self, "initialized"):
            self.last_click_time = 0
            self.click_count = 0  # Tracks number of successive clicks
            self.dragging = False
            self.drag_start_time = 0
            self.drag_start_pos = (0, 0)
            self.mouse_pos = (0, 0)
            
            self.dt = 0
            
            self.total_drag_distance = 0
            self.key_press_times = {}
            self.scrolled = 0
            self.request_for_window_update = False
            self.initialized = True  # Ensure it doesn't reinitialize

            # special KEYS
            self.ctrl = False
            self.shift = False
            self.backspace = False
            self.left = False
            self.right = False
            self.tab = False

            self.acc_backspace = 0
            self.acc_left = 0
            self.acc_right = 0
    

    def track_special_keys(self):
        keys = pygame.key.get_pressed()
        self.ctrl = keys[pygame.K_LCTRL]
        self.shift = keys[pygame.K_LSHIFT]
        self.backspace = keys[pygame.K_BACKSPACE]
        self.left = keys[pygame.K_LEFT]
        self.right = keys[pygame.K_RIGHT]
        self.tab = keys[pygame.K_TAB]


    def track_mouse_events(self, event):
        """Tracks dragging, click timing, and double/triple click detection."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            current_time = time.time()
            time_since_last_click = current_time - self.last_click_time

            if time_since_last_click < 0.3:  # Double/triple click threshold (300ms)
                self.click_count += 1
            else:
                self.click_count = 1  # Reset if too much time passed

            self.last_click_time = current_time

            # Store dragging start info
            self.dragging = True
            self.drag_start_time = current_time
            self.drag_start_pos = event.pos
            self.total_drag_distance = 0

            # scroll info
            if event.button == 4:
                self.scrolled += 1
            if event.button == 5:
                self.scrolled -= 1

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            dx = event.pos[0] - self.drag_start_pos[0]
            dy = event.pos[1] - self.drag_start_pos[1]
            self.total_drag_distance += (dx**2 + dy**2) ** 0.5  # Euclidean distance

        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
            

    def get_local_drag_start_pos(self, offset):
        return [self.drag_start_pos[0] - offset[0], self.drag_start_pos[1] - offset[1]]


    def get_local_mouse_pos(self, offset):
        return [self.mouse_pos[0] - offset[0], self.mouse_pos[1] - offset[1]]


    def reset(self):
        self.scrolled = 0


    def track_keyboard_events(self, event):
        """Tracks key press duration and repetition rate."""
        if event.type == pygame.KEYDOWN:
            self.key_press_times[event.key] = time.time()

        elif event.type == pygame.KEYUP:
            if event.key in self.key_press_times:
                hold_duration = time.time() - self.key_press_times[event.key]
                del self.key_press_times[event.key]
                return hold_duration
        return None


    def get_click_info(self):
        """Returns number of fast successive clicks (1 = single, 2 = double, etc.)."""
        return self.click_count


    def get_drag_info(self):
        """Returns drag duration and distance."""
        if self.dragging:
            return {
                "duration": time.time() - self.drag_start_time,
                "distance": self.total_drag_distance,
                "start_pos": self.drag_start_pos
            }
        return None
    

    def get_scroll_info(self):
        return self.scrolled
