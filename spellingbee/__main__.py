# flake8: noqa
from model.output import Output
import sys
argv = sys.argv[1:]

outty = Output.getInstance()

if len(argv) == 0:
    from controller.gController import __main__
else:
    if argv[0] == '--cli':
        from controller.cController import __main__
    else:
        print(argv[0] + ' is not a valid flag')
