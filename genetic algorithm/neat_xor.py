import numpy as np
import utility


if __name__ == "__main__":

	x = np.array([[0.2],
				  [0.5],
				  [-0.8]])

	architecture = [len(x),

					{"nodes": 2,
					 "bias": False,
					 "function": "relu"},

					{"nodes": 4,
					 "bias": True,
					 "function": "tanh"},

					{"nodes": 1,
					 "bias": True,
					 "function": "Sigmoid"}]

	# network, topology = utility.neuralNetwork(architecture)
	network = utility.neuralNetwork(architecture)
	topology = utility.networkStructure(architecture)
	print()
	print("network")
	print(network)
	print()
	print("topology")
	print(topology)
	output = utility.feedForward(x, network, architecture)
	print()
	print("output")
	print(output)
