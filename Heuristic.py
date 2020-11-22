def giveLetterScore(letter):
    letterGroups = {
        'Group1': "AEILNRST",
        'Group2': "DGOPU",
        'Group3': "BCFHM",
        'Group4': "KVWY",
        'Group5': "JX",
        'Group6': "QZ",
        'Group7': "#"
    }
    currentLetter = letter.upper
    if (currentLetter) in letterGroups['Group1']:
        currentLetter.score = 10
    if(currentLetter) in letterGroups['Group2']:
        currentLetter.score = 9
    if(currentLetter) in letterGroups['Group3']:
        currentLetter.score = 7
    if(currentLetter) in letterGroups['Group4']:
        currentLetter.score =4
    if(currentLetter) in letterGroups['Group5']:
        currentLetter.score = 2
    if(currentLetter) in letterGroups['Group6']:
        currentLetter.score = 1
    if(currentLetter) in letterGroups['Group7']:
       currentLetter.score = 0
    return currentLetter.score

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



