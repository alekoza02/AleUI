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

- `Window` (can contain only `Containers`):  
    - `Containers` (cannot contain other `Containers`):  
        - `Collapse_windows` (cannot contain other `Collapse_windows`)
            - Label_text  
            - Button_toggle  
            - Button_push    
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

# UI Elements overview and future implementations:

Label_text:
--
- Cosmetic:
    - $[\text{X}]$ Bloom
    - $[\text{X}]$ Rotations
    - $[\text{X}]$ Japanese writing
    - $[\text{X}]$ Enable slide to show text if not fitting

- Functionality:
    - $[\text{X}]$ Choose font
    - $[\checkmark]$ Choose size
    - $[\checkmark]$ Choose color
    - $[\checkmark]$ Raw strings (simple-mode)
    - $[\checkmark]$ Tag support (complex-mode)
    - $[\checkmark]$ Clip of the text on fixed size
    - $[\text{X}]$ Adapt the size of the label to the text size
    - $[\checkmark]$ Center on X and-or Y of a given size
    - $[\checkmark]$ Support multi-line (complex-mode)
    - $[\text{X}]$ Automatic new line insertion
    - $[\text{X}]$ Selectable for copy
    - $[\checkmark]$ Select through $\textit{`tab'}$

- Limitations:

    | Feature | Simple Mode | Hard Mode |
    |:-------|:------:|:------:|
    | Tags | N | Y |
    | Auto newline | Y | N |
    | Fixed Auto-center X | Y | N |
    | Fixed Auto-center Y | Y | N |
    | Label Resize X | Y | Y |
    | Label Resize Y | Y | Y |

Button_push:
--
- Cosmetic:
    - $[\text{X}]$ Click effect
    - $[\text{X}]$ Click sound
    - $[\text{X}]$ Hover effect
    - $[\text{X}]$ Hover sound
    - $[\text{X}]$ Outline

- Functionality:
    - $[\checkmark]$ Accept function to execute
    - $[\checkmark]$ Select through $\textit{`tab'}$
    - $[\checkmark]$ Activate with $\textit{`enter'}$

Button_toggle:
--
- Cosmetic:
    - $[\text{X}]$ Click effect
    - $[\text{X}]$ Click sound
    - $[\text{X}]$ Hover effect
    - $[\text{X}]$ Hover sound
    - $[\text{X}]$ Outline
    - $[\text{X}]$ Different styles:
        - $[\checkmark]$ Classic label
        - $[\text{X}]$ Check mode
            - $[\text{X}]$ Labels on left side
            - $[\text{X}]$ Labels on right side
        - $[\text{X}]$ Switch mode

- Functionality:
    - $[\checkmark]$ Select through $\textit{`tab'}$
    - $[\checkmark]$ Activate with $\textit{`enter'}$

Multi_button:
--
- Cosmetic:
    - $[\text{X}]$ Show background of the Bounding Box

- Functionality:
    - $[\text{X}]$ Support single answer
    - $[\text{X}]$ Support multiple answers
    - $[\text{X}]$ Get state of all buttons
    - $[\text{X}]$ Set state of all buttons
    - $[\text{X}]$ Select through $\textit{`tab'}$ which iterates between children
    - $[\text{X}]$ Activate with $\textit{`enter'}$

Entry_box:
--
- Cosmetic:
    - $[\checkmark]$ Text clipped outside the Bounding Box
    - $[\checkmark]$ Intermitting pointer with reset when starting writing
    - $[\text{X}]$ Title of the entry box 
    - $[\checkmark]$ Default text

- Functionality:
    - $[\checkmark]$ Select through $\textit{`tab'}$ (goes to next if no autocompletion)   
    - $[\text{X}]$ Basic autocompletion with $\textit{`tab'}$
    - $[\text{X}]$ Minimum delay of autocompletion
    - $[\text{X}]$ Show possible autocompletion + choosing with arrows
    - $[\text{X}]$ Offset the entry string to show different parts of the input (small entry box, big string)
    - $[\text{X}]$ Check for hex values
    - $[\text{X}]$ NUMBERS:
        - $[\text{X}]$ Check for digits only
        - $[\text{X}]$ Check for correct range of values (in case of digits only)
        - $[\text{X}]$ Slider behaviour to change  by continueous values
        - $[\text{X}]$ Arrows on the sides to change value by discrete values
    - $[\text{X}]$ Set maximum lenght of the entry string
    - $[\text{X}]$ Copy, Paste, Cut
    - $[\text{X}]$ Copy with mouse hover
    - $[\text{X}]$ Copy with right click
    - $[\text{X}]$ Selection with mouse

Scroll_elements:
--
- Cosmetic:
    - $[\text{X}]$ Show line of where a dragged element is goind to land
- Functionality:
    - $[\text{X}]$ Activate / Deactivate elements using toggles
    - $[\text{X}]$ Activate / Deactivate elements by dragging on the toggles
    - $[\text{X}]$ Activate / Deactivate elements with $\textit{`enter'}$
    - $[\text{X}]$ Move with mouse wheel
    - $[\text{X}]$ Move with arrows
    - $[\text{X}]$ Move the elements by dragging 
    - $[\text{X}]$ Highlight multiple elements
    - $[\text{X}]$ Delete highlighted files with $\textit{`esc'}$
    - $[\text{X}]$ Create collections
        - $[\text{X}]$ Manage collpases
        - $[\text{X}]$ Manage child-parent structure
        - $[\text{X}]$ Parse instructions given to the children

Drop_menu:
--
- Functionality:
    - $[\text{X}]$ Show a maximum number of options
    - $[\text{X}]$ Scroll through the option with wheel or arrows
    - $[\text{X}]$ Support writing to find closest option

Quick_menu:
--
- Cosmetic:
    - $[\text{X}]$ Support image texture rendering
    - $[\text{X}]$ Support lines to subdivide the blocks

- Functionality:
    - $[\text{X}]$ Can contain Button_toggle and Button_push

Color_picker:
--
- Functionality:
    - $[\text{X}]$ Select color from RGB
    - $[\text{X}]$ Select color from HSL
    - $[\text{X}]$ Select color from HEX
    - $[\text{X}]$ Select color from color wheel
    - $[\text{X}]$ Select color from recent used colors
    - $[\text{X}]$ Select color from favourite colors
    - $[\text{X}]$ Select color from frequently used colors
    - $[\text{X}]$ Simple palette that turns into complex palette
    - $[\text{X}]$ Choose a batch of colors using OKLAB palette generator
    - $[\text{X}]$ Copy and paste a color by hovering

Color_ramp:
--
- Cosmetic:
    - $[\text{X}]$ Color the bar to represent the change
- Functionality:
    - $[\text{X}]$ Import color ramps (`.json`)
    - $[\text{X}]$ Save color ramps (`.json`)
    - $[\text{X}]$ Invert color ramp
    - $[\text{X}]$ Set values
    - $[\text{X}]$ Drag the flags to change the values (slider like)

Slider:
--
- Functionality:
    - $[\text{X}]$ Entry box for controlling precisely the slider value
    - $[\text{X}]$ Set a discrete amount of possible subdivisions


<!-- 
Collapsable_window:
--
Pop_up:
-- 
-->
