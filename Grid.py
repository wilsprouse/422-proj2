class Cell:
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz\0'   # alphabet + wall character

    def __init__(self):
        self.__value = 0
        for i in range(len(Cell.ALPHABET)):
            self.__value = (self.__value << 1) + 1

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

    # ACCESSORS

    def isChosen(self):
        tmp = self.toList()
        if len(tmp) != 1:
            return False
        return True

    def getChosen(self):
        tmp = self.toList()
        if len(tmp) != 1:
            return None
        return tmp[0]

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
        pos = self.__get_index(item) # pos in alphabet
        if pos == None:
            raise TypeError('Key correctly formatted but does not exist in alphabet.')
        return 1 & (self.__value >> pos) == 1

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
        tmp = self.toList()
        if len(tmp) == 1:
            return tmp[0]
        return '?'

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

    # HELPERS

    def __get_index(self, char: str):
        """
        Helper method to get bit position of character char.
        :param char: str
        :return: int
        """
        if type(char) is not str or len(char) != 1:
            raise TypeError('Accesses must be a string of size one.')
        return Cell.ALPHABET.find(char.lower())


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
            self.__grid[x][y].set(value.lower())
        else:
            if y == None:
                for i in range(self.rows):
                    self.__grid[x][i].set(value[i].lower())
            else:
                for i in range(self.cols):
                    self.__grid[i][y].set(value[i].lower())

    # TODO: add special grid accessors and viewers making sure it copies the grid each time

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
            grid[row, col].set(test[row][col])
    print("Testing accessors:")
    print(f" - Test grid:\n{grid}")
    print(f" - Test pos: {grid[0,0]}")
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





if __name__ == '__main__':
    __test_grid()
    #__cell_test()
