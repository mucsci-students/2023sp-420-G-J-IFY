# flake8: noqa
from model.output import Output
import sys
argv = sys.argv[1:]
from model import puzzle

outty = Output.getInstance()

if len(argv) == 0:
    from controller.gController import __main__
else:
    if argv[0] == '--cli':
        from controller.cController.__main__ import main
        puzzle = puzzle.Puzzle('', '')

        main(puzzle)
    else:
        print(argv[0] + ' is not a valid flag')
