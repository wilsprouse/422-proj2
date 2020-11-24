def getScore(letter):
    score = 0
    complete = 0
    currentLetter = letter.getChosen()
    #print(currentLetter)


    if currentLetter == None:
        return 0,0
    elif currentLetter in 'ea':
        score = 5.61
        complete = 1
    elif currentLetter in 'riot': #'DGOPU':
        score = 9.24
        complete = 1
    elif currentLetter in 'nslc': #'BCFHM':
        score = 12.59
        complete = 1
    elif currentLetter in 'udpmh': #'KVWY':
        score = 18.51
        complete = 1
    elif currentLetter in 'gb': #'JX':
        score = 33
        complete = 1
    elif currentLetter in 'fyw': #'QZ':
        score = 38.64
        complete = 1
    elif currentLetter in 'kvxzjq': #'QZ':
        score = 56.88
        complete = 1
    elif currentLetter in '#':
        score = 5
    """
    if currentLetter == None:
        return 0,0
    elif currentLetter in 'aeilnrst':
        score = 1
        complete = 1
    elif currentLetter in 'dgopu': #'DGOPU':
        score = 10
        complete = 1
    elif currentLetter in 'bcfhm': #'BCFHM':
        score = 20
        complete = 1
    elif currentLetter in 'kvwy': #'KVWY':
        score = 30
        complete = 1
    elif currentLetter in 'jx': #'JX':
        score = 40
        complete = 1
    elif currentLetter in 'qz': #'QZ':
        score = 100
        complete = 1
    elif currentLetter in '#':
        score = 1
    """
    return score, complete



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


