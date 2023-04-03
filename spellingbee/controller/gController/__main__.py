from gview import *

from controller.GUIAdapter import GUI_A
from controller import cmd
from model.output import Output

outty = Output()
gui = GUI_A(
    puzzle=cmd.NewGame(outty, 'warlock', 'w').execute(),
    outty=outty,
)

gui.start()