import random
import json
import time

import entropy

class WordleRound:

	def __init__(self):
		self.word = entropy.randomWord()
		self.guesses = []
		self.info = []

	def makeGuess(self, guess):
		if self.guesses == 6:
			raise Exception('Round has ended.')
		if self.word == guess:
			return True
		self.guesses.append(guess)
		pattern = entropy.toTernary(entropy.getPattern(guess, self.word))
		self.info.append({'guess': guess, 'pattern': pattern})
		return False

	def getInfo(self):
		return self.info


def simulate():
	times = []

	for i in range(1):
		wr = WordleRound()
		wr.word = 'print'
		print(wr.word)
		startTime = time.time()
		for i in range(6):
			info = wr.getInfo()
			bestGuess = entropy.solvedBestGuess(info)
			print(bestGuess)
			result = wr.makeGuess(bestGuess)
			if result:
				print(f'game over! word was: {bestGuess}')
				break
		times.append(time.time()-startTime)

	print(sum(times)/1)

if __name__ == "__main__":
	simulate()