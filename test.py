import sys
import run
import time
from os import system, name

def main(argc, argv):
    if argc < 4 or argc > 4:
        print(f'incorrect number of parameters (Input {argc}, should be 4)')
        return
    row = int(argv[1])
    col = int(argv[2])
    runs = int(argv[3])
    averageTime = 0
    successes = 0
    for _ in range(runs):
        commandLine = f'Main.py crossword -r {row} -c {col}'
        inpt = commandLine.split(' ')
        startTime = time.time()
        test = run.main(len(inpt), inpt)
        averageTime += time.time() - startTime
        if test:
            successes += 1
    #if name == 'nt':
    #    _ = system('cls')
    #else:
    #    _ = system('clear')

    print(f'Algorithm succeeded {successes} / {runs} times.')
    print(f'Average runtime: {averageTime / runs} sec.')




if __name__ == '__main__':
    argv = sys.argv
    if len(argv) < 2:
        help_general()
    else:
        main(len(argv), argv)