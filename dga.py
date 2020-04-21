import json
import re
import csv
import math
import matplotlib.pyplot as plt
import numpy as np


threshold = -0.25


def main():  # a method to control the rest of the scripts reading and model development
	trainData = readTrain("Oxford English Dictionary.txt")
	testData = readTest("dga_test.txt")
	domains = []
	answers = []
	ys = []
	for row in testData:
		domains.append(row.split(".")[0])
		if row.split(" ")[1] == '1':
			ys.append(1)
			answers.append(True)
		else:
			ys.append(0)
			answers.append(False)
	model = buildStruc(trainData)
	analyze(model, domains, answers, ys)


def analyze(model, domains, answers, ys):  # A subroutine to analyze a list of domains for their respective entropy and classify them as valid or DGA
	gramlen = 2
	flags = []
	lengths = []
	measures = []
	for domain in domains:
		oddsProduct = 1.0
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
			oddsProduct *= factor
			round(oddsProduct, 6)
		measure = math.log10(oddsProduct) / wordLen
		measures.append(measure)
		lengths.append(wordLen)
	m, b = np.polyfit(lengths, measures, 1)
	adjMeasures = []
	for i in range(0, len(measures)):
		adj = measures[i]
		adj -= b
		adj -= lengths[i] * m
		adjMeasures.append(adj)
	for entropy in adjMeasures:
		flags.append(entropy < threshold)
	getConfusion(flags, answers)
	plot(lengths, adjMeasures, answers)


def getConfusion(flags, answers):  # This will compare the predicted classes to the correct classes and produce a confusion matrix for use in tuning
	print(flags)
	print(answers)
	matrix = [0, 0, 0, 0]
	for i in range(0, len(flags)):
		guess = flags[i]
		answer = answers[i]
		if guess:
			if answer:
				matrix[0] = matrix[0] + 1
			else:
				matrix[2] = matrix[2] + 1
		else:
			if answer:
				matrix[1] = matrix[1] + 1
			else:
				matrix[3] = matrix[3] + 1
	TP = matrix[0]
	FN = matrix[1]
	FP = matrix[2]
	TN = matrix[3]
	print("      | P-Yes | P-No")
	print("A-Yes |  " + str(TP) + "    |  " + str(FN))
	print("A-No  |  " + str(FP) + "    |  " + str(TN))
	print("Precision: " + str(round(((TP / (TP + FP)) * 100), 1)) + "%")
	print("Recall: " + str(round(((TP / (TP + FN)) * 100), 1)) + "%")
	print("Accuracy: " + str(round((((TP + TN) / (TP + FN + FP + TN)) * 100), 1)) + "%")


def plot(xs, ys, assignments):  # plots output to a colored scatter plot
	colors = []
	for flag in assignments:
		if flag:
			colors.append('r')
		else:
			colors.append('g')
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
			data.append(word)
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
