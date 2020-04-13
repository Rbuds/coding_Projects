import json
import re
import csv
import math
import matplotlib.pyplot as plt


threshold = -1.5  # A tuned threshold that determines the entropy that separates DGA from valid domains


def main():  # a method to control the rest of the scripts reading and model development
	trainData = readTrain("Oxford English Dictionary.txt")
	testData = readTest("dga_test.txt")
	model = buildStruc(trainData)
	analyze(model, testData)
	writeJSON(model)


def analyze(model, testData):  # A subroutine to analyze a list of domains for their respective entropy and classify them as valid or DGA
	gramlen = 2
	flags = []
	lengths = []
	measures = []
	for domain in testData:
		oddsSum = 1.0
		wordLen = len(domain)
		for index in range(0, wordLen - gramlen):
			gram = domain[index:index + gramlen]
			next = domain[index + gramlen]
			factor = 0.0001
			if gram in model.keys():
				if next in model[gram]:
					gramDenom = getGramTotal(model, gram)
					gramNum = model[gram][next]
					factor = gramNum / gramDenom
				# print(factor)
			oddsSum *= factor
			round(oddsSum, 6)
		measure = math.log10(oddsSum) / wordLen
		measures.append(measure)
		lengths.append(wordLen)
		flags.append(measure >= -1.5)
		print(str(domain) + " : " + str(flags[-1]))
	plot(lengths, measures, flags, testData)


def plot(xs, ys, assignments, testData):  # plots output to a colored scatter plot
	colors = []
	for flag in assignments:
		if flag:
			colors.append('g')
		else:
			colors.append('r')
	for i in range(0, len(xs)):
		plt.scatter(xs[i], ys[i], color=colors[i])
	plt.ylabel("Entropy Score")
	plt.xlabel("Domain Length")
	plt.title("Detecting DGA Domains")
	plt.show()


def getGramTotal(model, gram):  # A subroutine to calculate the weight of a given gram branch to act as the entropy denominator
	total = 0
	branch = model[gram]
	for key in branch:
		total += branch[key]
	return total


def readTest(file):  # Reads in the test data file for analysis
	data = []
	f = open(file, 'r')
	reader = csv.reader(f)
	for row in reader:
		for word in row:
			word = word.split(".")
			data.append(word[0])
	return data


def readTrain(source):  # Reads in and cleans the training data for developing the Markov chain data model
	cleanedData = list()
	with open(source, 'r', encoding="utf-8") as infile:
		raw = infile.read()
	textsplit = raw.split(" ")
	wordPat = re.compile('^[a-zA-Z]+$')
	for word in textsplit:
		if wordPat.match(word):
			cleanedData.append(str(word.lower()))
	return cleanedData


def buildStruc(cleanedData):  # This method converts cleaned training data into the Markov chain data model
	model = {}
	gramlen = 2
	for word in cleanedData:
		for index in range(0, len(word) - gramlen):
			gram = word[index:index + gramlen]
			next = word[index + gramlen]
			if gram in model.keys():
				if next in model[gram].keys():
					model[gram][next] += 1
				else:
					model[gram][next] = 1
			else:
				model[gram] = {}
				model[gram][next] = 1
	return model


def writeJSON(model):  # This will write the Markov chain data model to a .json for visual inspection or saving
	with open('dictionary_model.json', 'w') as fp:
		json.dump(model, fp, indent=4)


main()
