from os import system, name

# params:
#   - message: string list, stores text to be printed in text box
#       format: ['Tier one: \ this is the text in the first tier of box',
#               'Tier two: \ the backslash sylbol is used to denote a new
#               line character.', 'Tier three: \ each element in this list of
#               strings is a separate tier of the box. If the list contains
#               only one element, then the box will have only one tier.']
#   - width: int, the width of the box, including the borders.
#   - align: string, Left, right, or center alignment of the text.
#       < : left alligned
#       > : right alligned
#       ^ : center alligned
#   - Example: drawTextBox(['testing \ testing', '123'], 15, '^')
#       Output: ╔═════════════╗
#               ║   testing   ║
#               ║   testing   ║
#               ╟─────────────╢
#               ║     123     ║
#               ╚═════════════╝
#       # A textbox 15 characters wide with two tiers.
def drawTextBox(message, width, align):

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


# params: 
#   - size: int, width of the progress bar
#   - val: float, percent value to be displayed
#   - return: string, string containing progress bar
def drawProgressBar(size, val):
    fill = int(float(size-2) * val)
    remaining = ((size-2) - fill)
    # print a string with fill number of =, and remaining number of -
    bar = '<{0:=<{1}}{2:-<{3}}>'.format('', fill, '', remaining)
    return(bar)


# params:
#   - letters: list, contains the 7 unique letters to be displayed
#   - key: int, index of the key letter
def drawPuzzle(letters):
    # Pretty much just hard coded the output, letters are simple swapped in
    out =  (' ┌───┬───┐ \ '
            '│ {0[1]} │ {0[2]} │ \ '
            '┌─┴─╥─┴─╥─┴─┐ \ '
            '│ {0[3]} ║ {0[0]} ║ {0[4]} │ \ '
            '└─┬─╨─┬─╨─┬─┘ \ '
            '│ {0[5]} │ {0[6]} │ \ '
            '└───┴───┘ ').format(letters)
    return(out)

# params:
#   - list: list of strings, printed out nicely
def drawList(list):
    outstr = ' '
    for l in list:
        outstr += l.upper() + ' '
    return outstr

def drawGameBox(game):

    # calculate game progression
    score = game.getScore()
    max = game.getMaxScore()
    prog = score/max

    tier1 = 'Welcome to Spelling Bee! \ Presented by G(J)IFY'
    tier2 = 'Level: \ {lvl} {pBar}'.format(lvl = game.getRank(), 
                                           pBar = drawProgressBar(20, prog))
    tier3 = 'Discovered Words: \ {wrds}'.format(wrds = game.getFoundWords())
    tier4 = drawPuzzle(game.getShuffleLetters().upper())
    tier5 = 'Enter your guess, or type \'!help\' for a list of commands.'
    drawTextBox([tier1, tier2, tier3, tier4, tier5], 40, '^')

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')