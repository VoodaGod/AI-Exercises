import sys
import string

sortedSet = set()
wordDict = {}
ladder = []

def isVectorValid(vector):
	return isWordValid(getWordFromVector(vector))

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
	if len(sys.argv) > 2:
		startWord = sys.argv[1]
		endWord = sys.argv[2]
	else:
		print("takes 2 arguments: \"<startWord> <endWord>\"")
		startWord = "campos"
		endWord = "campus"
	return (startWord, endWord)

def loadWordList():
	#loads words from wordList.txt in root,
	#adds a wordVector to sortedSet
	#adds original word to wordDict{wordVector: [word1, word2]}
	print("loading words from wordList.txt")
	file = open("wordList.txt")
	for line in file:
		word = line.rstrip()
		wordSorted = getSortedWord(word)
		sortedSet.add(wordSorted)
		wordDict.setdefault(wordSorted, []).append(word)
	print("done")
	file.close()

def getSortedWord(word):
	return "".join(sorted(word))

def getVectorFromWord(word):
	#returns a vector containing counts of chars in string
	vector = []
	for char in string.ascii_lowercase:
		vector.append(word.count(char))
	return vector

def getWordFromVector(vector):
	#returns a sorted word from a vector
	sortedWord = []
	for char in range(len(vector)):
		for count in range(vector[char]):
			sortedWord.append(string.ascii_lowercase[char])
	return "".join(sortedWord)

def getVectorDifference(vector1, vector2):
	#returns the diffVector vector1-vector2
	diff = []
	for i in range(len(vector1)):
		diff.append(vector1[i] - vector2[i])
	return diff


def climbLadderSmart(currentVector, endVector):
	#climb ladder by trying to minimize the length of the distance vector
	if not isVectorValid(currentVector):
		return False
	if currentVector == endVector:
		return True

	diffVector = getVectorDifference(currentVector, endVector)
	for i in range(len(currentVector)):
		charCount = diffVector[i]
		newVector = list(currentVector)
		if charCount > 0:
			newVector[i] -= 1
		elif charCount < 0:
			newVector[i] += 1
		elif charCount == 0:
			continue

		if climbLadderSmart(newVector, endVector):
			ladder.append(newVector)
			return True
		else:
			continue
	return False


#TODO def climbLadderDumb():


def getWordLadder(startWord, endWord):
	#converts ladder of vectors to words
	#replaces start and end with correct words
	wordLadder = []
	for vector in ladder:
		words = getValidWords(getWordFromVector(vector))
		wordLadder.append(words[0])
	wordLadder.insert(0, startWord)
	wordLadder.pop()
	wordLadder.append(endWord)
	return wordLadder


def doLadder(startWord, endWord):
	if isWordValid(getSortedWord(startWord)) and isWordValid(getSortedWord(endWord)):
		print("startWord = " + startWord + ", endWord = " + endWord)
	else:
		print("invalid word(s)!")
		return

	startWordVector = getVectorFromWord(startWord)
	endWordVector = getVectorFromWord(endWord)

	if climbLadderSmart(startWordVector, endWordVector):
		ladder.reverse()
		print("ladder found!")
		print(str(getWordLadder(startWord, endWord)))
	else:
		print("no ladder found :(")
	ladder.clear()


def main():
	loadWordList()
	print("")

	#startEnd = getArgs()
	#startWord = startEnd[0]; endWord = startEnd[1]
	#doLadder(startWord, endWord)

	startWord = "croissant"; endWord = "baritone"
	doLadder(startWord, endWord)
	print("")

	startWord = "crumpet"; endWord = "treacle"
	doLadder(startWord, endWord)
	print("")

	startWord = "apple"; endWord = "pear"
	doLadder(startWord, endWord)
	print("")

	startWord = "lead"; endWord = "gold"
	doLadder(startWord, endWord)
	print("")


main()