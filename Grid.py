
class Site:
    def init(self, totalRows, totalColumns):
        isAvailable = True
        isBlack = False
        isOccupied = False
        letter = None
        HorizThPositionInWord = 0
        VertThPositionInWord = 0
        row = 0
        column = 0
        overallPosition = 0

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
""""""
class Grid:
    def init(self, totalRows, totalColumns):
        for i in range(0, totalRows):
            for j in range(0, totalColumns):
                Site().column = j
                Site.overallPosition = (i * totalColumns) + j
            Site().row = i

