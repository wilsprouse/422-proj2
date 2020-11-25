General:
--
The project is a program that generates a crossword puzzle. All words in all rows and columns are valid, according to a specific dictionary which can be provided by the user. 

Requirements and Design Documentation: 
--
The intent is to produce a viable, valid crossword puzzle with the size dimensions of length and width provided by the user. 
The basic outline of how the program runs or works is:
User enters the number of rows and columns.
The dictionary then loads all possible words into a very big non-binary-tree data structure, with an indicator on the node of a tree when a word is complete from the root to that node.
A word is chosen.
Word is placed in row or column. 
When word is placed, cell’s ALPHABET attribute shuts off all other possible letters except chosen letter.
When a word is placed, the letters for the cells where a word is placed are chosen, all other possible letters are eliminated for that cell. In a bit-array called ALPHABET for each cell, the bits representing all letters that were not chosen are turned off.
When a word is placed, that word’s letters are decided for at least some of the cells of the row or column where the word is placed. Say the word is placed horizontally, say in row 2, columns 1-5. We call the functions of shutOffVerticalFollow() on the cells above the word, on cells of row 1, columns 1-5. For any letter in the word placed, shutOffVerticalPrecede() turns to 0 the bits for any letter in the ALPHABET-array per cell that cannot precede the letter assigned to the cell below, because those two letters would make an unattested combination. (Attested means that the linguistic construction [e.g. 2-letter combination] exists in any word in the language; unattested means that the linguistic construction [e.g. 2-letter combination] does not exist anywhere in the language.) We call shutOffVerticalFollow() to shut off the bits of the letters that would make an invalid 2-letter combination on all the cells below the placed word. 
We would follow the same logic when a word is placed vertically down a column with shutOffHorizontalPrecede() and shutOffHorizontalFollow() to shut off the bits of the letters that would make an unattested combination, in order to avoid ever putting an unattested 2-letter combination perpendicular to a word that has just been placed.   
Continues to fill the grid, repeating steps D through I, gathering words from the tree data structure, until the grid is as complete as possible.
The output can be viewed in the command line interface, or via double clicking the html file that gets created.

Future Development:
--
Plans for future development are to continue optimizing, shorten run-time, and offer users more variety of crossword puzzle themes and symmetrical designs. This works best on small puzzles, 5x5 or smaller, and the developers would like to see the grid be expanded with a valid puzzle still produced. At this point, clues for the solution to the puzzle generated are not developed, but that would be part of future development. In order to allow room for cleverness, word-play, or theme reference in the clues, the intent is not to merely give the dictionary definition for the clues. However perhaps a database or at least data structure matching solutions to clues with their clues could be accessible to the puzzle-generator in the future, and could allow users to include and coordinate numbering of clues with the row, column, or part of column or row to which the clue applies. 



Build, deployment and run process:
--
1. To start, clone this repository in your terminal. 
2. This will create the necessary files for the command line interface
3. To run the project use the run.py file
   - When running the project there are a number of flags to be used for customization such as:
     To specify rows use:
	-c <number_of_columns>
     To specify columns use:
	-r <number_of_rows>
     To specify a dictionary:
	-d <dictionary>
     To specify an output html file
	-e <export_file_name>
     To specify a multiplier (the further into the grid, the more words it will choose):
	-m <multiplier>
     To specify a constant (initial number of states the AStar will expand and the multiplier increases that value based on the depth.):
	-k <constant>

So creating a crossword with all the flags would wield a command that looks like:

$ python3 run.py -c 4 -r 4 -d dictionary.txt -e output.html -m 2 -k 4


Tests:
--
To test this, simply follow the instructions for how to run the project


Organization:
--
This is the README file in the main branch of Wil Sprouse’s 422-proj2 repository. The README and the src folder are in the home directory. The src directory contains all the code.

In the wiki are the following categories describing the process of building this project: Team roles, Coding parts delegated, meeting notes, developer logs.

