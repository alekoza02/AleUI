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