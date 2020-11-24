def getScore(letter):
    score = 0
    complete = 0
    currentLetter = letter.getChosen()
    #print(currentLetter)

    if currentLetter == None:
        return 0,0
    elif currentLetter in 'aeilnrst':
        score = 1#10
        complete = 1
    elif currentLetter in 'dgopu': #'DGOPU':
        score = 2#9
        complete = 1
    elif currentLetter in 'bcfhm': #'BCFHM':
        score = 4#7
        complete = 1
    elif currentLetter in 'kvwy': #'KVWY':
        score = 7#4
        complete = 1
    elif currentLetter in 'jx': #'JX':
        score = 9 #2
        complete = 1
    elif currentLetter in 'qz': #'QZ':
        score = 10#1
        complete = 1
    elif currentLetter in '#':
        complete = 1
    
    return score, complete

def getHeuristic(gridState):
    #state, depth = gridState
    score = 0
    complete = 0
    #print(gridState)
    for i in range(gridState[0].rows):
        for j in range(gridState[0].cols):
            tempScore, tempComplete = Heuristic.getScore(gridState[0].__getitem__((i, j)))
            score += tempScore
            complete += tempComplete
    totalCells = gridState[0].rows*gridState[0].cols
    heuristic = score*(complete/totalCells)
    return heuristic

#loop through every cell in grid?
#for every cell in grid
#assign score to cell based on letter in that cell, according to letterGroups dictionary

#may be possible optimization in N time? Think about that from now til we meet again
# tonight
"""
loopEveryCell(letter):
    i = 0
    j = 0
    while(currentRow != totalRows-1 && currentColumn != totalColumns -1):
        while( i < totalRows-1):
            while (j < totalColumns-1):
                Grid[i][j].giveLetterScore()
                j+=1
            i+=1
"""
#print(giveWordHeuristic('DAG'))


