
def loadWordList():
	wordListFile = open("wordList.txt")
	word = ""
	for line in wordListFile:
		word = line.rstrip()


loadWordList()