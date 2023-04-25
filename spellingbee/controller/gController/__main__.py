from controller.GUIAdapter import GUI_A
from controller import cmd

gui = GUI_A(
    puzzle=cmd.NewGame('', '').execute(),
)

gui.start()
