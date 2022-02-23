import json
import string
import numpy as np



# with open('dictionary.txt', 'r') as f:
# 	lines = f.readlines()

# lines = [line.strip() for line in lines]

# guessList = {i: [word.lower() for word in lines if len(word) == i] for i in range(5, 9)}

# with open('guessableWords.json', 'w') as j:
# 	json.dump(guessList, j)

with open('guessableWords.json', 'r') as j:
	guessList = json.load(j)

with open('possibleWords.json', 'r') as j:
	answerList = json.load(j)


possGuessList = np.array(guessList['5'])
possAnswerList = np.array([answer[0] for answer in answerList['5']])


# newAnswerList = {}

# for i in range(5, 9):
# 	possGuessList = guessList[str(i)]
# 	newAnswerList[str(i)] = [item for item in answerList[str(i)] if item[0] in possGuessList]

# with open('possibleWords.json', 'w') as j:
# 	json.dump(newAnswerList, j)
	




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
		elif currwfreq == 0 or currgfreq >= currwfreq:
			pattern.append(0)
		gfreq[gchar] = currgfreq + 1
	return "".join(str(i) for i in pattern)


# gCode = {}
# for i, word in enumerate(possGuessList):
# 	gCode[word] = i

# with open('guessCodes.json', 'w') as j:
# 	json.dump(gCode, j)

# aCode = {}
# for i, word in enumerate(possAnswerList):
# 	aCode[word] = i

# with open('answerCodes.json', 'w') as j:
# 	json.dump(aCode, j)

# patternArray = np.zeros((possGuessList.size, possAnswerList.size), dtype=np.int16)

# for i, guess in enumerate(possGuessList):
# 	for j, answer in enumerate(possAnswerList):
# 		pattern = getPattern(guess, answer)
# 		num = fromTernary(pattern)
# 		patternArray[i, j] = num

# with open('patternArray.npy', 'wb') as f:
# 	np.save(f, patternArray)

