import matplotlib.pyplot as plt
import math


gran = 1  # any integer or float that represents the maximum distance that identifies a connective relationship, try changing this!


def main():
	# test 1: uncomment me to run my test
	xs = [1, 2, 3, 4, 5, 3, 4, 7, 5, 6, 7, 7, 7, 7, 8.5, 7, 6, 5, 4, 3, 5, 4, 3, 2, 1, 1, 1, 1, 1, 2, 3, 4, 5, 8, 8, 9, 9, 9]
	ys = [1, 1, 1, 1, 1, 3, 3, 9, 3, 3, 3, 4, 5, 6, 7.5, 7, 7, 7, 7, 7, 5, 5, 5, 5, 5, 6, 7, 8, 9, 9, 9, 9, 9, 9, 8, 9, 8, 7]
	# test 2: uncomment me to run my test
	# xs = [1, 2, 3, 4, 5, 6, 7, 8, 8, 8, 8, 8, 8, 8, 8, 7, 6, 5, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1, 4, 4, 5, 5, 2.5, 2.5, 2.5, 2.5, 2.5, 3.5, 4.5, 5.5, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 5.5, 4.5, 3.5]
	# ys = [8, 8, 8, 8, 8, 8, 8, 8, 7, 6, 5, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 6, 7, 4, 5, 4, 5, 2.5, 3.5, 4.5, 5.5, 6.5, 6.5, 6.5, 6.5, 6.5, 5.5, 4.5, 3.5, 2.5, 2.5, 2.5, 2.5, 2.5]
	# test 3: uncomment me to run my test
	# xs = [1, 2, 3, 4, 2, 3, 1, 2, 3, 4, 2, 3, 8, 8, 8, 8, 7, 8, 7, 8, 7, 6, 8, 7, 6, 5, 4, 7, 8, 7, 4, 6, 4, 5, 5, 5, 4, 3, 2, 1]
	# ys = [5, 6, 6, 5, 5, 5, 4, 4, 4, 4, 3, 3, 7, 6, 5, 4, 4, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 7, 8, 8, 6, 8, 3, 4, 5, 6, 7, 7, 7, 6]

	neighborhoods = calculateNeighborhoods(xs, ys)  # calculates all neighbors of a given point
	groups = consolidate(neighborhoods)  # consolidates neighborhoods that are shared until no more consolidation can occur
	assignments = []
	for i in range(0, len(xs)):  # assigns a color to each point based on its group
		for group in groups:
			if i in group:
				assignments.append(groups.index(group))
	plot(xs, ys, assignments) # plots points on a GUI and adds colors to identify group affiliations


def consolidate(neighborhoods):  # consolidates neighborhoods until no more changes can occur
	dirty = True
	while dirty:
		oldLen = len(neighborhoods)
		neighborhoods = consolidateOne(neighborhoods)
		if len(neighborhoods) == oldLen:  # did any consolidations occur?
			dirty = False
	return neighborhoods


def consolidateOne(neighborhoods):  # finds one pair of neighborhoods to consolidate and returns revised neighborhoods
	for i in range(0, len(neighborhoods)):
		for j in range(0, len(neighborhoods)):
			if i != j:  # do not consolidate neighborhood with self or remove
				if len(neighborhoods[i].intersection(neighborhoods[j])) > 0:
					neighborhoods[i].update(neighborhoods[j])
					neighborhoods.remove(neighborhoods[j])
					return neighborhoods
	return neighborhoods


def calculateNeighborhoods(xs, ys):  # calculates all neighbors of all points
	neighborhoods = [0] * len(xs)
	for anchor in range(0, len(xs)):
		neighbors = set()
		neighbors.update(findNeighbors(anchor, xs, ys))
		neighborhoods[anchor] = neighbors
	return neighborhoods


def findNeighbors(anchor, xs, ys):  # finds all neighbors of a given x,y point including itself
	neighbors = set()
	for i in range(0, len(xs)):
		if neighbor(xs[anchor], ys[anchor], xs[i], ys[i]):
			neighbors.add(i)
	return neighbors


def neighbor(x1, y1, x2, y2):  # determines if two points are neighbors based on their euclidean distance
	xDist = abs(x2 - x1)
	yDist = abs(y2 - y1)
	xSqr = xDist * xDist
	ySqr = yDist * yDist
	totDist = math.sqrt(xSqr + ySqr)
	return totDist <= gran


def plot(xs, ys, assignments):  # plots output to a colored scatter plot
	colors = ['b', 'g', 'r', 'c', 'm', 'y']
	for i in range(0, len(xs)):
		plt.scatter(xs[i], ys[i], color=colors[assignments[i] % len(colors)])
	plt.show()


main()
