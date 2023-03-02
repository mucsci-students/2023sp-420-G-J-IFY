import sys
argv = sys.argv[1:]
    
if len(argv) == 0:
    from controller.gController import __main__
else:
    if argv[0] == '-c':
        from controller.cController import __main__
    else:
        print(argv[0] + ' is not a valid flag')

