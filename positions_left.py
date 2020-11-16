class Grid:
    def __init__(self, totalRows, totalColumns):
        self.rows = totalRows
        self.cols = totalColumns
        self.grid = [ [ '0 ' for i in range(self.rows) ] for j in range(self.cols) ] 

    def print_grid(self):
        for i in range(self.cols):
            for j in range(self.rows):
                print(self.grid[i][j], end='')
            print()

    def insert(self, rowPos, colPos, word, horz):
        for letter in word:
            self.grid[colPos][rowPos%15] = letter + ' '
            if horz:
                rowPos += 1
            else:
                colPos += 1
        return colPos, rowPos

    def populate_crossword(self, startWord):
        horz = True
        stack = []
        stack.append((0,0))
        colPos, rowPos = grid.insert(0, 0, startWord, horz)
        cnt = 0 #len(startWord)
        while stack[0] != (self.rows-1,0):
            enter_word = 'Juicy'
            if not rowPos%15:
                
                colPos += 1
            colPos, rowPos = grid.insert(rowPos, colPos, enter_word, horz)
            stack = stack[1:]
            stack.append((colPos, rowPos%self.rows))
    
    def determine_positions(self):
        pos_left = []
        i = 0
        while i < self.cols:
            j = 0
            while j < self.rows:
                if self.grid[i][j] == '0 ':
                    #pos_left.append((i,j,'Horizontal'))
                    while self.grid[i][j] == '0 ':
                        j += 1
                        if j == self.cols:
                            break
                j += 1
            i += 1

        i = 0
        while i < self.cols:
            j = 0
            while j < self.rows:
                if self.grid[j][i] == '0 ':
                    pos_left.append((j,i,'Vertical'))
                    while self.grid[j][i] == '0 ':
                        j += 1
                        if j == self.rows:
                            break
                j += 1
            i += 1
        return pos_left
                        








grid = Grid(15, 15)
#grid.print_grid()
grid.insert(8, 8, 'dog', True)
grid.print_grid()
print(grid.determine_positions())







