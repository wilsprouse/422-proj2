import re
from Grid import *
import util
import copy
import json

class WordFinder:
    def __init__(self):
        self.__dict = dict()

    def importFromList(self, list):
        for word in list:
            self.addWord(word)

    def importFromFile(self, filepath):
        """
        imports words from backing file (.txt)
        :param filepath:
        :return:
        """
        fp = open(filepath, 'r')
        for word in fp:
            print(word)
            self.addWord(word[:-1])
        fp.close()

    def importFromJson(self, filepath):
        """
        imports words from json file (WARNING: size and loadtime for a json file are both worse, if possible use importFromFile)
        :param filepath:
        :return:
        """
        fp = open(filepath, 'r')
        self.__dict = json.load(fp)
        fp.close()

    def addWord(self, word):
        dictionaryLevel = self.__dict # Save access level (for quicker accessing)
        #print(id(dictionaryLevel))
        for index in range(len(word)):
            #print(f"\t{id(dictionaryLevel)}")
            char = word[index].lower()

            if char not in dictionaryLevel: # if level not initialized
                dictionaryLevel[char] = {'letters': dict(), 'isComplete': False} # initialize dictionary at level along w isComplete value (initialized to False)

            if index + 1 == len(word): # if word is complete (i.e no more letters to add), set level to complete.
                dictionaryLevel[char]['isComplete'] = True
            else: # if the word is not complete, load sub-dictionary.
                dictionaryLevel = dictionaryLevel[char]['letters']

    def getWords(self, line):
        ret = []
        for start in range(len(line) - 1): # Start at all points except the last one (will not be adding one letter words)
            states = util.Queue()
            stateLine = line
            if start > 0: # if not adding to beginning of line, add wall character to start of word
                stateLine = line.copy() # copy line so original not changed
                stateLine[start - 1] = CELL_WALL
            states.push((stateLine, start, self.__dict)) #insert starting state to queue. Values are line state, position in line, and dictionary level.

            while not states.isEmpty():
                currLine, pos, dictionaryLevel = states.pop()
                #if pos != 0:
                #    print(f"{'  ' * pos}{currLine[pos - 1]} -> {id(dictionaryLevel)}")
                #else:
                #    print(f"{'  ' * pos}head -> {id(dictionaryLevel)}")

                if pos >= len(line):
                    continue

                for validChar in line[pos]:
                    if validChar in dictionaryLevel:
                        newLine = currLine.copy()
                        newLine[pos] = Cell(validChar)

                        if dictionaryLevel[validChar]['isComplete']:
                            if pos + 1 < len(newLine): # if pos + 1 in line (no IndexError)
                                newLine[pos + 1] = CELL_WALL
                            ret.append(newLine)

                        states.push((newLine, pos + 1, dictionaryLevel[validChar]['letters']))
        return ret

    def getDict(self):
        return copy.deepcopy(self.__dict)

    def exportToJson(self, filepath):
        fp = open(filepath, 'w')
        json.dump(self.__dict, fp, indent='\t', sort_keys=True)
        fp.close()



def create_valid_dictionary(filepath):
    try:
        fp = open(filepath, 'r')
    except FileNotFoundError:
        raise FileNotFoundError()
    #from Grid import Cell
    holder = set()                              # Holder to make sure there are no repeating words
    searcher = f"^[{Cell.ALPHABET[:-1]}]+$"     # Scan for characters excluding the wall character
    for line in fp:
        edited = re.search(searcher, line.lower()).group()
        if edited != None and len(edited) > 1:
            holder.add(edited)
    fp.close()

    newFilepath = filepath[:filepath.rfind('.')] + '.new' + filepath[filepath.rfind('.'):]
    fp = open(newFilepath, "w")
    for word in holder:
        fp.write(f"{word}\n")
    fp.close()

def __test_wordFinder():
    dictionary = WordFinder()
    dictionary.importFromFile("dictionary.new.txt")
    test = dictionary.getWords([Cell('afeqfvyhx'), Cell('sgcqerirx'), Cell('sderx'), Cell('axad'), Cell('yxedo')])
    for line in test:
        print(line)


def __printLevel(dictionaryLevel, depth):
    for char in dictionaryLevel:
        print('  ' * depth + char, end='')
        if dictionaryLevel[char]['isComplete']:
            print(' (complete word)')
        else:
            print()
        printLevel(dictionaryLevel[char]['letters'], depth + 1)

if __name__ == '__main__':
    #create_valid_dictionary("dictionary.txt")
    #test_wordFinder()
        


