import cview.CLI as CLI
import model.puzzle as puzzle
from controller.cController import CLIAdapter
from model.output import Output
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter


# Start of game declarations for needed objects and fields
outty = Output.getInstance()


def main(puzzle):

    usrinput = ' '
    notValidIn = True
    adapter = CLIAdapter.CLI_A(puzzle)
    puzzle = None
    #tabComp = WordCompleter(adapter.commandsList)

    startLoopCommands = ['newGame', 'loadGame', 'quitToDesktop']

    mainLoopCommands = ['shuffleLetters', 'showHints', 'showHelp',   
                        'showFoundWords', 'showLeaderboard', 
                        'saveGame', 'saveBlankGame', 'endGame']

    # inital game loop, loop until valid start is reached
    while notValidIn:
        if outty.getField() != '':
            print(outty.getField())
        CLI.drawTextBox(['Welcome to Spelling Bee! \ '
                         'Presented by G(J)IFY'], 40, '^')
        CLI.drawTextBox(['Enter a command to get started: \ '
                         '> newGame \ '
                         '> loadGame \ '
                         '> quitToDesktop'], 40, '<')
        usrinput = prompt('> ', completer=WordCompleter(startLoopCommands))
        if usrinput in startLoopCommands:
            puzzle = adapter.parse(usrinput)
        else:
            print("INVALID COMMAND")
            puzzle = None

        # check and see if bad puzzle object was returned somewhere
        if puzzle is None:
            notValidIn = True
        else:
            notValidIn = False

    # after start of game loop, draw new game for first time
    CLI.clear()
    CLI.drawGameBox(puzzle)
    usrinput = prompt('> ', completer = WordCompleter(mainLoopCommands))

    # game loop
    while True:
        CLI.clear()
        # check that command is valid command for game
        if usrinput not in startLoopCommands:
            # parse user input
            retPuzzle = adapter.parse(usrinput)
            # check to see if return puzzle was None (error occuered)
            if retPuzzle is not None:
                puzzle = retPuzzle
        else:
            outty.setField('INVALID COMMAND')
        # draw game box
        CLI.drawGameBox(puzzle)
        # reset outty
        outty.setField('')
        # check for end of game flag
        if puzzle.getFinishedFlag():
            CLI.clear()
            adapter.endGame()
        # wait for user's next input
        usrinput = prompt('> ', completer = WordCompleter(mainLoopCommands))

if __name__ == '__main__':
    main(puzzle)
