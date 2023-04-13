import cview.CLI as CLI                                     # change to view not cview
import model.puzzle as puzzle
from controller.cController import CLIAdapter
import model.output as output
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter


# Start of game declarations for needed objects and fields
outty = output.Output()
usrinput = ' '
notValidIn = True
puzzle = puzzle.Puzzle('', '')
adapter = CLIAdapter.CLI_A(puzzle, outty)
tabComp = WordCompleter(adapter.commandsList)

# inital game loop, loop until valid start is reached
while notValidIn:
    if outty.getField() != '':
        print(outty.getField())
    CLI.drawTextBox(['Welcome to Spelling Bee! \ '
                     'Presented by G(J)IFY',
                     'To start a new game, type "!new". To load a previous '
                     'save, type "!load"'], 40, '^')
    usrinput = prompt('> ', completer=WordCompleter(['!new', '!load',
                                                     '!exit']))
    puzzle = adapter.parse(usrinput)
    # check and see if bad puzzle object was returned somewhere
    if puzzle is None:
        notValidIn = True
    else:
        notValidIn = False


# after start of game loop, draw new game for first time
CLI.clear()
CLI.drawGameBox(puzzle, outty)
usrinput = prompt('> ', completer=tabComp)

# game loop
while True:
    CLI.clear()
    # parse user input
    retPuzzle = adapter.parse(usrinput)
    # check to see if return puzzle was None (error occuered)
    if retPuzzle is not None:
        puzzle = retPuzzle
    # draw game box
    CLI.drawGameBox(puzzle, outty)
    # reset outty
    outty.setField('')
    # check for end of game flag
    if puzzle.getFinishedFlag():
        adapter.finalGame()
    # wait for user's next input
    usrinput = prompt('> ', completer=tabComp)
