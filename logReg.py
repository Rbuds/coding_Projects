import math
import numpy as np


def main():  # a method to control the rest of the scripts reading and model development
	trainData = readTrain("heights.txt")
	xs = list()
	ys = list()
	for point in trainData:
		xs.append(point[0])
		ys.append(point[1])
	average = sum(xs) / len(xs)
	normXs = []
	for height in xs:
		normXs.append(height - average)
	m, b = np.polyfit(normXs, ys, 1)
	logRegPoints = genLogReg(normXs, m, b)
	flags = classify(logRegPoints)
	answers = classify(ys)
	getConfusion(flags, answers)


def classify(logRegPoints):  # uses the logistic regression to predict gender based on the height and returns a boolean list, True for male
	flags = []
	for height in logRegPoints:
		flags.append(height > .5)
	return flags


def genLogReg(xs, m, b):  # develops the logistic regression model and returns a list of threshold points
	points = list()
	for x in xs:
		point = calcRegPoint(x, m, b)
		points.append(point)
	return points


def calcRegPoint(x, m, b):  # accepts a height and and returns the threshold that determines male or female accordingly
	exp = b + m * x
	y = 1 / (1 + math.pow(math.e, -exp))
	return y


def getConfusion(flags, answers):  # This will compare the predicted classes to the correct classes and produce a confusion matrix for use in tuning
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
	print("A-Yes |  " + str(TP) + "   |  " + str(FN))
	print("A-No  |  " + str(FP) + "   |  " + str(TN))
	print("Precision: " + str(round(((TP / (TP + FP)) * 100), 1)) + "%")
	print("Recall: " + str(round(((TP / (TP + FN)) * 100), 1)) + "%")
	print("Accuracy: " + str(round((((TP + TN) / (TP + FN + FP + TN)) * 100), 1)) + "%")


def readTrain(source):  # Reads in and cleans the training data for developing the model
	data = list()
	with open(source, 'r') as inFile:
		for line in inFile:
			line = line.rstrip("\n").split(" ")
			height = int(line[0])
			gender = int(line[1])
			data.append([height, gender])
	return data


main()
