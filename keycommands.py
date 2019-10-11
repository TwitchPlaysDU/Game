import keypresser

commands = ['1', '2', '3', '4', '5', 'shop', 'lock', 'roll', 'level', 'all', 'dmg', 'items', 'sell', 'bench']

def command(c):

    if c in commands:
        if c.isdigit(): keypresser.pressAndRelease(c)
        elif c == 'shop': keypresser.pressAndRelease('space')
        elif c == 'lock': keypresser.pressAndRelease('q')
        elif c == 'roll': keypresser.pressAndRelease('r')
        elif c == 'level': keypresser.pressAndRelease('t')
        elif c == 'all': keypresser.pressAndRelease('p')
        elif c == 'dmg': keypresser.pressAndRelease('o')
        elif c == 'items': keypresser.pressAndRelease('i')
        elif c == 'sell': keypresser.pressAndRelease('e')
        elif c == 'bench': keypresser.pressAndRelease('w')
        
        return True
    return False