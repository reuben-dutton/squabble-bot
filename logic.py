import json
import math
import re

import numpy as np
import time

with open('words.json', 'r') as j:
	baseWordList = json.load(j)

with open('patterns.json', 'r') as j:
	patternDict = json.load(j)


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
# 		elif currwfreq == 0 or currgfreq == currwfreq:
# 			pattern.append(0)
# 		gfreq[gchar] = currgfreq + 1
# 	return pattern

def getPattern(guess, word):
	return patternDict[guess + word]

def getMatches(data, wordlist):
	guess = data['guess']
	pattern = data['pattern']
	matches = []
	for word in wordlist:
		wordPattern = getPattern(guess, word)
		if pattern == wordPattern:
			matches.append(word)
	return matches

def getMatchesMultiple(dataList, wordList=baseWordList):
	matches = baseWordList
	for data in dataList:
		currMatches = matches
		matches = set(currMatches).intersection(set(getMatches(data, currMatches)))
	print(list(matches))
	return list(matches)

def p(guess, wordList, pattern):
	data = {'guess': guess, 'pattern': pattern}
	matches = set(getMatches(data, wordList))
	size = len(matches.intersection(set(wordList)))
	return size/len(wordList)


def bestGuess(wordList):
	info = {}
	if len(wordList) == 1:
		return wordList[0]
	for word in baseWordList:
		E = 0
		for pattern in patterns():
			prob = p(word, wordList, pattern)
			if prob == 0:
				pass
			else:
				E += prob*I(prob)
		info[word] = E
	return max(info, key=info.get)