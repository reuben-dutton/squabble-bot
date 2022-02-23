import json
import math
import re
import random

import numpy as np
import time

with open('words.json', 'r') as j:
	baseWordList = json.load(j)

with open('patterns.json', 'r') as j:
	patternDict = json.load(j)

with open('precompute.json', 'r') as j:
	secondGuess = json.load(j)

with open('precomptier2.json', 'r') as j:
	thirdGuess = json.load(j)


def randomWord():
	return random.choice(baseWordList)


def I(p):
	return -math.log2(p)

# Taken from https://stackoverflow.com/questions/34559663/convert-decimal-to-ternarybase3-in-python
def ternary(n):
    if n == 0:
        return '00000'
    nums = []
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))
    return ''.join(reversed(nums)).zfill(5)

def patterns():
	for i in range(3**5):
		tern = ternary(i)
		yield [int(digit) for digit in tern]

def lfreq(word):
	freq = {}
	for char in word:
		freq[char] = freq.get(char, 0) + 1
	return freq

def getPattern(guess, word):
	pattern = []
	wfreq = lfreq(word)
	gfreq = {}
	for i in range(5):
		gchar = guess[i]
		wchar = word[i]
		currgfreq = gfreq.get(gchar, 0)
		currwfreq = wfreq.get(gchar, 0)
		if gchar == wchar:
			pattern.append(2)
		elif gchar != wchar and currwfreq > 0 and currgfreq < currwfreq:
			pattern.append(1)
		elif currwfreq == 0 or currgfreq == currwfreq:
			pattern.append(0)
		gfreq[gchar] = currgfreq + 1
	return "".join(str(i) for i in pattern)

def getPattern(guess, word):
	return patternDict[guess + word]

def getMatchesSingle(data, wordlist):
	guess = data['guess']
	pattern = data['pattern']
	matches = []
	for word in wordlist:
		wordPattern = getPattern(guess, word)
		if pattern == wordPattern:
			matches.append(word)
	return matches

def getMatches(dataList, wordList=baseWordList):
	matches = baseWordList
	for data in dataList:
		currMatches = matches
		matches = set(currMatches).intersection(set(getMatchesSingle(data, currMatches)))
	return list(matches)

def p(guess, wordList, pattern):
	data = {'guess': guess, 'pattern': pattern}
	matches = set(getMatchesSingle(data, wordList))
	size = len(matches.intersection(set(wordList)))
	return size/len(wordList)


def bestGuess(dataList):
	info = {}

	if len(dataList) == 0:
		return 'raise'
	elif len(dataList) == 1:
		tstr = "".join(str(i) for i in dataList[0]['pattern'])
		newGuess = secondGuess[tstr]
		if newGuess != "":
			return newGuess
		else:
			return randomWord()
	elif len(dataList) == 2:
		tstr1 = "".join(str(i) for i in dataList[0]['pattern'])
		tstr2 = "".join(str(i) for i in dataList[1]['pattern'])
		newGuess = thirdGuess[tstr1 + tstr2]
		if newGuess != "":
			return newGuess
		else:
			return randomWord()

	matches = getMatches(dataList)

	if len(matches) == 1:
		return matches[0]
	elif len(matches) == 0:
		return randomWord()

	for word in baseWordList:
		E = 0
		for pattern in patterns():
			prob = p(word, matches, pattern)
			if prob == 0:
				pass
			else:
				E += prob*I(prob)
		info[word] = E
	return max(info, key=info.get)



# precompute = {}
# for i in range(3**5):
# 	tstr1 = ternary(i)
# 	firstPattern = [int(digit) for digit in tstr1]
# 	newGuess = secondGuess[tstr1]
# 	for j in range(3**5):
# 		startTime = time.time()
# 		tstr2 = ternary(j)
# 		secondPattern = [int(digit) for digit in tstr2]

# 		print('firstPattern: {}'.format(firstPattern))
# 		print('secondPattern: {}'.format(secondPattern))

# 		data = [{'guess': 'raise', 'pattern': firstPattern},
# 				{'guess': newGuess, 'pattern': secondPattern}]
# 		computeGuess = bestGuess(data)
# 		precompute[tstr1 + tstr2] = computeGuess
# 		print(time.time() - startTime)

# with open('precomptier2.json', 'w') as j:
# 	json.dump(precompute, j)