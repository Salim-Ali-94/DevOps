import numpy as np


def neuralNetwork(architecture):

	network = []

	for layer in range(len(architecture) - 1):

		flag = architecture[layer + 1]["bias"]
		forward = architecture[layer + 1]["nodes"]

		if (layer == 0):

			current = architecture[layer]

		else:

			current = architecture[layer]["nodes"]

		if flag:

			current += 1

		weights = np.random.rand(forward, current)
		network.append(weights)

	return network
