import random
import json
import re
import numpy as np
import time
import math

with open('guessableWords.json', 'r') as j:
	guessList = json.load(j)

with open('possibleWords.json', 'r') as j:
	answerList = json.load(j)

possGuessList = np.array(guessList['5'])
possAnswerList = np.array([answer[0] for answer in answerList['5']])
possAnswerFreq = np.array([answer[1] for answer in answerList['5']])


with open('guessCodes.json', 'r') as j:
	gCodes = json.load(j)

with open('answerCodes.json', 'r') as j:
	aCodes = json.load(j)

patternArray = np.load('patternArray.npy')

def getPattern(guess, answer):
	return patternArray[gCodes[guess], aCodes[answer]]


def randomWord():
	return random.choice(possAnswerList)

with open('firstGuess.json', 'r') as j:
	firstGuesses = json.load(j)

with open('secondGuess.json', 'r') as j:
	secondGuesses = json.load(j)

with open('thirdGuess.json', 'r') as j:
	thirdGuesses = json.load(j)

with open('fourthGuess.json', 'r') as j:
	fourthGuesses = json.load(j)


def I(p):
	return -math.log2(p)

def toTernary(n):
    if n == 0:
        return '00000'
    nums = []
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))
    return ''.join(reversed(nums)).zfill(5)

def fromTernary(pattern):
	return sum([int(pattern[i])*3**(4-i) for i in range(5)])

def possiblePatterns(guess, answerList):
	for tern in set(patternArray[gCodes[guess], answerList]):
		yield toTernary(tern)

# def lfreq(word):
# 	freq = {}
# 	for char in word:
# 		freq[char] = freq.get(char, 0) + 1
# 	return freq

# def getPattern(guess, word):
# 	pattern = []
# 	wfreq = lfreq(word)
# 	gfreq = {}
# 	for i in range(5):
# 		gchar = guess[i]
# 		wchar = word[i]
# 		currgfreq = gfreq.get(gchar, 0)
# 		currwfreq = wfreq.get(gchar, 0)
# 		if gchar == wchar:
# 			pattern.append(2)
# 		elif gchar != wchar and currwfreq > 0 and currgfreq < currwfreq:
# 			pattern.append(1)
# 		elif currwfreq == 0 or currgfreq >= currwfreq:
# 			pattern.append(0)
# 		gfreq[gchar] = currgfreq + 1
# 	return "".join(str(i) for i in pattern)

# def getMatches(dataList, possibleAnswers):
# 	matches = possibleAnswers.copy()
# 	for data in dataList:
# 		guess, pattern = data['guess'], data['pattern']
# 		for answer in possibleAnswers:
# 			wordPattern = getPattern(guess, answer)
# 			if pattern != wordPattern:
# 				matches.remove(answer)

# 	return matches

def getMatches(dataList):
	matchIndex = np.array(range(possAnswerList.size))
	for data in dataList:
		guess, pattern = data['guess'], data['pattern']
		tern = fromTernary(pattern)
		patterns = patternArray[gCodes[guess], :]
		newMatches = np.where(patterns == tern)
		matchIndex = np.intersect1d(matchIndex, newMatches, assume_unique=True)
	return matchIndex

def p(guess, pattern, answerList=np.array(range(possAnswerList.size))):
	if answerList.size == 0:
		return 0
	tern = fromTernary(pattern)
	patterns = patternArray[gCodes[guess], :]
	# Get the possible matches in the answer list
	matchIndex = np.where(patterns == tern)
	# Get the matches that are in the given matches and the new answer list
	newIndex = np.intersect1d(matchIndex, answerList, assume_unique=True)

	if newIndex.size == 0:
		return 0

	totalFreq = np.sum(possAnswerFreq[answerList])
	newFreq = np.sum(possAnswerFreq[newIndex])
	return newFreq/totalFreq


def bestGuess(dataList):

	info = {}

	answerMatches = getMatches(dataList)
	if len(answerMatches) == 1:
		return possAnswerList[answerMatches[0]]
	elif len(answerMatches) == 0:
		return randomWord()

	startTime = time.time()
	for i in range(possGuessList.size):
		# if i % 100 == 0 and i != 0:
		# 	print(possGuessList[i])
		# 	print(time.time() - startTime)
		# 	startTime = time.time()
		possGuess = possGuessList[i]
		E = 0
		for pattern in possiblePatterns(possGuess, answerMatches):
			prob = p(possGuess, pattern, answerList=answerMatches)
			if prob == 0:
				pass
			else:
				E += prob*I(prob)

		info[possGuess] = E
	return max(info, key=info.get)
	

def solvedBestGuess(dataList):
	
	try:
		if len(dataList) == 0:
			return 'tares'
		elif len(dataList) == 1:
			return firstGuesses[dataList[0]['pattern']]
		elif len(dataList) == 2:
			return secondGuesses[dataList[0]['pattern']][dataList[1]['pattern']]
		elif len(dataList) == 3:
			return thirdGuesses[dataList[0]['pattern']][dataList[1]['pattern']][dataList[2]['pattern']]
		elif len(dataList) == 4:
			return fourthGuesses[dataList[0]['pattern']][dataList[1]['pattern']][dataList[2]['pattern']][dataList[3]['pattern']]
	except KeyError:
		pass

	return bestGuess(dataList)



# data = []

# matches = getMatches(data)

# firstGuesses = {}

# for pattern in possiblePatterns('tares', matches):
# 	print(pattern)
# 	newData = [{'guess': 'tares', 'pattern': pattern}]
# 	nextGuess = bestGuess(newData)
# 	firstGuesses[pattern] = nextGuess


# with open('firstGuess.json', 'w') as j:
# 	json.dump(firstGuesses, j)

# with open('firstGuess.json', 'r') as j:
# 	firstGuesses = json.load(j)

# secondGuesses = {}

# noMatches = getMatches([])

# for firstPattern in possiblePatterns('tares', noMatches):
# 	secondGuess = firstGuesses[firstPattern]
# 	firstData = [{'guess': 'tares', 'pattern': firstPattern}]
# 	firstMatches = getMatches(firstData)
# 	for secondPattern in possiblePatterns(secondGuess, firstMatches):
# 		print(firstPattern, secondPattern)
# 		secondData = [{'guess': 'tares', 'pattern': firstPattern},
# 					  {'guess': secondGuess, 'pattern': secondPattern}]
# 		nextGuess = bestGuess(secondData)
# 		temp = secondGuesses.get(firstPattern, {})
# 		temp[secondPattern] = nextGuess
# 		secondGuesses[firstPattern] = temp

# with open('secondGuess.json', 'w') as j:
# 	json.dump(secondGuesses, j)

# with open('secondGuess.json', 'r') as j:
# 	secondGuesses = json.load(j)


# thirdGuesses = secondGuesses.copy()

# noMatches = getMatches([])

# for firstPattern in possiblePatterns('tares', noMatches):
# 	secondGuess = firstGuesses[firstPattern]
# 	firstData = [{'guess': 'tares', 'pattern': firstPattern}]
# 	firstMatches = getMatches(firstData)
# 	for secondPattern in possiblePatterns(secondGuess, firstMatches):
# 		thirdGuess = secondGuesses[firstPattern][secondPattern]
# 		secondData = [{'guess': 'tares', 'pattern': firstPattern},
# 					  {'guess': secondGuess, 'pattern': secondPattern}]
# 		secondMatches = getMatches(secondData)
# 		for thirdPattern in possiblePatterns(thirdGuess, secondMatches):
# 			print(firstPattern, secondPattern, thirdPattern)
# 			thirdData = [{'guess': 'tares', 'pattern': firstPattern},
# 					  	 {'guess': secondGuess, 'pattern': secondPattern},
# 					  	 {'guess': thirdGuess, 'pattern': thirdPattern}]
# 			nextGuess = bestGuess(thirdData)
# 			if type(thirdGuesses[firstPattern][secondPattern]) is not dict:
# 				thirdGuesses[firstPattern][secondPattern] = {}
# 			thirdGuesses[firstPattern][secondPattern][thirdPattern] = nextGuess

# with open('thirdGuess.json', 'w') as j:
# 	json.dump(thirdGuesses, j)

# with open('thirdGuess.json', 'r') as j:
# 	thirdGuesses = json.load(j)



# fourthGuesses = thirdGuesses.copy()

# noMatches = getMatches([])

# for firstPattern in possiblePatterns('tares', noMatches):
# 	secondGuess = firstGuesses[firstPattern]
# 	firstData = [{'guess': 'tares', 'pattern': firstPattern}]
# 	firstMatches = getMatches(firstData)
# 	for secondPattern in possiblePatterns(secondGuess, firstMatches):
# 		thirdGuess = secondGuesses[firstPattern][secondPattern]
# 		secondData = [{'guess': 'tares', 'pattern': firstPattern},
# 					  {'guess': secondGuess, 'pattern': secondPattern}]
# 		secondMatches = getMatches(secondData)
# 		for thirdPattern in possiblePatterns(thirdGuess, secondMatches):
# 			fourthGuess = thirdGuesses[firstPattern][secondPattern][thirdPattern]
# 			thirdData = [{'guess': 'tares', 'pattern': firstPattern},
# 					  	 {'guess': secondGuess, 'pattern': secondPattern},
# 					  	 {'guess': thirdGuess, 'pattern': thirdPattern}]
# 			thirdMatches = getMatches(thirdData)
# 			for fourthPattern in possiblePatterns(fourthGuess, thirdMatches):
# 				# print(firstPattern, secondPattern, thirdPattern, fourthPattern)
# 				fourthData = [{'guess': 'tares', 'pattern': firstPattern},
# 					  	 {'guess': secondGuess, 'pattern': secondPattern},
# 					  	 {'guess': thirdGuess, 'pattern': thirdPattern},
# 					  	 {'guess': fourthGuess, 'pattern': fourthPattern}]
# 				nextGuess = bestGuess(fourthData)
# 				if fourthPattern != '22222':
# 					print(fourthData)
# 				if type(fourthGuesses[firstPattern][secondPattern][thirdPattern]) is not dict:
# 					fourthGuesses[firstPattern][secondPattern][thirdPattern] = {}
# 				fourthGuesses[firstPattern][secondPattern][thirdPattern][fourthPattern] = nextGuess

# with open('fourthGuess.json', 'w') as j:
# 	json.dump(fourthGuesses, j)




# secondData = [{'guess': 'tares', 'pattern': '01100'},
# 			  {'guess': 'doing', 'pattern': '00000'}]


# matches = getMatches(secondData)
# print(possAnswerList[matches])
# for i in possiblePatterns('acmic', matches):
# 	print(i)