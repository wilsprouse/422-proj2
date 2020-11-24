import time

import random
import copy
import math
import WordFinder
from ErrorChecker import shutOffLeftRight, shutOffAboveBelow


class Cell:
    WALL_CHAR = '#'
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz' + WALL_CHAR  # alphabet + wall character

    # INITIALIZER

    def __init__(self, value=None):
        self.__value = 0
        for i in range(len(Cell.ALPHABET)):
            self.__value = (self.__value << 1) + 1
        if value != None:
            self.set(value)

    # MUTATORS

    def set(self, value):
        """
        Mutator method for Cell state (used like cell = value). Sets cell possibilities to a specific state through the input value "value."
        :param instance: Not used (required for __set__ method)
        :param value: May be either an integer representation of the cell (how value is stored internally) or a string of possible characters.
        :return: None
        """
        if type(value) is int:  # Use functionality for integer representation
            self.__value = value
        if type(value) is str:  # Use functionality for string representation
            self.__value = 0
            for char in value:
                self[char] = True

    def __setitem__(self, key: str, value: bool):
        """
        Mutator method for an element in cell (used like cell[key] = value). Sets the character state of the given character "key" to "value."
        :param key: A one character string
        :param value: Whether the character is possible or not
        :return: None
        """
        pos = self.__get_index(key)
        if pos == None:
            raise TypeError('Key correctly formatted but does not exist in alphabet.')
        if value:
            self.__value |= 1 << pos
        else:
            self.__value &= ~(1 << pos)

    def __invert__(self):
        """Bitwise not, inverts the cell (copying the data)"""
        return Cell(~self.__value)

    # ACCESSORS

    def isChosen(self):
        if self.__value == 0:
            return False
        tmp = math.log2(self.__value)
        return int(tmp) == tmp

    def getChosen(self):
        if self.__value == 0:
            return None
        tmp = math.log2(self.__value)
        if int(tmp) != tmp:
            return None
        return Cell.ALPHABET[int(tmp)]

    def getValues(self):
        """
        Accessor method for Cell state (used like tmp = cell, etc.). Get's the integer representation of the Cell's state.
        :return: int
        """
        return self.__value

    def __getitem__(self, item):
        """
        Accessor method for an element in cell (used like cell[item]). Get's the possibility state of a given character "item."
        :param item: Single character string
        :return: bool
        """
        pos = self.__get_index(item)  # pos in alphabet
        if pos == None:
            raise TypeError('Key correctly formatted but does not exist in alphabet.')
        return 1 & (self.__value >> pos) == 1

    def __eq__(self, other):
        assert type(other) is Cell
        return self.__value == other.getValues()

    # ITERATORS

    def __len__(self):
        """Gets number of possible characters."""
        return len(Cell.ALPHABET)

    def __contains__(self, item):
        """
        Accessor method for an element in cell (used like item in cell). Get's the possibility state of a given character "item."
        :param item: Single character string
        :return: bool
        """
        return self[item]

    def __iter__(self):
        """
        Iterator method for Cell class (used in for loops). iterates through all possible letters
        :return: char (returned through yield)
        """
        for char in self.toList():
            yield char

    # CONVERTERS

    def __str__(self):
        """
        Converts cell to string. Returns character only if there is one possible character left, otherwise an emp
        :return: str
        """
        tmp = self.getChosen()
        if tmp == None:
            return '?'
        return tmp

    def __format__(self, format_spec):
        return str(self)

    def __repr__(self):
        return str(self)

    def toList(self):
        """
        Get representation of Cell. Returns list of one character strings representing each possible character.
        :return: list
        """
        ret = []
        for pos in range(len(self)):
            tmp = Cell.ALPHABET[pos]
            if tmp in self:
                ret.append(tmp)
        return ret

    # COPIERS

    def __copy__(self):
        """
        Copy value into a new cell
        """
        return Cell(self.__value)

    def __deepcopy__(self, memodict={}):
        """
        Copy both the class and the values in the class (will not share any data)
        """
        return Cell(copy.deepcopy(self.__value, memodict))

    # HELPERS

    def __get_index(self, char: str):
        """
        Helper method to get bit position of character char.
        :param char: str
        :return: int
        """
        if type(char) is not str or len(char) != 1:
            raise TypeError('Accesses must be a string of size one.')
        pos = Cell.ALPHABET.find(char.lower())
        if pos < 0:
            raise TypeError(f'Access must be in alphabet ({Cell.ALPHABET[:-1]})')
        return pos


CELL_WALL = Cell(Cell.WALL_CHAR)


class Grid:
    AddVertically = lambda self, point, val: (point[0] + val, point[1])
    AddHorizontally = lambda self, point, val: (point[0], point[1] + val)

    def __init__(self, totalRows, totalColumns):
        self.rows = totalRows
        self.cols = totalColumns
        self.__grid = []
        for row in range(totalRows):
            self.__grid.append([])
            for col in range(totalColumns):
                self.__grid[row].append(Cell())

    def __getitem__(self, key: tuple):
        """
        Accessor method for index in Grid class (used like grid[key]). Taking in the row, y pair "key", will return either a row/col vector if either row or y is set to None or a specific cell if both are given.
        :param key: Index value as an row, y pair. If one of the values is set to None return whole row (x) or column(y).
        :return: A list of type Cell or a single Cell object
        """
        row, col = key
        return self.__grid[row][col]

    def __setitem__(self, key, value):
        """
        Mutator method for index in Grid class (used like grid[key] = value).
        :param key: Index value as an row, y pair. If one of the values is set to None will set the whole row (y) or column(x)
        :param value: Value the index at key will be set to. Must be a Cell type if accessing point or list of Cell if accessing row/col.
        :return: None
        """
        row, col = key
        self.__grid[row][col] = value

    # TODO: add special grid accessors and viewers making sure it copies the grid each time

    def __str__(self):
        """
        Return's a string representation of the grid (useful for testing).
        :return: str
        """
        ret = ''
        line = '+-' * self.cols + '+\n'
        for row in range(self.rows):
            ret += line
            for col in range(self.cols):
                ret += f'|{self[row, col]}'
            ret += '|\n'
        ret += line
        return ret

    def __eq__(self, other):
        assert type(other) is Grid
        if self.rows != other.rows or self.cols != other.cols:
            return False
        for row in range(self.rows):
            for col in range(self.cols):
                if self[row, col] != other[row, col]:
                    return False
        return True

    def __contains__(self, item):
        assert type(item) is tuple
        row, col = item
        # print(f'0 <= {row} < self.rows and 0 <= {col} < self.cols')
        # print(0 <= row < self.rows and 0 <= col < self.cols)
        return 0 <= row < self.rows and 0 <= col < self.cols

    def __copy__(self):
        newGrid = Grid(self.rows, self.cols)
        for i in range(len(self.__grid)):
            newGrid.__grid[i] = copy.copy(self.__grid[i])
        return newGrid

    def __deepcopy__(self, memodict={}):
        newGrid = Grid(self.rows, self.cols)
        newGrid.__grid = copy.deepcopy(self.__grid, memodict)
        return newGrid

    def toDict(self):
        """
        Converts the Grid class into a dictionary
        :return: dict
        """
        ret = dict()
        for row in range(len(self.__grid)):
            for col in range(len(self.__grid)):
                ret[row, col] = self.__grid[row][col]
        return ret

    def isComplete(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if not self[row, col].isChosen():  # If cell has not been chosen
                    return False
        return True

    def isValid(self, dictionary):
        for _, location in self.findLines(lambda list: all([cell.isChosen() for cell in list])):
            if not dictionary.isWord(location):
                return False
        return True

    def getNextGridStates(self, dictionary, maxWords=100):
        """
        Creates successor grid states based on current state by...
            - Finding where to input subsequent words (Row / Col Chooser)
            - Inserting all possible words into that point as separate substates (WordFinder)
            - Return these states
        """
        '''
        startingPoint = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
        while self[startingPoint] == CELL_WALL:
            startingPoint = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
        verticalLine = self.__getNextLine(startingPoint, 'Vertical')
        # print(verticalLine)
        horizontalLine = self.__getNextLine(startingPoint, 'Horizontal')
        # print(horizontalLine)

        start, direction, line = horizontalLine
        if len(verticalLine[2]) > len(line):  # Add longer line first
            start, direction, line = verticalLine
        #print(start, direction, line)
        stp1 = []
        if not all([cell.isChosen() for cell in line]):
            #print('hi')
            for word in dictionary.getWords(line, len(line)//2):
                # print('hi')
                new_grid = copy.deepcopy(self)
                if direction == 'Horizontal':
                    iterate = self.AddHorizontally  # Horizontal iterator
                elif direction == 'Vertical':
                    iterate = self.AddVertically  # Vertical iterator
                else:
                    raise Exception(f'Failed both directions ({direction})')
                pos = start
                for cell in word:
                    #print(pos)
                    if pos not in self:
                        print(self)
                        print(start, direction, line)
                        print(pos)
                    new_grid[pos] = cell
                    if direction == 'Vertical':
                        shutOffLeftRight(new_grid, pos)
                    elif direction == 'Horizontal':
                        shutOffAboveBelow(new_grid, pos)
                    pos = iterate(pos, 1)
                stp1.append(new_grid)
        else:
            #print('failed')
            stp1.append(self)

        # for grid in stp1:
        #    print(str(grid))

        start, direction, line = horizontalLine
        if len(verticalLine[2]) < len(line):  # Add longer line first
            start, direction, line = verticalLine

        ret = []
        if not all([cell.isChosen() for cell in line]):
            #print('hi again')
            for grid in stp1:
                for word in dictionary.getWords(line, len(line) // 2):
                    new_grid = copy.deepcopy(grid)
                    if direction == 'Horizontal':
                        iterate = self.AddHorizontally  # Horizontal iterator
                    elif direction == 'Vertical':
                        iterate = self.AddVertically  # Vertical iterator
                    else:
                        raise Exception('Failed both directions')
                    pos = start
                    for cell in word:
                        new_grid[pos] = cell
                        if direction == 'Vertical':
                            shutOffLeftRight(new_grid, pos)
                        elif direction == 'Horizontal':
                            shutOffAboveBelow(new_grid, pos)
                        pos = iterate(pos, 1)
                    ret.append(new_grid)
        else:
            #print('failed again')
            ret = stp1
        #for grid in ret:
        #    print(str(grid))
        print(len(ret))
        return ret
        '''
        ret = []
        #print(type(linesleft))
        lines = self.findLines(lambda list: not all([cell.isChosen() for cell in list]))
        if len(lines) < 1:
            return ret
        for metadata, location in random.sample(lines, 1):
            startRow, startCol, direction = metadata
            words = dictionary.getWords(location, len(location)//2)
            if len(words) > maxWords:
                words = random.sample(words, maxWords)
            for word in words:
                new_grid = copy.deepcopy(self)
                if direction == 'Horizontal':
                    iterate = lambda point : (point[0], point[1] + 1) # Horizontal iterator
                elif direction == 'Vertical':
                    iterate = lambda point : (point[0] + 1, point[1]) # Vertical iterator
                else:
                    raise Exception('Failed both directions')

                #print(f'Adding {word} {direction}ly to grid:\n{str(self)}')
                point = startRow, startCol
                for cell in word:
                    #print(f'Adding {cell} to point {point}', end='\t')
                    new_grid[point] = cell
                    if direction == 'Vertical':
                        shutOffLeftRight(new_grid, point)
                    elif direction == 'Horizontal':
                        shutOffAboveBelow(new_grid, point)
                    else:
                        raise Exception('Failed both directions')
                    point = iterate(point)
                #print()
                #print(f'Added {word} to grid:\n{str(self)}')
                #print(str(new_grid))
                #print(new_grid[])
                ret.append(new_grid)
        return ret

    '''
    def __getNextLine(self, middle, direction):
        func = self.AddHorizontally
        if direction == 'Vertical':
            func = self.AddVertically

        line = [self[middle]]
        start = middle
        print(start)
        negativeEnd = False
        positiveEnd = False
        for delta in range(1, max(self.rows, self.cols)):
            if negativeEnd and positiveEnd:
                # print('end early')
                break
            if not negativeEnd:
                posNeg = func(middle, -delta)
                if posNeg not in self or self[posNeg] == CELL_WALL:
                    start = func(posNeg, 1)
                    print(f'updating start to {start}')
                    negativeEnd = True
                    continue
                #print(f'adding negatively {posNeg}')
                line.insert(0, self[posNeg])
            if not positiveEnd:
                posPos = func(middle, delta)
                if posPos not in self or self[posPos] == CELL_WALL:
                    positiveEnd = True
                    continue
                #print(f'adding positively {posPos}')
                line.append(self[posPos])
        return start, direction, line
    '''

    def findLines(self, requirements=lambda list: True):
        # startTime = time.time()
        pos_left = []
        col = 0
        while col < self.cols:
            row = 0
            while row < self.rows:
                if self[row, col] != CELL_WALL:
                    save_row = row
                    pos = []
                    # alreadyComplete = True
                    while self[row, col] != CELL_WALL:
                        # tmp = self[row, col]
                        # if not tmp.isChosen():
                        #    alreadyComplete = False
                        pos.append(self[row, col])
                        row += 1
                        if row == self.rows:
                            break
                    # if len(pos) != 1 and not alreadyComplete:
                    # print(f'{[cell.isChosen() for cell in pos]} -> {requirements(pos)}')
                    if len(pos) != 1 and requirements(pos):
                        pos_left.append(((save_row, col, 'Vertical'), pos))
                row += 1
            col += 1

        row = 0
        while row < self.rows:
            col = 0
            while col < self.cols:
                if self[row, col] != CELL_WALL:
                    pos = []
                    save_col = col
                    # alreadyComplete = True
                    while self[row, col] != CELL_WALL:
                        tmp = self[row, col]
                        # if not tmp.isChosen():
                        #    alreadyComplete = False
                        pos.append(tmp)
                        col += 1
                        if col == self.cols:
                            break
                    # if len(pos) != 1 and not alreadyComplete:
                    if len(pos) != 1 and requirements(pos):
                        pos_left.append(((row, save_col, 'Horizontal'), pos))
                col += 1
            row += 1
        # print(f'findLines ran in {time.time() - startTime} sec.')
        return pos_left


def __test_grid():
    grid = Grid(2, 2)
    test = [['a', 'n'],
            ['t', 'o']]
    for row in range(len(test)):
        for col in range(len(test[0])):
            grid[row, col].set(test[row][col])
    print("Testing accessors:")
    print(f" - Test grid:\n{grid}")
    print(f" - Test pos: {grid[0, 0]}")
    print(f" - Test row: {grid[0, None]}")
    print(f" - Test col: {grid[None, 0]}")
    print("Testing mutators:")
    grid[0, None] = ['p', 'p']
    print(f" - Test add row\n{grid}")
    grid[None, 1] = ['l', 'p']
    print(f" - Test add col\n{grid}")


def __cell_test():
    cell = Cell()
    print("====================\ntest create\n====================")
    print(f"{bin(cell.getValues())}\n{cell.toList()}")
    print("====================\ntest edit bit\n====================")
    cell["b"] = False
    cell["P"] = False
    print(f"{bin(cell.getValues())}\n{cell.toList()}")
    store = cell.getValues()
    print("====================\ntest get bit\n====================")
    print(cell["p"])
    print(cell["d"])
    print(f"{bin(cell.getValues())}\n{cell.toList()}")
    print("====================\ntest set\n====================")
    cell.set('f')
    print(f"{bin(cell.getValues())}\n{cell.toList()}")
    print("====================\ntest string\n====================")
    print(f"{cell}")
    print("====================\ntest iterate\n====================")
    cell.set(store)
    for char in cell:
        print(char, end=' ')
    print()


def __test_getNext():
    dictionary = WordFinder.WordFinder()
    dictionary.importFromFile('dictionary.new.txt')

    grid = Grid(2, 2)
    test_grid = [
        ['a', 't'],
        [None, '#']
    ]
    for y in range(len(test_grid)):
        for x in range(len(test_grid[0])):
            cell = test_grid[x][y]
            if cell != None:
                grid[x, y] = Cell(cell)

    print(str(grid))
    print('---------------------')
    # for i in range(5):
    #    grid[random.randint(0,grid.rows - 1), random.randint(0,grid.cols - 1)] = Cell.WALL_CHAR
    # print(str(grid))
    test = grid.getNextGridStates(dictionary)

    for grid in test:
        print(str(grid))


def __test_getNextAdditionPoints():
    grid = Grid(4, 4)
    test_grid = [
        ['h', 'e', 'a', 'd'],
        ['e', 'v', 'e', 'r'],
        [None, '#', '#', '#'],
        [None, None, None, None]
    ]
    for y in range(len(test_grid)):
        for x in range(len(test_grid[0])):
            cell = test_grid[x][y]
            if cell != None:
                grid[x, y] = Cell(cell)
    print('testing for getNext')
    test = grid.getNextAdditionPoints(lambda list: not all([cell.isChosen() for cell in list]))
    for cell in test:
        print(cell)
    print('testing for isComplete')
    test = grid.getNextAdditionPoints()
    for cell in test:
        print(cell)


"""
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
TUTORIAL
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
"""


def cell_tutorial():
    undecided_cell = Cell("abdlmp")
    decided_cell = Cell("z")
    """
    --------------------
    Accessing a cell:
    --------------------
    """
    "Checking if a letter is possible"
    # To check if a cell is possible there are 2 methods you can use:
    # 1. index (i.e. cell[])
    print(undecided_cell['a'])  # prints true
    print(undecided_cell['x'])  # prints false
    print(decided_cell['z'])  # prints true
    # 2. 'in' statement
    print('a' in undecided_cell)  # prints true
    print('x' in undecided_cell)  # prints false
    print('z' in decided_cell)  # prints true
    "Iterating through possible letters"
    # If you'd like to check all possible letters place the cell in a for loop
    for char in undecided_cell:
        print(char, end='\t')  # prints 'a   b   d   l   m   p'
    print()
    "Checking if a letter is the only possible letter"
    # The cell class also has a few methods to see if a letter has been decided (i.e. there's only 1 possibility)
    # 1. isChosen() - tests whether the cell has been decided
    print(undecided_cell.isChosen())  # prints false
    print(decided_cell.isChosen())  # prints true
    # 2. getChosen() - returns decided character
    print(undecided_cell.getChosen())  # prints None
    print(decided_cell.getChosen())  # prints 'z'
    """
    --------------------
    Editing a cell:
    --------------------
    """
    "Setting multiple letters"
    # U can set multiple values using the set() command which takes either a string of possible characters or a integer representation as an input
    undecided_cell.set("mpwqr")  # Sets characters 'm', 'p', 'q', 'r', 'w' to true and the rest false
    # ABCDEFGHIJKLMNOPQRSTUVWXYZ
    undecided_cell.set(0b00001001000100100000000000)  # Sets characters 'e', 'h', 'l', 'o' to true and the rest false
    "Setting 1 letter"
    # To set a specific letter index the letter like in a dictionary and set it to a boolean
    undecided_cell['v'] = True  # Sets v to true
    undecided_cell['l'] = False  # Sets l to false
    """
    --------------------
    Printing a cell:
    --------------------
    """
    "Print possible characters"
    print(undecided_cell.toList())
    "Print decided characters"
    print(str(decided_cell))


if __name__ == '__main__':
    # __test_grid()
    # __cell_test()
    cell_tutorial()
    # __test_getNext()
    # __test_getNextAdditionPoints()
    # __testGridCopy()
