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
		startWord = ""
		endWord = ""
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
	#returns sum of absolute Values in vector
	length = 0
	for charCount in vector:
		length += abs(charCount)
	return length


def climbLadderSmart(currentVector, endVector):
	#climb ladder by only shortening distance vector
	if currentVector == endVector:
		ladder.append(currentVector)
		return True

	diffVector = getVectorDifference(currentVector, endVector)
	for char in range(len(currentVector)):
		charCount = diffVector[char]
		newVector = list(currentVector)
		if charCount > 0:
			newVector[char] -= 1
		elif charCount < 0:
			newVector[char] += 1
		elif charCount == 0:
			continue

		if isVectorValid(newVector):
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
		exploredSet.clear()
		if depthLimitedSearch(startVector, endVector, depth):
			return True
		else:
			depth += 1
	return False


def depthLimitedSearch(currentVector, endVector, limit):
	if currentVector == endVector:
		ladder.append(currentVector)
		return True
	if limit == 0:
		return False
	exploredSet.add(getWordFromVector(currentVector))

	if climbLadderSmart(currentVector, endVector):
		print("finished with climbLadderSmart")
		return True

	for char in range(len(currentVector)):
		child = list(currentVector)
		diffLength = getVectorLength(getVectorDifference(currentVector, endVector))
		if(diffLength <= 0):
			#add char
			child[char] = currentVector[char] + 1
			if getWordFromVector(child) not in exploredSet and isVectorValid(child):
				if depthLimitedSearch(child, endVector, limit - 1):
					ladder.append(currentVector)
					return True
			#remove char
			child[char] = currentVector[char] - 1
			if getWordFromVector(child) not in exploredSet and isVectorValid(child):
				if depthLimitedSearch(child, endVector, limit - 1):
					ladder.append(currentVector)
					return True
		if(diffLength > 0):
			#remove char
			child[char] = currentVector[char] - 1
			if getWordFromVector(child) not in exploredSet and isVectorValid(child):
				if depthLimitedSearch(child, endVector, limit - 1):
					ladder.append(currentVector)
					return True
			#add char
			child[char] = currentVector[char] + 1
			if getWordFromVector(child) not in exploredSet and isVectorValid(child):
				if depthLimitedSearch(child, endVector, limit - 1):
					ladder.append(currentVector)
					return True

	return False


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
		#ladder must be longer than direct distanceVector
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

	startWord = startEnd[0]
	endWord = startEnd[1]
	wordLadder = []
	if doLadder(startWord, endWord):
		wordLadder = getWordLadder(startWord, endWord)
		print(str(wordLadder))
		ladder.clear()
	file = open("output.txt", "w")
	for word in wordLadder:
		file.write(word + "\n")
	file.close()
	print("")

	'''
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
	'''

main()