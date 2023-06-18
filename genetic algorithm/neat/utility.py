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

def feedForward(data, network, architecture):

	activity = data.copy()

	for layer, neuron in enumerate(network):

		flag = architecture[layer + 1]["bias"]

		if flag:

			activity = np.vstack((activity, 1))

		output = neuron.dot(activity)
		activity = activation(output, architecture[layer + 1]["function"])

	return activity

def activation(data, function = "sigmoid"):

	if (function == "sigmoid"):

		return 1 / (1 + np.exp(-data))

	elif (function == "tanh"):

		return np.tanh(data)

	elif (function == "relu"):

		return np.maximum(data, 0)

	elif (function == "step"):

		return np.sign(data)

	return data
