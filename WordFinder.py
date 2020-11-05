import re

class __WordNode:
    def __init__(self):
        self.__letter = None
        self.__next = dict()

    def add_word(self, word:str):
        if len(word) != 0: # if word is not an empty string
            self.__letter = word
            if len(word) > 0:
                if word[1] not in self.__next:
                    self.__next[word[1]] = __WordNode()
                self.__next[word[1]].add_word(word[1:]) # Repeat process at next rung down, i.e. add "hunt" -> "unt" -> "nt" -> "t"

    def get_word(self, line):
        if len(line) != 0:
            for cell in line[:-2]:
                for letter in cell:
class WordFinder:
    def __init__(self, filename):
        """
        WordFinder initializer function. Takes in a file path to a list of usable words.
        :param filename: path to dictionary txt file
        """
        try:
           fp = open(filename, "r")
        except FileNotFoundError:
            raise FileNotFoundError("Dictionary file could not be open, file may not exist")
