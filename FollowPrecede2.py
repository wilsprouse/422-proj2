
#letter comes from the decided letter in a cell
#call on grid object [row #][column#] of decided cell you're interested in
def assignPostShutOffs(letter):
    NonFollows = {
        'B': "QX",
        'C': "FJVX",
        'D': "X",
        'F': "QXZ",
        'G': "QX",
        'H': "X",
        'J': "BCFGQVXZ",
        'K': "QZ",
        'P': "QX",
        'Q': "CDGHJKLMNPQRVXYZ",
        'S': "X",
        'T': "X",
        'V': "BCFJMPQTWX",
        'W': "QX",
        'X': "DJXZ",
        'Z': "JX"
        #total: 61
        #Letters that are not keys in this are A, E, I, L, M, N, O, R, U,Y. So AEILMNORUY can take any letter
    }
    initialLetter = letter.upper() #getChosen().upper()
    shutOff = None
    #initialLetter = letter.upper()
    if initialLetter in NonFollows:
        shutOff = NonFollows.get(initialLetter)
    return shutOff
    #else:
    #if initialLetter not in NonFollows:
        #noBitChanges = "All letters possible to follow"
        #returnValue = None
"""shutOffHorizontalFollow and shutOffVerticalFollow are to be grid-class functions"""
def shutOffHorizontalFollow(row, column, letter):
    toBeShutOff = assignPostShutOffs(letter)
    if toBeShutOff is not None:
        for letter in toBeShutOff:
            [row][column+1].setitem(letter, False)

def shutOffVerticalFollow(row, column, letter):
    toBeShutOff = assignPostShutOffs(letter)
    if toBeShutOff is not None:
        for letter in toBeShutOff():
            [row+1][column].setitem(letter, False)

# returns string of not possible 2-letter combinations with ? + givenletter
def assignPreShutOffs(letter):  # pass in a Grid, row # and column # that reprsent the position that you're looking to fill left or up
    NonPrecedes = {
        'B': "JV",
        'C': "JQV",
        'D': "QX",
        'F': "CJV",
        'G': "JQ",
        'H': "Q",
        'J': "CQVXZ",
        'K': "Q",
        'L': "Q",
        'M': "QV",
        'N': "Q",
        'P': "QV",
        'Q': "BFGJKPQVW",
        'R': "Q",
        'T': "V",
        'V': "CJQ",
        'W': "V",
        'X': "BCDFGHJPQSTVWXZ",
        'Y': "Q",
        'Z': "FJKQX"
        #total: 61
        #letters not keys are AEIOSU
    }
    myLetter = letter.upper() #getChosen().upper()
    shutOff = None
    # initialLetter = letter.upper()
    if myLetter in NonPrecedes:
        shutOff = NonPrecedes.get(myLetter)
        # for letter in shutOff:
        # Grid[row][column+1].setitem(letter, False)
    return shutOff

"""shutOffHorizontalPrecde and shutOffVerticalPrecede are to be grid class functions"""

def shutOffHorizontalPrecede(row, column, letter):
    toBeShutOff = assignPreShutOffs(letter)
    if toBeShutOff is not None:
        for letter in assignPostShutOffs():
            [row][column-1].setitem(letter, False)

def shutOffVerticalPrecede(row, column, letter):
    toBeShutOff = assignPreShutOffs(letter)
    if toBeShutOff is not None:
        for letter in assignPostShutOffs():
            [row-1][column].setitem(letter, False)