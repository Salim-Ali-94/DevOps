import numpy as np
import utility


if __name__ == "__main__":

	# x = np.array([[0.2],
	# 			  [-0.5],
	# 			  [-0.8]])
	# x = { "1": 0.2,
	# 	  "2": -0.5,
	# 	  "3": -0.8 }

	x = [0.2, -0.5, -0.8]

	structure = { "input_neurons": len(x),
	# structure = { "input_neurons": len(x) + 1,
				  "data": x,
				  "output_neurons": 1,
				  # "output_neurons": 2,
				  # "maximum_layers": 10,
				  "maximum_layers": 2,
				  # "maximum_layers": 0,
				  # "maximum_layers": 1,
				  # "minimum_layers": 1,
				  "minimum_layers": 2,
				  # "minimum_layers": 0,
				  # "maximum_neurons": 10,
				  # "maximum_neurons": 3,
				  # "minimum_neurons": 1 }
				  "maximum_neurons": 3,
				  "minimum_neurons": 3 }

	# topology, network, history = utility.neuralNetwork(structure)
	# topology = utility.networkStructure(structure, 0.5)
	# network, history = utility.neuralNetwork(topology)
	topology = utility.networkStructure(structure, 0.25)
	network, history = utility.neuralNetwork(topology, False, True, 0.25, 0.25, 0, [])
	# ANN = utility.generateNetwork(50, structure)
	# ANN, LUT = utility.generateNetwork(50, structure)
	population_size = 50
	# connection_rate = 0.25
	connection_rate = 0.90
	# connection_rate = 1
	# active_rate = 0.25
	active_rate = 0.75
	# active_rate = 1
	# bias_rate = 0.25
	bias_rate = 0.5
	recurrent_rate = 0
	recurrent = False
	skip = True
	ANN, LUT = utility.generateNetwork(population_size,
									   structure,
									   connection_rate,
									   active_rate,
									   bias_rate,
									   recurrent_rate,
									   recurrent,
									   skip)

	out = utility.propagate(ANN[0]["network"])

	print()
	print("topology /", len(topology))
	print(topology)
	print()
	print("network /", len(network))
	print(network)
	print()
	print("history /", len(history))
	print(history)
	print()
	print("ANN /", len(ANN))
	print(ANN)
	print()
	print("LUT /", len(LUT))
	print(LUT)
	print()

	for ann in network:

		print()
		print("weights /", len(ann))
		# print(ann)
		print("="*100)

		for nn in ann:

			print()
			print("weight /", len(nn))
			print(nn)
			print()
		# 	print()
		# 	print("input_layer")
		# 	print(nn["input_layer"])
		# 	print()
		# 	print("output_layer")
		# 	print(nn["output_layer"])
		# 	print()
		# 	print("input_node")
		# 	print(nn["input_node"])
		# 	print()
		# 	print("output_node")
		# 	print(nn["output_node"])
		# 	print()
		# branches.append({ "fitness": 0,
		# 				  "network": ann })

	print()
	print("out /", len(out))
	print(out)
	print()


	for ann in out:

		print()
		print("weights /", len(ann))
		print(ann)
		print("="*100)

		for nn in ann:

			print()
			print("weight /", len(nn))
			print(nn)
			print()
			print("node")
			print(nn["node"])
			print()
			print("input")
			print(nn["input"])
			print()
			print("output")
			print(nn["output"])
			print()
			print("type")
			print(nn["type"])
			print()
			print("layer")
			print(nn["layer"])
			print()

			for data in nn["data"]:

				print()
				print(f"node ({nn['layer']}):")
				print(nn["node"])
				print()
				print(f"connecting to node ({data['input_layer']}):")
				print(data["input_node"])
				print()
				print(f"state: {'on' if data['active'] else 'off'}")
				print()
				print("branch")
				print(data)
				print()

