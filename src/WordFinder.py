import re
import Grid
import util
import copy
import json

class WordFinder:
    def __init__(self):
        self.__dict = dict()
        self.__popN = dict()
        self.__wordN = 0
        self.__maxdepth = 0

    def importFromList(self, list, maxWordLength=9999):
        for word in list:
            if len(word) <= maxWordLength:
                self.__wordN += 1
                self.addWord(word)

    def importFromFile(self, filepath, maxWordLength=9999):
        """
        imports words from backing file (.txt)
        :param filepath:
        :return:
        """
        fp = open(filepath, 'r')
        for word in fp:
            if len(word) <= maxWordLength + 1:
                self.__wordN += 1
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
        if len(word) not in self.__popN:
            self.__popN[len(word)] = 0
        self.__popN[len(word)] += 1
        dictionaryLevel = self.__dict # Save access level (for quicker accessing)
        #print(id(dictionaryLevel))
        if len(word) > self.__maxdepth:
            self.__maxdepth = len(word)
        for index in range(len(word)):
            #print(f"\t{id(dictionaryLevel)}")
            char = word[index].lower()

            if char not in dictionaryLevel: # if level not initialized
                dictionaryLevel[char] = {'letters': dict(), 'isComplete': False} # initialize dictionary at level along w isComplete value (initialized to False)

            if index + 1 == len(word): # if word is complete (i.e no more letters to add), set level to complete.
                dictionaryLevel[char]['isComplete'] = True
            else: # if the word is not complete, load sub-dictionary.
                dictionaryLevel = dictionaryLevel[char]['letters']

    def isWord(self, line):
        assert all([cell.isChosen() for cell in line])
        dictionaryLevel = self.__dict

        for index in range(len(line)):
            char = line[index].getChosen()
            if char is None or char not in dictionaryLevel:
                return False
            else:
                if index + 1 == len(line) and dictionaryLevel[char]['isComplete']:
                    return True
                dictionaryLevel = dictionaryLevel[char]['letters']
        return False

    def getMinLength(self, n, max):
        curr_words = 0
        minLength = n
        for i in range(n, 0, -1):
            if n in self.__popN:
                curr_words += self.__popN[n]
            if curr_words > max:
                minLength = i
        return minLength

    def getWords(self, line, minSize=2):
        minSize = min(self.__maxdepth, minSize)

        ret = []
        for start in range(len(line) - (minSize-1)): # Start at all points except the last one (will not be adding one letter words)
            states = util.Stack()
            stateLine = line
            if start > 0: # if not adding to beginning of line, add wall character to start of word
                if stateLine[start - 1].isChosen():
                    continue
                stateLine = copy.copy(line) # copy line so original not changed
                stateLine[start - 1] = Grid.CELL_WALL
            states.push((stateLine, start, self.__dict)) #insert starting state to queue. Values are line state, position in line, and dictionary level.

            while not states.isEmpty():
                currLine, pos, dictionaryLevel = states.pop()
                if pos >= len(line):
                    continue

                for validChar in line[pos]:
                    if validChar in dictionaryLevel:
                        newLine = copy.copy(currLine)
                        newLine[pos] = Grid.Cell(validChar)

                        if dictionaryLevel[validChar]['isComplete']:
                            #foundWord
                            if pos + 1 < len(newLine): # if pos + 1 in line (no IndexError)
                                if currLine[pos + 1].isChosen():
                                    continue
                                else:
                                    newLine[pos + 1] = Grid.CELL_WALL
                            if pos - start >= minSize:
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
    fp = open(filepath, 'r')
    #from Grid import Cell
    holder = set()                              # Holder to make sure there are no repeating words
    searcher = f"^[{Grid.Cell.ALPHABET[:-1]}]+$"     # Scan for characters excluding the wall character
    for line in fp:
        edited = re.search(searcher, line.lower())
        if edited != None and len(edited.group()) > 1:
            holder.add(edited.group())
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

def __testIsWord():
    dictionary = WordFinder()
    dictionary.importFromList(['apple', 'notapple'])
    test = [Grid.Cell('a'), Grid.Cell('p'), Grid.Cell('p'), Grid.Cell('l'), Grid.Cell('e')]
    print(dictionary.isWord(test))
    test = [Grid.Cell('a'), Grid.Cell('p'), Grid.Cell('p'), Grid.Cell('l'), Grid.Cell('o')]
    print(dictionary.isWord(test))

if __name__ == '__main__':
    pass
    #create_valid_dictionary("dictionary.txt")
    #__test_wordFinder()
    __testIsWord()
#Reached end