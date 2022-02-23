import time
import random
import string
import json

from selenium import webdriver

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import entropy


url = "https://squabble.me/"

BASE_WRONG_LETTER_PROB = 0
with open('errorchars.json', 'r') as j:
	errorchars = json.load(j)

# returns a random character which is not the given one
def randomChar(char):
	result = random.choice(errorchars[char])
	return result



def enter(driver):
	d.get(url)
	scrabbleButton = d.find_element(By.XPATH, "//*[text()='Squabble Royale']")
	scrabbleButton.click()
	time.sleep(2)

def findgame(driver):
	findGameButton = d.find_element(By.XPATH, "//*[text()='Find Game']")
	findGameButton.click()
	time.sleep(2)
	findGameButton.click()
	try:
		WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "css-1er3ts7")))
	except:
		driver.back()
		return False
	time.sleep(2.1)
	return True

def readyup(driver):
	body = driver.find_element(By.TAG_NAME, 'body')
	for character in 'ready':
		body.send_keys(character)
		sleeptime = random.random()*0.2
		time.sleep(sleeptime)
	enterKey = driver.find_element(By.CLASS_NAME, 'css-wea04k')
	enterKey.click()


def type(driver, word):
	print(f'typing {word}')
	body = driver.find_element(By.TAG_NAME, 'body')
	char_list = [char for char in word]
	wrong_letters = 0
	wrong_letter_prob = BASE_WRONG_LETTER_PROB
	while len(char_list) > 0:
		if random.random() < wrong_letter_prob and wrong_letters < len(char_list):
			wrong_letter_prob = (5-len(char_list))*0.2
			body.send_keys(randomChar(char_list[0]))
			wrong_letters += 1
		else:
			wrong_letter_prob = BASE_WRONG_LETTER_PROB
			if wrong_letters > 0:
				time.sleep(0.75*random.random()+0.5)
			while wrong_letters > 0:
				body.send_keys(Keys.BACKSPACE)
				wrong_letters -= 1
				time.sleep(random.random()*0.1)
			char = char_list.pop(0)
			body.send_keys(char)
		time.sleep(random.random()*0.05)

	enterKey = None
	while enterKey == None:
		try:
			enterKey = driver.find_element(By.CLASS_NAME, 'css-wea04k')
			enterKey.click()
		except:
			pass
		


def getEntries(driver):
	rows = driver.find_elements(By.CLASS_NAME, 'css-1ng6jrc')
	
	guesses = []
	for row in rows:
		letters = row.find_elements(By.CLASS_NAME, 'letter')
		word = ""
		codes = []
		for letter in letters:
			char = letter.text
			code = 'none'
			iterations = 0
			while code == 'none' and iterations < 1000 and (len(word) != 0 or len(word) != 5):
				try:
					letter.find_element(By.CLASS_NAME, 'css-18037ny')
					code = 0
				except:
					pass
				try:
					letter.find_element(By.CLASS_NAME, 'css-tim17a')
					code = 1
				except:
					pass
				try:
					letter.find_element(By.CLASS_NAME, 'css-g8h5cn')
					code = 2
				except:
					pass
				try:
					letter.find_element(By.CLASS_NAME, 'css-n4oe6o')
					code = 0
				except:
					pass
				iterations += 1
			word += char
			codes.append(code)
		if word != "":
			guesses.append({'guess': word.lower(), 'pattern': "".join([str(code) for code in codes])})
	return guesses


def gameStart(driver):
	try:
		driver.find_element(By.CLASS_NAME, 'css-v05knc')
	except:
		return False
	return True

def gameUpdated(driver):
	try:
		driver.find_element(By.CLASS_NAME, 'css-1b7d4qo')
	except:
		return False
	return True

def initialguesses(driver):
	type(driver, 'tares')



opt = Options()
opt.headless = False

d = webdriver.Firefox(options=opt)

enter(d)

gamefound = findgame(d)

while not gamefound:
	findgame(d)

# readyup(d)

started = False
while not started:
	started = gameStart(d)


while True:

	initialguesses(d)
	
	updated = False
	while not updated:
		updated = gameUpdated(d)

	dataList = getEntries(d)
	print(dataList)
	bestGuess = entropy.solvedBestGuess(dataList)
	type(d, bestGuess)

	while len(dataList) > 0:

		updated = False
		i = 0
		while not updated and i < 100000:
			if i >= 100000:
				print('game over')
				quit()
			updated = gameUpdated(d)

		dataList = getEntries(d)
		print(dataList)
		if len(dataList) == 0 or dataList[-1]['pattern'] == '22222':
			break
		bestGuess = entropy.solvedBestGuess(dataList)
		type(d, bestGuess)

	print('round finished')
