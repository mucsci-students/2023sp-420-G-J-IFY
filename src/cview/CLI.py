#!/usr/bin/env

################################################################################
# CLI.py
# AUTHOR: Isaak Weidman
# DATE OF CREATION: -
# 
# DESCRIPTION:
#   Multi-line descripiton pending
#
# FUNCTIONS:
#   drawTextBox(message : str, width : int, align : str) -> None
#     - draws a text box containing message, width wide, and alignment align.
#   drawProgressBox(size : int, val : float) -> str
#     - draws a progress bar of size width and displaying float %
#   drawPuzzle(letters : list[str]) -> str
#     - Draws a hex pattern of 7 letters
#   drawGameBox(game : object) -> None
#     - Formats and prints game data stored in object
#   clear() -> None
#     - Checks os and calls applicable console clear command
################################################################################

from os import system, name

################################################################################
# drawTextBox(message : str, width : int, align : str) -> None
#
# DESCRIPTION:
#   Draws a box of a specified size around a list of strings where each element
#   in the list is another tier in the box. Text is alligned according to
#   given alignment string.
# 
# PARAMETERS:
#   message : list[str]
#     - List of message to be printed within the text box. use " \ " to define
#       carriage return. Each element in the list will be drawn in the next
#       tier below the last.
#   width : int
#     - Overall width of the textbox in characters, including border.
#   align : str
#     - A single character that defines the alignment of text in the textbox.
#       '<' => left alignment
#       '>' => right alignment
#       '^' => center alignment
################################################################################
def drawTextBox(message : list[str], width : int, align : str) -> None:

    # Build ceiling, wall, and floor of text box based on given width.
    # Ceiling is the top of the box, floor is the bottom of the box, and wall
    #   is the separater line between each tier.
    ceiling = '╔{:═<{}}╗'.format('', width-2)
    wall = '╟{:─<{}}╢'.format('', width-2)
    floor = '╚{:═<{}}╝'.format('', width-2)

    words = [] # a list of strings where each string is a tier
    blocks = [] # a list of lists, where each list represents a tier,
                  # and each sub-list represents a line in that tier
    txtBox = '' # a string storing the final, properly formatted text box

    # Split each string in message into list of the words, split by spaces.
    for string in message:
        words.append(string.split())
    
    # Format words lists back into strings where each element in the list
    #   is a line in the block, aligned and spaced correctly.
    for list in words:
        lines = []
        line = ' '
        for word in list:
            if (len(line) + len(word)+1) >= width-2:
                lines.append(line)
                line = ' ' + word + ' '
            elif word == '\\':
                lines.append(line)
                line = ' '
            else:
                line += word + ' '
        lines.append(line)
        blocks.append(lines)
    
    # Fencepost algorithm for building the final box
    txtBox = ceiling + '\n'
    # Remove first block and format it properly
    for line in blocks.pop(0):
        txtBox += '║{:{}{}}║\n'.format(line, align, width-2)

    # Now format remaining blocks
    for block in blocks:
        # Begin each block with a separator wall
        txtBox += wall + '\n'
        # Format each like according to parameters
        for line in block:
            txtBox += '║{:{}{}}║\n'.format(line, align, width-2)

    # Finally, add floor of text box
    txtBox += floor + '\n'

    # Print final product.
    print(txtBox)


################################################################################
# drawProgressBar(size : int, val : float) -> str
#
# DESCRIPTION:
#   Draws a progress bar displaying a provided percentage, of a specific width
#
# PARAMETERS:
#   size : int
#     - the number of characters wide to draw the text box
#   val : float
#     - percent to be displayed on ptrogress bar
#
# RETURNS:
#   str
#     - a formatted string containing the resulting progress bar.
################################################################################
def drawProgressBar(size : int, val : float) -> str:
    fill = int(float(size-2) * val)
    remaining = ((size-2) - fill)
    # print a string with fill number of =, and remaining number of -
    bar = '<{0:=<{1}}{2:-<{3}}>'.format('', fill, '', remaining)
    return(bar)



################################################################################
# drawPuzzle(letters : list) -> str:
#
# DESCRIPTION:
#   formats a string representing a hex pattern of 7 characters.
#
# PARAMETERS:
#   letters : list
#     - list of 7 characters
#
# RETURNS:
#   str:
#     - formatted string containing the puzzle representation
################################################################################
def drawPuzzle(letters : list) -> str:
    # Pretty much just hard coded the output, letters are simple swapped in
    out =  (' ┌───┬───┐ \ '
            '│ {0[1]} │ {0[2]} │ \ '
            '┌─┴─╥─┴─╥─┴─┐ \ '
            '│ {0[3]} ║ {0[0]} ║ {0[4]} │ \ '
            '└─┬─╨─┬─╨─┬─┘ \ '
            '│ {0[5]} │ {0[6]} │ \ '
            '└───┴───┘ ').format(letters)
    return(out)


################################################################################
# drawGameBox(game : object) -> None:
# 
# DESCRIPTION:
#   Draws game information stored in game object to the screen for gameplay
#
# PARAMETERS:
#   game : object
#     - puzzle object storing current game state
################################################################################
def drawGameBox(game : object) -> None:

    # calculate game progression
    score = game.showScore()
    max = game.showMaxScore()
    prog = score/max

    tier1 = 'Welcome to Spelling Bee! \ Presented by G(J)IFY'
    tier2 = 'Level: \ {lvl} {pBar}'.format(lvl = game.showRank(), 
                                           pBar = drawProgressBar(20, prog))
    tier3 = 'Discovered Words: \ {wrds}'.format(wrds = game.showFoundWords())
    tier4 = drawPuzzle(game.showShuffleLetters().upper())
    tier5 = 'Enter your guess, or type \'!help\' for a list of commands.'
    drawTextBox([tier1, tier2, tier3, tier4, tier5], 40, '^')


################################################################################
# clear() -> None
#
# DESCRIPTION:
#   calls appliciable clear console command depending on operating system.
################################################################################
def clear() -> None:
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')