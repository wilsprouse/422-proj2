import sys
import math
import WordFinder
import AStar
import Grid

RUN_CONSTANT = 5
RUN_MULT = 2
MAX_ATTEMPTS = 50

# ----------------------
# HELP PRINTING FUNCs.
# ----------------------
def printWithStarter(string, start='', end='\n'):
    print(f'{start}{string}', end=end)
def help_general(start=''):
    printWithStarter('Crossword Builder v1.0\n', start=start)
    help_run(start=start+'\t')
    print()
    help_dict(start=start + '\t')

def help_run(start=''):
    printWithStarter('python Main.py crossword <options>',start=start)
    printWithStarter('\t-r, --row: Sets the row length (defaults to 3)',start=start)
    printWithStarter('\t-c, --column: sets the column length (defaults to 3)',start=start)
    printWithStarter('\t-d, --dictionary: choose a backing dictionary file (supports only txt files currently)',start=start)
    printWithStarter('\t-e, --export: set an export file to return the completed grid (supports txt and html)',start=start)
    print()
    printWithStarter('\t-k, ----choiceConstant: choose minimum choices (used for testing)',start=start)
    printWithStarter('\t-m, --choiceMultiplier: choose choice multiplier (used for testing)',start=start)

def help_dict(start=''):
    printWithStarter('python Main.py dictionary [file]',start=start)

# ----------------------
# MAIN RUN
# ----------------------

def main(args, argv):
    #print('Welcome to Crossword Calculator v1.0!')
    #if args
    if argv[1] == 'dictionary':                         # CREATING DICTIONARY
        if args == 2:                                       # ERROR: Not enough params
            help_dict()
            return False
        if args > 3:                                        # ERROR: Too many params
            print('Error: To many parameters.')
            help_dict()
        return createDictionary(argv[2])                        # run dictionary maker
    elif argv[1] == 'crossword':                        # RUNNING CROSSWORD MAKER
        if args == 2:                                       # ERROR: Not enough params
            help_run()
            return False
        return run(args, argv)                              # run crossword maker
    else:                                               # INCORRECT FUNCTION (ERROR)
        print(f'\'{argv[1]}\' is not a valid command')
        print()
        help_general()
        return False

def run(args, argv):
    # Parse Values
    row = 3
    col = 3
    mult = RUN_MULT/max(row, col)
    const = (RUN_CONSTANT//max(row, col)) + 1
    dictname = 'txt_files/default_dict.txt'
    exportname = None

    index = 2
    #print(args)
    while index < args:
        # parse tags
        tag = argv[index]
        index += 1
        if tag == '-r' or tag == '--row':               # SET ROW LENGTH
            if index == args:
                print('No value given for row')
                return False
            try:
                row = int(argv[index])
            except ValueError:
                print(                                      # ERROR: param not integer
                    f'Error setting row: \'{argv[index]}\' not integer.')
                return False
        elif tag == '-c' or tag == '--column':             # SET COL LENGTH
            if index == args:
                print('No value given for column')
                return False
            try:
                col = int(argv[index])
            except ValueError:
                print(                                      # ERROR: param not integer
                    f'Error setting col: \'{argv[index]}\' not integer.')
                return False
        elif tag == '-k' or tag == '--choiceConstant':  # SET CONSTANT
            if index == args:
                print('No value given for column')
                return False
            try:
                const = int(argv[index])
            except ValueError:
                print(  # ERROR: param not integer
                    f'Error setting col: \'{argv[index]}\' not integer.')
                return False
        elif tag == '-m' or tag == '--choiceMultiplier':# SET MULTIPLIER
            if index == args:
                print('No value given for column')
                return False
            try:
                mult = int(argv[index])
            except ValueError:
                print(                                      # ERROR: param not integer
                    f'Error setting col: \'{argv[index]}\' not integer.')
                return False
        elif tag == '-d' or tag == '--dictionary':      # SET BACKING DICTIONARY
            if index == args:
                print('No value given for dictionary')
                return False
            dictname = argv[index]
        elif tag == '-e' or tag == '--export':          # SET EXPORT FILE
            if index == args:
                print('No value given for export file')
                return False
            exportname = argv[index]
        else:                                           # INCORRECT TAG (ERROR)
            print(f'Tag \'{tag}\' does not exist.')
            print()
            help_run()
            return False
        index += 1

    # Setup run
    dictionary = WordFinder.WordFinder()
    try:
        dictionary.importFromFile(dictname, max(row, col))
    except FileNotFoundError:
        print(f'Error reading dictionary: File {dictname} could not be read.')
        return False

    # print(f'{row}, {col}')
    for _ in range(MAX_ATTEMPTS + int(math.pow(row + col, 2))):
        grid, iterations = AStar.aStarSearch(Grid.Grid(row, col), dictionary, choiceMin=const, choiceMult=mult)
        if grid is not None: break
    if grid is None:
        print('Crossword creation failed. Exiting')
        return False
    print(f'Crossword created!!')

    if exportname is None:
        print(str(grid))
    elif not export(exportname, grid):
        print(str(grid))
    return True

def export(filepath, grid):
    try:
        extension = filepath.split('.')[-1]
        if extension == 'txt':
            fp = open(filepath, 'w')
            fp.write(str(grid))
        elif extension == 'html':
            fp = open(filepath, 'w')
            pass # For shoshanah to do
        else:
            print(f'Error: {extension} file not supported.')
            return False
        fp.close()
        return True
    except FileNotFoundError:
        print('Error creating export file, printing to stdout.')
    return False

def createDictionary(filepath):
    try:
        WordFinder.create_valid_dictionary(filepath)
        print('New dictionary created.')
        return True
    except FileNotFoundError:
        print(f'File \'{filepath}\' not valid.')
        return False



if __name__ == '__main__':
    argv = sys.argv
    if len(argv) < 2:
        help_general()
    else:
        main(len(argv), argv)