import sys
import string

sortedSet = set()
exploredSet = set()
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
		startWord = "pug"
		endWord = "gum"
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

def getVectorLength(vector):
	length = 0
	for charCount in vector:
		length += abs(charCount)
	return length


def climbLadderSmart(currentVector, endVector):
	#climb ladder by only shortening distance vector
	if not isVectorValid(currentVector):
		return False
	if currentVector == endVector:
		ladder.append(currentVector)
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
			ladder.append(currentVector)
			return True
		else:
			continue
	return False


def iterativeDeepeningSearch(startVector, endVector, startDepth):
	depth = startDepth
	while depth < len(sortedSet):
		print("searching to depth " + str(depth))
		if depthLimitedSearch(startVector, endVector, depth):
			return True
		else:
			depth += 1
	return False


def depthLimitedSearch(currentVector, endVector, limit):
	if not isVectorValid(currentVector):
		return False
	if currentVector == endVector:
		ladder.append(currentVector)
		return True
	elif limit == 0:
		return False

	if climbLadderSmart(currentVector, endVector):
		return True

	child = getChild(currentVector, endVector)
	if child is not None:
		exploredSet.add(getWordFromVector(child))
		if depthLimitedSearch(child, endVector, limit - 1):
			ladder.append(currentVector)
			return True
	else:
		return False


def getChild(parentVector, endVector):
	diffLength = getVectorLength(endVector) - getVectorLength(parentVector)
	for char in range(len(parentVector)):
		child = list(parentVector)
		if diffLength >= 0:
			child[char] = parentVector[char] + 1
		else:
			child[char] = parentVector[char] - 1
		if isVectorValid(child) and getWordFromVector(child) not in exploredSet:
			return child
		else:
			child = list(parentVector)
			if diffLength >= 0:
				child[char] = parentVector[char] - 1
			else:
				child[char] = parentVector[char] + 1
			if isVectorValid(child) and getWordFromVector(child) not in exploredSet:
				return child
	#return None


def getWordLadder(startWord, endWord):
	#converts ladder of vectors to words
	#replaces start and end with correct words
	wordLadder = []
	for vector in ladder:
		words = getValidWords(getWordFromVector(vector))
		wordLadder.append(words[0])
	wordLadder[0] = startWord
	wordLadder[-1] = endWord
	return wordLadder


def doLadder(startWord, endWord):
	if isWordValid(getSortedWord(startWord)) and isWordValid(getSortedWord(endWord)):
		print("startWord = " + startWord + ", endWord = " + endWord)
	else:
		print("invalid word(s)!")
		return

	startVector = getVectorFromWord(startWord)
	endVector = getVectorFromWord(endWord)
	ladderFound = True
	if not climbLadderSmart(startVector, endVector):
		minLadderLength = getVectorLength(getVectorDifference(startVector, endVector))
		if not iterativeDeepeningSearch(startVector, endVector, minLadderLength):
			print("no ladder found :(")
			ladderFound = False

	ladder.reverse()
	return ladderFound


def main():
	startEnd = getArgs()
	loadWordList()
	print("")

	#'''
	startWord = startEnd[0]; endWord = startEnd[1]
	if doLadder(startWord, endWord):
		print(str(getWordLadder(startWord, endWord)))
		ladder.clear()
	print("")
	#'''

	startWord = "croissant"; endWord = "baritone"
	if doLadder(startWord, endWord):
		print(str(getWordLadder(startWord, endWord)))
		ladder.clear()
	print("")

	startWord = "crumpet"; endWord = "treacle"
	if doLadder(startWord, endWord):
		print(str(getWordLadder(startWord, endWord)))
		ladder.clear()
	print("")

	startWord = "apple"; endWord = "pear"
	if doLadder(startWord, endWord):
		print(str(getWordLadder(startWord, endWord)))
		ladder.clear()
	print("")

	startWord = "lead"; endWord = "gold"
	if doLadder(startWord, endWord):
		print(str(getWordLadder(startWord, endWord)))
		ladder.clear()
	print("")


main()