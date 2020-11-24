



#letter comes from the decided letter in a cell
#call on grid object [row #][column#] of decided cell you're interested in


class ValidCombo:
    __NonPrecedes = {
        'b': "jv",
        'c': "jqv",
        'd': "qx",
        'f': "cjv",
        'g': "jq",
        'h': "q",
        'j': "cqvxz",
        'k': "q",
        'l': "q",
        'm': "qv",
        'n': "q",
        'p': "qv",
        'q': "bfgjkpqvw",
        'r': "q",
        't': "v",
        'v': "cjq",
        'w': "v",
        'x': "bcdfghjpqstvwxz",
        'y': "q",
        'z': "fjkqx"
        # total: 61
        # letters not keys are AEIOSU
    }

    __NonFollows = {
        'b': "qx",
        'c': "fjvx",
        'd': "x",
        'f': "qxz",
        'g': "qx",
        'h': "x",
        'j': "bcfgqvxz",
        'k': "qz",
        'p': "qx",
        'q': "cdghjklmnpqrvxyz",
        's': "x",
        't': "x",
        'v': "bcfjmpqtwx",
        'w': "qx",
        'x': "djxz",
        'z': "jx"
        # total: 61
        # Letters that are not keys in this are A, E, I, L, M, N, O, R, U,Y. So AEILMNORUY can take any letter
    }

    @staticmethod
    def getPrecedes(letter):  # pass in a Grid, row # and column # that reprsent the position that you're looking to fill left or up
        shutOff = None
        if letter in ValidCombo.__NonPrecedes:
            shutOff = ValidCombo.__NonPrecedes[letter]
        return shutOff

    @staticmethod
    def getFollows(letter):
        shutOff = None
        # initialLetter = letter.upper()
        if letter in ValidCombo.__NonFollows:
            shutOff = ValidCombo.__NonFollows[letter]
        return shutOff


def shutOffLeftRight(grid, point):
    if not grid[point].isChosen(): return

    row, col = point
    letter = grid[row, col].getChosen()
    # PRECEDES
    toBeShutOff = ValidCombo.getPrecedes(letter)
    #print(toBeShutOff)
    if toBeShutOff is not None and col-1 >= 0:
        for newLetter in toBeShutOff:
            grid[row, col-1][newLetter] = False
            #print(f'removed {newLetter} grid now includes{grid[row, col-1].toList()}')
    # FOLLOWS
    toBeShutOff = ValidCombo.getFollows(letter)
    #print(toBeShutOff)
    if toBeShutOff is not None and col+1 < grid.cols:
        for newLetter in toBeShutOff:
            grid[row, col+1][newLetter] = False
            #print(f'removed {newLetter} grid now includes{grid[row, col+1].toList()}')

def shutOffAboveBelow(grid, point):
    if not grid[point].isChosen(): return

    row, col = point
    letter = grid[row, col].getChosen()
    # PRECEDES
    toBeShutOff = ValidCombo.getPrecedes(letter)
    #print(toBeShutOff)
    if toBeShutOff is not None and row-1 >= 0:
        for newLetter in toBeShutOff:
            grid[row-1, col][newLetter] = False
            #print(f'removed {newLetter} grid now includes{grid.toList()}')
    # FOLLOWS
    toBeShutOff = ValidCombo.getFollows(letter)
    #print(toBeShutOff)
    if toBeShutOff is not None and row+1 < grid.rows:
        for newLetter in toBeShutOff:
            grid[row+1, col][newLetter] = False

'''
-----------------------------
            TESTS
-----------------------------
'''

def __testPrePostShutOff():
    import Grid
    grid = Grid.Grid(2, 2)
    test_grid = [
        ['Tq', 'h',],# 'Tx'],
        ['Tcqvxz', 'j']# 'Tbcfgqvxz']
    ]
    for row in range(len(test_grid)):
        for col in range(len(test_grid[0])):
            if test_grid[row][col] != None:
                grid[row, col] = Grid.Cell(test_grid[row][col])

    print(str(grid))
    shutOffLeftRight(grid, 0, 1)
    shutOffLeftRight(grid, 1, 1)
    print(str(grid))



if __name__ == '__main__':
    __testPrePostShutOff()