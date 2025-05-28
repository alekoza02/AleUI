from UI_ELEMENTS.element_button_push import Button_push
from UI_ELEMENTS.element_container import Container
from UI_ELEMENTS.element_text_label import Label_text
from UI_ELEMENTS.element_collapse_window import Collapse_Window
from UI_ELEMENTS.element_entry import Entry


DO_NOT_EXECUTE = False
if DO_NOT_EXECUTE:
    from AleUI import App

def build_dev_scene(app: 'App') -> 'App':
    app.UI["debug1"] = Container("0vw 10px", "0vh 10px", "50vw -15px", "97.5vh -20px", None)
    app.UI["debug1"].add_element("debugger", Entry("50cw", "50ch", "70cw", "100px", "center-center"))
    

    app.UI["debug2"] = Container("50vw 5px", "0vh 10px", "50vw -15px", "66.6vh -15px", None, scrollable=True)
    app.UI["debug3"] = Container("50vw 5px", "66.6vh 5px", "50vw -15px", "30.8vh -15px", None)
    app.UI["debug3"].add_element("debugger", Entry("50cw", "50ch", "70cw", "100px", "center-center"))
    
    app.UI["debug2"].add_element("debugger", Collapse_Window("2cw", "0ch 5px", "95cw -10px", "20ch", "left-up", title="Collapsable 1"))
    app.UI["debug2"].add_element("debugger2", Collapse_Window("0px", "0px", "95cw -10px", "20ch", "center-up", title="Collapsable 2"))
    app.UI["debug2"].child_elements["debugger2"].set_parent(app.UI["debug2"].child_elements["debugger"], "center-down", "0px", "5px")
    
    app.UI["debug2"].add_element("prova", Button_push("0px", "0px", "10cw", "10cw", "left-up", callback=lambda: print("Hello world!")))
    app.UI["debug2"].child_elements["prova"].set_parent(app.UI["debug2"].child_elements["debugger2"], "left-down", "0px", "2.5cw")

    app.UI["debug2"].add_element("debugger3", Collapse_Window("0px", "0px", "95cw -10px", "20ch", "left-up", title="Collapsable 3"))
    app.UI["debug2"].child_elements["debugger3"].set_parent(app.UI["debug2"].child_elements["prova"], "left-down", "0px", "2.5cw")
    app.UI["debug2"].add_element("debugger4", Collapse_Window("0px", "0px", "95cw -10px", "20ch", "center-up", title="Collapsable 4"))
    app.UI["debug2"].child_elements["debugger4"].set_parent(app.UI["debug2"].child_elements["debugger3"], "center-down", "0px", "5px")
    
    app.UI["debug2"].add_element("debugger5", Collapse_Window("0px", "0px", "95cw -10px", "20ch", "left-up", title="Collapsable 4"))
    app.UI["debug2"].child_elements["debugger5"].set_parent(app.UI["debug2"].child_elements["debugger4"], "left-down", "0px", "2.5cw")
    app.UI["debug2"].add_element("debugger6", Collapse_Window("0px", "0px", "95cw -10px", "20ch", "center-up", title="Collapsable 5"))
    app.UI["debug2"].child_elements["debugger6"].set_parent(app.UI["debug2"].child_elements["debugger5"], "center-down", "0px", "5px")

    app.UI["debug2"].child_elements["debugger"].add_element("prova1", Label_text("50cw", "0px", "50cw -5px", "50ch -5px", "left-up", "Primo testo", text_tag_support=False))
    app.UI["debug2"].child_elements["debugger"].add_element("prova2", Label_text("50cw", "50ch", "50cw -5px", "50ch -5px", "left-up", "Secondo testo", text_tag_support=False))
    
    app.UI["STATS"] = Container("0vw 10px", "97.5vh", "100vw -20px", "2vh", None)

    app.UI["STATS"].add_element("TIME", Label_text("100cw -2px", "50ch", "0cw", "100ch -4px", "right-center", "TIME", text_tag_support=True, fixed_number_of_chars=21))
    app.UI["STATS"].add_element("MEMORY", Label_text("0cw", "50ch", "0cw", "100ch -4px", "right-center", "MEMORY", text_tag_support=True, fixed_number_of_chars=21))
    app.UI["STATS"].add_element("BATTERY", Label_text("0cw", "50ch", "0cw", "100ch -4px", "right-center", "BATTERY", text_tag_support=True, fixed_number_of_chars=7))
    app.UI["STATS"].add_element("FPS", Label_text("0cw", "50ch", "0cw", "100ch -4px", "right-center", "FPS", text_tag_support=True, fixed_number_of_chars=12))
    app.UI["STATS"].add_element("CPU", Label_text("0cw", "50ch", "0cw", "100ch -4px", "right-center", "CPU", text_tag_support=True, fixed_number_of_chars=12))
    
    app.UI["STATS"].child_elements["MEMORY"].set_parent(app.UI["STATS"].child_elements["TIME"], "left-center", "-10px", "0px")
    app.UI["STATS"].child_elements["BATTERY"].set_parent(app.UI["STATS"].child_elements["MEMORY"], "left-center", "-10px", "0px")
    app.UI["STATS"].child_elements["FPS"].set_parent(app.UI["STATS"].child_elements["BATTERY"], "left-center", "-10px", "0px")
    app.UI["STATS"].child_elements["CPU"].set_parent(app.UI["STATS"].child_elements["FPS"], "left-center", "-10px", "0px")
    
    # Build the scene specified and updates it to the screen
    app.update_coords_UI_elements()

    return app