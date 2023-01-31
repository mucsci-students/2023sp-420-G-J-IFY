

import argparse

# Create and ArgumentParser object and provide a description of the program
parser = argparse.ArgumentParser(description="An addition program")

# Add arguments:
# Fill up parser object with info by adding arguments

# arg1: 'add' -> will use this name to access add args by typing 'args.add'
# arg2: nargs='*' -> the number of command-line arguments that should be
#   consumed. Specifying it to '*' means it can be any number of arguments,
#   i.e. from 0 to anything.
# arg3: metavar='num' -> A name for the argument in usage messages.
# arg4: type=int -> The type to which the command line argument should be
#   converted. It is str by default.
# arg5: help -> A brief description of what the argument does.
parser.add_argument("add", nargs='*', metavar = "num", type = int,
    help = "All the numbers separated by spaces will be added.")

# Now that  all arguments have been specified, parse the arguments from the
#   standard command line input stream.
args = parser.parse_args()

# Check if add argument has any input data.
# If it has, then print sum of the given numbers
if len(args.add) != 0:
    print(sum(args.add))

