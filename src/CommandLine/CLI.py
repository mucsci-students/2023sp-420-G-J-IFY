
def drawDblTxtBox (message, width):
    line = '+'
    emptyBdy = '|'
    for i in range(width-2):
        line = line + '-'
        emptyBdy = emptyBdy + ' '
    line = line + '+'
    emptyBdy = emptyBdy + '|'
    return(line + '\n' + emptyBdy + '\n' + line)

print(drawDblTxtBox('test', 12))