import util
import random
import WordFinder
import Grid
import time


def nullHeuristic(gridState):
    return random.random()


def aStarSearch(grid, dictionary, heuristic=nullHeuristic):
    visited = [] # Swapped to dict for faster accessing
    sorter = util.PriorityQueueWithFunction(heuristic)
    sorter.push((grid, 0, []))

    iterations = 0
    while not sorter.isEmpty():
        gridState, depth, history = sorter.pop()
        iterations += 1
        #if iterations > 2:
        #    break
        # print(f"iteration {iterations}: testing state at depth {depth} with grid:")
        # print(str(gridState))
        if gridState in visited:
            continue
        visited.append(gridState)
        #print(f"Scanning {gridState}", end='\t')
        if gridState.isComplete() and gridState.isValid(dictionary): # fine to test it this way since the python and statement will only test the second case if the first one is true
            #print("DONE")
            return gridState, iterations

        successors = gridState.getNextGridStates(dictionary)
        random.shuffle(successors)
        #print(f"Expanding from {gridState}")
        for newState in successors:
            #print(newState)
            newHistory = list(history)
            newHistory.append(newState)
            sorter.push((newState, depth + 1, newHistory))
        #del(gridState)

    return None


def main(dictionary):
    grid = Grid.Grid(4,4)
    #print('------------------------------------')
    completedGrid, iterations = aStarSearch(grid, dictionary)
    print(f'completed grid after {iterations} iterations.\nResult:\n{str(completedGrid)}')


if __name__ == '__main__':
    dictionary = WordFinder.WordFinder()
    startTime = time.time()
    dictionary.importFromFile('usa.txt')
    endTime = time.time()
    print(f'Dictionary loaded in {endTime - startTime} sec.')
    #dictionary.importFromList(['is', 'it', 'to', 'an', 'on', 'no'])
    print('Beginning crossword maker...')
    startTime = time.time()
    main(dictionary)
    endTime = time.time()
    print(f'Crossword created in {endTime - startTime} sec.')