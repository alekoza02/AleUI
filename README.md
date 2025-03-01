# HIGHLY EFFICIENT User Interface (AleUI)

Optimized UI written in PyGame. Still in developement.  
Frame-work for developement of POMOSHNIK.  
Documentation and FlowCharts in `docs`.

# TEST

You can use the `demo.py` to try the UI.

# INSTALLATION

Launch `pip install -r requirements.txt` to install all dependencies.  
To use new fonts, insert them in the folder `TEXTURES`.

# FEATURES

Tree structure:
--
All the elements of the UI must be contained in a container, which are bounded to the main window.

- Window:  
    - Containers:  
        - Label_text  
        - Button_toggle  
        - Button_push    

Coordinates:
--
- `px` size in pixels
- `sw` percentage of the 'width' of the physical screen
- `sh` percentage of the 'height' of the physical screen
- `vw` percentage of the 'width' of the viewport (window)
- `vh` percentage of the 'height' of the viewport (window)
- `cw` percentage of the 'width' of the container
- `ch` percentage of the 'height' of the container

Anchor points:
--
- `left-up`: top-left corner
- `center-up`: top-center corner
- `right-up`: top-right corner        
- `left-center`: center-left corner
- `center-center`: center-center corner
- `right-center`: center-right corner
- `left-down`: bottom-left corner
- `center-down`: bottom-center corner
- `right-down`: bottom-right corner