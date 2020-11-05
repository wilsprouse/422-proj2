"""
class Site:
    def __init__(self, totalRows, totalColumns):
        isOpen = True
        isClosed = False
        letter = 0x3FFFFFF # 26
        HorizThPositionInWord = 0
        VertThPositionInWord = 0
        row = 0
        column = 0

    def setPointers(self, totalRows, totalColumns):
    #relate site to up, down, left, and right sites
        #relate to immediately-above site
        if self.row> 0:
            self.up.row = self.row-1
            self.up.column =self.column
        else: self.up = None

        #relate to immediately-below site
        if self.row <totalRows-1:
            self.down.row = self.row+1
            self.down.column = self.column
        else: self.down = None

        #relate to immediately-left site
        if self.column > 0:
            self.left.column = self.column -1
            self.left.row = self.row
        else: self.left = None

        #relate to immediately-right site
        if self.column < totalColumns -1:
            self.right.column = self.column +1
            self.right.row = self.row
        else:self.right = None


class Grid:
    def __init__(self, totalRows, totalColumns):
        for i in range (0, totalRows):
            for j in range (0, totalColumns):
                Site().column = j
            Site().row = i
"""


class Cell:
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

    def __init__(self):
        self.__value = 0
        for i in range(len(Cell.alphabet)):
            self.__value = (self.__value << 1) & 1

    # MUTATORS

    def __set__(self, instance, value):
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
        Mutator method for an element in cell (used like cell[key] = value). Sets the possibility state of the given character "key" to "value."
        :param key: A one character string
        :param value: Whether the character is possible or not
        :return: None
        """
        pos = self.__get_index(key)
        if pos == None:
            raise TypeError('Key correctly formatted but does not exist in alphabet.')
        self.__value = self.__value & (int(value) << pos)

    # ACCESSORS

    def __get__(self, instance, owner):
        """
        Accessor method for Cell state (used like tmp = cell, etc.). Get's the integer representation of the Cell's state.
        :param instance: Not used
        :param owner: Not used
        :return: int
        """
        return self.__value

    def __getitem__(self, item):
        """
        Accessor method for an element in cell (used like cell[item]). Get's the possibility state of a given character "item."
        :param item: Single character string
        :return: bool
        """
        pos = self.__get_index(item)
        if pos == None:
            raise TypeError('Key correctly formatted but does not exist in alphabet.')
        return 1 & (self.__value >> pos) == 1

    # ITERATORS

    def __len__(self):
        """Gets number of possible characters."""
        return len(Cell.alphabet)

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
        for char in repr(self):
            yield char


    # CONVERTERS

    def __str__(self):
        """
        Converts cell to string. Returns character only if there is one possible character left, otherwise an emp
        :return: str
        """
        tmp = repr(self)
        if len(tmp) == 1:
            return tmp[0]
        return '?'


    def __repr__(self):
        """
        Get representation of Cell. Returns list of one character strings representing each possible character.
        :return: list
        """
        ret = []
        for pos in range(len(self)):
            if pos in self:
                ret += Cell.ALPHABET[pos]
        return ret

    # HELPERS

    def __get_index(self, char: str):
        """
        Helper method to get bit position of character char.
        :param char: str
        :return: int
        """
        if len(char) != 1:
            raise TypeError('Accesses must be a string of size one.')
        return Grid.ALPHABET.find(char)


class Grid:
    def __init__(self, totalRows, totalColumns):
        self.rows = totalRows
        self.cols = totalColumns
        self.__grid = []
        for x in range(totalRows):
            self.__grid.append([])
            for y in range(totalColumns):
                self.__grid[x].append(Cell())

    def __getitem__(self, key: tuple):
        """
        Accessor method for index in Grid class (used like grid[key]). Taking in the x, y pair "key", will return either a row/col vector if either x or y is set to None or a specific cell if both are given.
        :param key: Index value as an x, y pair. If one of the values is set to None return whole row (x) or column(y).
        :return: A list of type Cell or a single Cell object
        """
        x, y = key
        if x != None and y != None:
            return self.__grid[x][y]
        else:
            if y == None:
                return self.__grid[x]
            else:
                ret = []
                for i in range(self.cols):
                    ret.append(self.__grid[i][y])
                return ret

    def __setitem__(self, key, value):
        """
        Mutator method for index in Grid class (used like grid[key] = value).
        :param key: Index value as an x, y pair. If one of the values is set to None will set the whole row (y) or column(x)
        :param value: Value the index at key will be set to. Must be a Cell type if accessing point or list of Cell if accessing row/col.
        :return: None
        """
        x, y = key
        if x != None and y != None:
            self.__grid[x][y][value.lower()] = True
        else:
            if y == None:
                for i in range(self.rows):
                    self.__grid[x][i][value[i].lower()] = True
            else:
                for i in range(self.cols):
                    self.__grid[i][y][value[i].lower()] = True

    def __str__(self):
        """
        Return's a string representation of the grid (useful for testing).
        :return: str
        """
        ret = ''
        line = '+-+' * self.rows + '\n'
        for row in self.__grid:
            ret += line
            for cell in row:
                ret += f'|{cell}|'
            ret += '\n'
        ret += line
        return ret

    def toDict(self):
        """
        Converts the Grid class into a dictionary
        :return: dict
        """
        ret = dict()
        for x in range(len(self.__grid)):
            for y in range(len(self.__grid)):
                ret[x, y] = self.__grid[x][y]
        return ret


def __test_grid():
    grid = Grid(2, 2)
    test = [['a', 'n'],
            ['t', 'o']]
    for row in range(len(test)):
        for col in range(len(test[0])):
            grid[row, col] = test[row][col]
    print("Testing accessors:")
    print(f" - Test grid:\n{grid}")
    print(f" - Test row: {grid[0, None]}")
    print(f" - Test col: {grid[None, 0]}")
    print("Testing mutators:")
    grid[0, None] = ['p', 'p']
    print(f" - Test add row\n{grid}.")


if __name__ == '__main__':
    __test_grid()
