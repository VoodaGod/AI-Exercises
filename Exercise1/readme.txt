Name: Jason Janse van Rensburg
Matrikelnummer: 03664065

I used Python 3.5.2

My solution creates a set of strings of alphabetically sorted characters from the wordList.txt
and maps words from the wordList.txt to their sorted strings in a dictionary.
Then it converts the start and end words to vectors which describe how often each character appears in them.
At first it tries to find a direct solution by only adding/subtracting characters that minimize the
distance vector between the current word and the end word.
For example: pug -> pugs
	the distance vector has length 1 because pug is missing 1 's', so an 's' is added
If this fails, the program tries to find a ladder using iterative deepening, with
startDepth = length of distance vector from start to end word, because it is known that this is the minimum
length of the ladder.
This is combined with the direct solution search explained above