import sys
import WordFinder
import AStar
import Grid

RUN_CONSTANT = 5

# ----------------------
# HELP PRINTING FUNCs.
# ----------------------

def help_general(start='', end=''):
    print('Print the help stuff')

def help_run(start='', end=''):
    print('Print help info for run')

def help_dict(start='', end=''):
    print('Print help for create dictionary')

# ----------------------
# MAIN RUN
# ----------------------

def main(args, argv):
    #print('Welcome to Crossword Calculator v1.0!')
    #if args
    if argv[1] == 'dictionary':                         # CREATING DICTIONARY
        if args == 2:                                       # ERROR: Not enough params
            help_dict()
            return
        if args > 3:                                        # ERROR: Too many params
            print('Error: To many parameters.')
            help_dict()
        createDictionary(argv[2])                        # run dictionary maker
        return
    elif argv[1] == 'crossword':                        # RUNNING CROSSWORD MAKER
        if args == 2:                                       # ERROR: Not enough params
            help_run()
            return
        run(args, argv)                                     # run crossword maker
        return
    else:                                               # INCORRECT FUNCTION (ERROR)
        print(f'\'{argv[1]}\' is not a valid command')
        print()
        help_general()
        return

def run(args, argv):
    # Parse Values
    row = 3
    col = 3
    mult = 1/max(row, col)
    const = (RUN_CONSTANT//max(row, col)) + 1
    dictname = 'default_dict.txt'
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
                return
            try:
                row = int(argv[index])
            except ValueError:
                print(                                      # ERROR: param not integer
                    f'Error setting row: \'{argv[index]}\' not integer.')
                return
        elif tag == '-c' or tag == '--col':             # SET COL LENGTH
            if index == args:
                print('No value given for column')
                return
            try:
                col = int(argv[index])
            except ValueError:
                print(                                      # ERROR: param not integer
                    f'Error setting col: \'{argv[index]}\' not integer.')
                return
        elif tag == '-k' or tag == '--ChoiceConstant':  # SET CONSTANT
            if index == args:
                print('No value given for column')
                return
            try:
                const = int(argv[index])
            except ValueError:
                print(  # ERROR: param not integer
                    f'Error setting col: \'{argv[index]}\' not integer.')
                return
        elif tag == '-m' or tag == '--ChoiceMultiplier':# SET MULTIPLIER
            if index == args:
                print('No value given for column')
                return
            try:
                mult = int(argv[index])
            except ValueError:
                print(                                      # ERROR: param not integer
                    f'Error setting col: \'{argv[index]}\' not integer.')
                return
        elif tag == '-d' or tag == '--dictionary':      # SET BACKING DICTIONARY
            if index == args:
                print('No value given for dictionary')
                return
            dictname = argv[index]
        elif tag == '-e' or tag == '--export':          # SET EXPORT FILE
            if index == args:
                print('No value given for export file')
                return
            exportname = argv[index]
        else:                                           # INCORRECT TAG (ERROR)
            print(f'Tag \'{tag}\' does not exist.')
            print()
            help_run()
            return
        index += 1

    # Setup run
    dictionary = WordFinder.WordFinder()
    try:
        dictionary.importFromFile(dictname, max(row, col))
    except FileNotFoundError:
        print(f'Error reading dictionary: File {dictname} could not be read.')
        return

    # print(f'{row}, {col}')
    grid, iterations = AStar.aStarSearch(Grid.Grid(row, col), dictionary, choiceMin=const, choiceMult=mult)
    if exportname is None:
        print(f'Crossword created after {iterations} iterations.')
        print(str(grid))
    else:
        export(exportname)

def export(filepath):
    pass

def createDictionary(filepath):
    try:
        WordFinder.create_valid_dictionary(filepath)
        print('New dictionary created.')
    except FileNotFoundError:
        print(f'File \'{filepath}\' not valid.')


if __name__ == '__main__':
    argv = sys.argv
    if len(argv) < 2:
        help_general()
    else:
        main(len(argv), argv)