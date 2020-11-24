import util
import math
import random
import WordFinder
import Grid
import time
#from guppy import hpy
import Heuristic


def nullHeuristic(gridState):
    #newState, depth = gridState
    #return depth
    return random.random()
    #return 1

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
    #totalCells = gridState[0].rows*gridState[0].cols
    #heuristic = score*(complete/totalCells)
    if complete == 0:
        heuristic = 0
    else:
        heuristic = score/complete
    return heuristic

#loop through every cell in grid?


def aStarSearch(grid, dictionary, heuristic=getHeuristic, choiceMult=1, choiceMin=1):
    visited = [] # Swapped to dict for faster accessing
    sorter = util.PriorityQueueWithFunction(heuristic)
    sorter.push((grid, 0))

    iterations = 0
    times_visited = 0
    while not sorter.isEmpty():
        gridState, depth = sorter.pop()
        iterations += 1
        #if iterations > 2:
        #    break
        # print(f"iteration {iterations}: testing state at depth {depth} with grid:")
        # print(str(gridState))
        if gridState in visited:
             times_visited += 1
             continue
        visited.append(gridState)
        #print(f"Scanning {gridState}", end='\t')
        if gridState.isComplete() and gridState.isValid(dictionary): # fine to test it this way since the python and statement will only test the second case if the first one is true
            #print("DONE")
            #h = hpy()
            #print(h.heap())
            #print(f'Found same state {times_visited} times.')
            return gridState, iterations

        successors = gridState.getNextGridStates(dictionary, int(choiceMult * (depth + 1)) + choiceMin)
        random.shuffle(successors)
        #print(f"Expanding from {gridState}")
        for newState in successors:
            #print(newState)
            if newState.isValid(dictionary):
                sorter.push((newState, depth + 1))
            else:
                del(newState)
        #del(gridState)
    #print(f'Found same state {times_visited} times.')

    return None, iterations


def main(dictionary):
    grid = Grid.Grid(5,5)
    #print('------------------------------------')
    completedGrid, iterations = aStarSearch(grid, dictionary, choiceMult=1)
    print(f'completed grid after {iterations} iterations.\nResult:\n{str(completedGrid)}')


if __name__ == '__main__':
    dictionary = WordFinder.WordFinder()
    startTime = time.time()
    dictionary.importFromFile('./txt_files/5000-words.txt')
    endTime = time.time()
    print(f'Dictionary loaded in {endTime - startTime} sec.')
    #dictionary.importFromList(['is', 'it', 'to', 'an', 'on', 'no'])
    print('Beginning crossword maker...')
    startTime = time.time()
    main(dictionary)
    endTime = time.time()
    print(f'Crossword created in {endTime - startTime} sec.')
