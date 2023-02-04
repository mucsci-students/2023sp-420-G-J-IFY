# import CommandHandler.py

'''
def drawTxtBox (message, width):
    
    line = '+'
    emptyBdy = '| '
    message = message.split()

    for i in range(width-2):
        line = line + '-'

    for word in message:
        if (word.len() + emptyBdy.len()) < width - 2:
            emptyBdy = emptyBdy + word
        else:
            emptyBdy = ''
        

    line = line + '+'
    emptyBdy = emptyBdy + '|'

    return(line + '\n' + emptyBdy + '\n' + line)
'''

# Print a text box to output that is 39 characters in total width
def drawStaticBox (message):
    # Build horizontal line starting and ending with + with 37 - in between
    topBorder = '+{0:-<37}+'.format('')
    body = ''
    words = message.split()
    lines = []

    # While words list is not empty.
    # After this loop, lines should be filled with the contents of each line of
    # text in the text box such that there are no words split between lines and
    # each line fits within the bounds of the box
    line = ' '
    for word in words:
        if ((len(line) + len(word)+1) >= 37):
            lines.append(line)
            line = ' ' + word + ' '
        elif word == '\\':
            lines.append(line)
            line = ' '
        else:
            line += word + ' '
    
    # Center each line of text within the body of the text box.
    for line in lines:
        # Begin each line of body with '| ', then center the line of text
        # within the bounds of the box, followed by ' |' and a carriage return.
        # Do this for each line to be printed within the box.
        body += '|{0:^37s}|\n'.format(line)

    return topBorder + '\n' + body + topBorder

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
#       Output: +-------------+
#               |   testing   |
#               |   testing   |
#               +-------------+
#               |     123     |
#               +-------------+
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
