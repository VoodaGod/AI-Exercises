import sys
import string

sortedSet = set()
wordDict = {}
ladder = []
startWord = ""
endWord = ""

def isVectorValid(vector):
	return isWordValid(createWordFromVector(vector))

def isWordValid(sortedWord):
	#returns wether sortedWord is a valid combination
	if sortedWord in sortedSet:
		return True
	else:
		return False

def getValidWords(sortedWord):
	#returns list of words matching sorted string
	return wordDict[sortedWord]

def getArgs():
	#sets startWord & endWord to cmd args
	global startWord; global endWord
	if len(sys.argv) > 2:
		startWord = sys.argv[1]
		endWord = sys.argv[2]
	else:
		print("needs 2 arguments: \"<startWord> <endWord>\"")
		startWord = "lamp"
		endWord = "camping"

def loadWordList():
	#loads words from wordList.txt in root,
	#adds a wordVector to sortedSet
	#adds original word to wordDict{wordVector: [word1, word2]}
	file = open("wordList.txt")
	for line in file:
		word = line.rstrip()
		wordSorted = sortWord(word)
		sortedSet.add(wordSorted)
		wordDict.setdefault(wordSorted, []).append(word)
	file.close()

def sortWord(word):
	return "".join(sorted(word))

def createVectorFromWord(word):
	#returns a vector containing counts of chars in string
	vector = []
	for char in string.ascii_lowercase:
		vector.append(word.count(char))
	return vector

def createWordFromVector(vector):
	#returns a sorted word from a vector
	sortedWord = []
	for char in range(len(vector)):
		for count in range(vector[char]):
			sortedWord.append(string.ascii_lowercase[char])
	return "".join(sortedWord)

def getVectorDifference(vector1, vector2):
	diff = []
	for i in range(len(vector1)):
		diff.append(vector1[i] - vector2[i])
	return diff

def main():
	getArgs()
	loadWordList()
	print("startWord = " + startWord + ", endWord = " + endWord)
	startWordVector = createVectorFromWord(startWord)
	endWordVector = createVectorFromWord(endWord)


main()