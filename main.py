import time
import random

from selenium import webdriver

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import logic


url = "https://squabble.me/"


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
	body = driver.find_element(By.TAG_NAME, 'body')
	for character in word:
		body.send_keys(character)
		sleeptime = random.random()*0.2
		time.sleep(sleeptime)
	try:
		enterKey = driver.find_element(By.CLASS_NAME, 'css-wea04k')
		enterKey.click()
	except:
		body.send_keys(Keys.BACKSPACE)
		time.sleep(0.1)
		body.send_keys(Keys.BACKSPACE)
		time.sleep(0.1)
		body.send_keys(Keys.BACKSPACE)
		time.sleep(0.1)
		body.send_keys(Keys.BACKSPACE)
		time.sleep(0.1)
		body.send_keys(Keys.BACKSPACE)
		time.sleep(0.2)
		type(d, word)


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
			word += char
			codes.append(code)
		if word != "":
			guesses.append({'guess': word.lower(), 'pattern': codes})
	return guesses


def gameStart(driver):
	try:
		driver.find_element(By.CLASS_NAME, 'css-v05knc')
	except:
		return False
	return True

def initialguesses(driver):
	type(driver, 'raise')
	time.sleep(0.5)
	type(driver, 'dough')
	time.sleep(0.5)
	type(driver, 'testy')
	time.sleep(0.5)
	type(driver, 'buxom')



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

time.sleep(0.5)


while True:

	initialguesses(d)
	dataList = getEntries(d)

	matches = logic.getMatchesMultiple(dataList)
	if len(matches) == 0:
		bestGuess = 'crate'
	else:
		bestGuess = logic.bestGuess(matches)

	type(d, bestGuess)

	time.sleep(0.5)

	dataList = getEntries(d)

	if len(dataList) == 0:
		continue

	matches = logic.getMatchesMultiple(dataList)
	if len(matches) == 0:
		bestGuess = 'crate'
	else:
		bestGuess = logic.bestGuess(matches)

	type(d, bestGuess)

	time.sleep(0.5)

	dataList = getEntries(d)
