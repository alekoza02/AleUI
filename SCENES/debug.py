from UI_ELEMENTS.element_button_push import Button_push
from UI_ELEMENTS.element_container import Container
from UI_ELEMENTS.element_text_label import Label_text
from UI_ELEMENTS.element_collapse_window import Collapse_Window


DO_NOT_EXECUTE = False
if DO_NOT_EXECUTE:
    from AleUI import App

def build_dev_scene(app: 'App') -> 'App':
    app.UI["debug1"] = Container("0vw 10px", "0vh 10px", "50vw -15px", "100vh -20px", None, performant=1)
    
    app.UI["debug1"].add_element("hello_button1", Button_push("0cw", "0ch", "5sw", "5sh", None, performant=1))
    
    app.UI["debug1"].add_element("hello_button2", Label_text("50cw", "50ch", "20sw", "5sh", "center-center", performant=1))
    app.UI["debug1"].add_element("hello_button_anchor", Label_text("0px", "0px", "20sw", "5sh", "center-center", text="\\h{Ancorato}", performant=1))
    app.UI["debug1"].child_elements["hello_button_anchor"].set_parent("center-down", app.UI["debug1"].child_elements["hello_button2"], "center-up", "10sw", "-50px")

    app.UI["debug1"].add_element("hello_button3", Button_push("100cw -5sw", "100ch -5sh", "5sw", "5sh", None, performant=1))
    
    app.UI["debug2"] = Container("50vw 5px", "0vh 10px", "50vw -15px", "66.6vh -15px", None, performant=1)
    app.UI["debug3"] = Container("50vw 5px", "66.6vh 5px", "50vw -15px", "33.3vh -15px", None, performant=1)

    app.UI["debug2"].add_element("debugger", Collapse_Window("50cw", "0ch 5px", "100cw -10px", "50ch -7.5px", "center-up", title="Collapsable 1", performant=1))
    app.UI["debug2"].add_element("debugger2", Collapse_Window("0px", "0px", "100cw -10px", "50ch -7.5px", "center-up", title="Collapsable 2", performant=1))
    app.UI["debug2"].child_elements["debugger2"].set_parent("center-up", app.UI["debug2"].child_elements["debugger"], "center-down", "0px", "5px")

    app.UI["debug2"].child_elements["debugger"].add_element("prova1", Label_text("50cw", "0px", "50cw -5px", "50ch -5px", "left-up", "Primo testo", text_tag_support=False))
    app.UI["debug2"].child_elements["debugger"].add_element("prova2", Label_text("50cw", "50ch", "50cw -5px", "50ch -5px", "left-up", "Secondo testo", text_tag_support=False))
    
    app.UI["debug2"].child_elements["debugger2"].add_element("prova3", Label_text("50cw", "0px", "50cw -5px", "50ch -5px", "left-up", "Terzo testo", text_tag_support=False))
    app.UI["debug2"].child_elements["debugger2"].add_element("prova4", Label_text("50cw", "50ch", "50cw -5px", "50ch -5px", "left-up", "Quarto testo", text_tag_support=False))

    # Build the scene specified and updates it to the screen
    app.update_coords_UI_elements()

    return app