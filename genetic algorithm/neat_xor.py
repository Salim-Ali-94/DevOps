import numpy as np
import utility


if __name__ == "__main__":

	x = np.array([[0.2],
				  [0.5],
				  [-0.8]])

	architecture = [{"nodes": len(x),
					 "layer": 0,
					 # "state": 1,
					 # "bias": False,
					 "bias": None,
					 "function": ""},

					{"nodes": 2,
					 "layer": 1,
					 # "state": 1,
					 "bias": False,
					 "function": "relu"},

					{"nodes": 4,
					 "layer": 2,
					 # "state": 1,
					 "bias": True,
					 "function": "tanh"},

					{"nodes": 1,
					 "layer": 3,
					 # "state": 1,
					 "bias": True,
					 "function": "Sigmoid"}]

	attatchType = lambda w, previous = 0: w + previous
	attatchState = lambda w, state = 1: w*state
	# modify network
	# forward / recurrent --> infer from layer of each node ==> if (layer_to > layer_from): type = forward else recurrent
	# consecutive / cascade --> determine from layer of each node ==> if (layer_to - layer_from == 1): type = consecutive else cascade

	# network, topology = utility.neuralNetwork(architecture)
	network = utility.neuralNetwork(architecture)
	topology = utility.networkStructure(architecture)
	output = utility.feedForward(x, network, architecture)
	nodes = []

	for layer in topology:

		nodes += [node for node in layer]

	print()
	print("network")
	print(network)
	print()
	print("topology")
	print(topology)
	print()
	print("nodes")
	print(nodes)
	print()
	print("output")
	print(output)

	# for matrix in network:

	# 	for row in matrix:

	# 		for cell in row:

	# 			print(cell)

	# for matrix in network:
	for weight in range(len(network)):

		# print(matrix.shape)
		print(network[weight].shape)

		# for row in range(matrix.shape[0]):
		for row in range(network[weight].shape[0]):

			# for column in range(len(matrix[row])):
			for column in range(len(network[weight][row])):

				print()
				print("row", "\tcolumn")
				print()
				print(row + 1, f"\t{column + 1}")
				print()
				print("weight:")
				print()
				current = topology[weight + 1][row]
				previous = topology[weight][column]
				# print(f"w_{row + 1}{column + 1} = {network[weight][row][column]}")
				# print(f"w_{row + 1}{column + 1}/({weight}{weight + 1}) = {network[weight][row][column]}")
				# print(f"w_{topology[weight + 1][row]}{topology[weight][column]}/({weight}{weight + 1}) = {network[weight][row][column]}")
				print(f"w_{current}{previous}/({weight}{weight + 1}) = {network[weight][row][column]}")
				# print(matrix[row][column])
				# print(network[weight][row][column])
				print()
				print("corresponding nodes / layers")
				print()
				# print(topology[weight][row], topology[weight + 1][column])
				print("from:")
				# print(topology[weight][row])
				print(previous)
				# print(topology[weight][column])
				print()
				print("to:")
				# print(topology[weight + 1][row])
				# print(topology[weight + 1][column])
				# print(topology[weight + 1][row])
				print(current)
				print()
				print("node / branch relationship:")
				print()
				# print(f"N{column + 1} (L{weight}) --> N{row + 1} (L{weight + 1})")
				# print(f"N{topology[weight][row]} (L{weight}) --> N{topology[weight + 1][column]} (L{weight + 1})")
				# print(f"N{topology[weight][row]} (L{weight}) --> N{topology[weight + 1][row]} (L{weight + 1})")
				print(f"N{previous} (L{weight}) --> N{current} (L{weight + 1})")
				print("-"*100)
				print()



	# print()
	# print("network")
	# print(network)
	# print()
	# print("topology")
	# print(topology)
	# print()
	# print("nodes")
	# print(nodes)
	# print()
	# print("output")
	# print(output)
