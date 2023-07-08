import numpy as np
import utility


if __name__ == "__main__":

	# x = np.array([[0.2],
	# 			  [-0.5],
	# 			  [-0.8]])
	# x = { "1": 0.2,
	# 	  "2": -0.5,
	# 	  "3": -0.8 }

	x = [0.2, -0.5, 0.8]

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
	
	# out = utility.propagate(ANN[0]["network"])
	X = [({ 'node': 5,
			'input': 0,
			'output': 0,
			'function': 'sigmoid',
			'type': 'neuron',
			'layer': 1,

			'data': [{ 'type': 'synapse',
					   'weight': 0.3,
					   'category': 'neuron',
					   'function': 'sigmoid',
					   'input': 0.8,
					   'output': 0,
					   'activity': 0,
					   'input_layer': 0,
					   'output_layer': 1,
					   'input_node': 3,
					   'output_node': 5,
					   'recurrent': False,
					   'skip': False,
					   'active': True,
					   'innovation': 1 },

					 { 'type': 'synapse',
					   'weight': -2.5,
					   'category': 'neuron',
					   'function': 'sigmoid',
					   'input': -0.5,
					   'output': 0,
					   'activity': 0,
					   'input_layer': 0,
					   'output_layer': 1,
					   'input_node': 2,
					   'output_node': 5,
					   'recurrent': False,
					   'skip': False,
					   'active': False,
					   'innovation': 2 }],

			'activity': 0 },

		  { 'node': 6,
		    'input': 0,
		    'output': 0,
		    'function': 'tanh',
		    'type': 'neuron',
		    'layer': 1,

		    'data': [{ 'type': 'synapse',
						'weight': 0.1,
						'category': 'neuron',
						'function': 'tanh',
						'input': 0.2,
						'output': 0,
						'activity': 0,
						'input_layer': 0,
						'output_layer': 1,
						'input_node': 1,
						'output_node': 6,
						'recurrent': False,
						'skip': False,
						'active': True,
						'innovation': 4 }],

		    'activity': 0 }),

		 ({ 'node': 8,
		    'input': 0,
		    'output': 0,
		    'function': 'sigmoid',
		    'type': 'neuron',
		    'layer': 2,

		    'data': [],

		    'activity': 11 },

		  { 'node': 9,
			'input': 0,
			'output': 0,
			'function': 'tanh',
			'type': 'neuron',
			'layer': 2,

			'data': [{ 'type': 'synapse',
					   'weight': -0.4,
					   'category': 'neuron',
					   'function': 'tanh',
					   'input': 0.8,
					   'output': 0,
					   'activity': 0,
					   'input_layer': 0,
					   'output_layer': 2,
					   'input_node': 3,
					   'output_node': 9,
					   'recurrent': False,
					   'skip': True,
					   'active': True,
					   'innovation': 12 },

					 { 'type': 'bias',
					   'weight': 2,
					   'category': 'neuron',
					   'function': 'tanh',
					   'input': 1,
					   'output': 0,
					   'activity': 0,
					   'input_layer': 1,
					   'output_layer': 2,
					   'input_node': 7,
					   'output_node': 9,
					   'recurrent': False,
					   'skip': False,
					   'active': True,
					   'innovation': 18 }],

			'activity': 0 },

		  { 'node': 11,
		    'input': 0,
		    'output': 0,
		    'function': 'tanh',
		    'type': 'neuron',
		    'layer': 2,

		    'data': [{ 'type': 'synapse',
						'weight': -0.6,
						'category': 'neuron',
						'function': 'tanh',
						'input': 0,
						'output': 0,
						'activity': 0,
						'input_layer': 1,
						'output_layer': 2,
						'input_node': 5,
						'output_node': 11,
						'recurrent': False,
						'skip': False,
						'active': True,
						'innovation': 14 },

		    		 { 'type': 'synapse',
						'weight': -0.8,
						'category': 'neuron',
						'function': 'tanh',
						'input': 0,
						'output': 0,
						'activity': 0,
						'input_layer': 1,
						'output_layer': 2,
						'input_node': 6,
						'output_node': 11,
						'recurrent': False,
						'skip': False,
						'active': True,
						'innovation': 15 },

		    		{ 'type': 'synapse',
						'weight': 3,
						'category': 'neuron',
						'function': 'tanh',
						'input': 0.8,
						'output': 0,
						'activity': 0,
						'input_layer': 0,
						'output_layer': 2,
						'input_node': 3,
						'output_node': 11,
						'recurrent': False,
						'skip': True,
						'active': True,
						'innovation': 16 },

					{ 'type': 'bias',
						'weight': -1.5,
						'category': 'neuron',
						'function': 'tanh',
						'input': 1,
						'output': 0,
						'activity': 0,
						'input_layer': 1,
						'output_layer': 2,
						'input_node': 7,
						'output_node': 11,
						'recurrent': False,
						'skip': False,
						'active': True,
						'innovation': 17 },],

		    'activity': 0 }),



		({ 'node': 4,
			'input': 0,
			'output': 0,
			'function': 'sigmoid',
			'type': 'neuron',
			'layer': 3,

			'data': [{ 'type': 'synapse',
					   'weight': -0.2,
					   'category': 'neuron',
					   'function': 'sigmoid',
					   'input': -0.5,
					   'output': 0,
					   'activity': 0,
					   'input_layer': 0,
					   'output_layer': 3,
					   'input_node': 2,
					   'output_node': 4,
					   'recurrent': False,
					   'skip': True,
					   'active': True,
					   'innovation': 19 },

					 { 'type': 'synapse',
					   'weight': 0.9,
					   'category': 'neuron',
					   'function': 'sigmoid',
					   'input': 0,
					   'output': 0,
					   'activity': 0,
					   'input_layer': 2,
					   'output_layer': 3,
					   'input_node': 9,
					   'output_node': 4,
					   'recurrent': False,
					   'skip': False,
					   'active': True,
					   'innovation': 20 },

					 { 'type': 'synapse',
					   'weight': 1.5,
					   'category': 'neuron',
					   'function': 'sigmoid',
					   'input': 0,
					   'output': 0,
					   'activity': 0,
					   'input_layer': 2,
					   'output_layer': 3,
					   'input_node': 10,
					   'output_node': 4,
					   'recurrent': False,
					   'skip': False,
					   'active': True,
					   'innovation': 21 },

					 { 'type': 'synapse',
					   'weight': 0.7,
					   # 'weight': -1,
					   'category': 'neuron',
					   'function': 'sigmoid',
					   'input': 0,
					   'output': 0,
					   'activity': 0,
					   'input_layer': 1,
					   'output_layer': 3,
					   'input_node': 6,
					   'output_node': 4,
					   'recurrent': False,
					   'skip': True,
					   'active': True,
					   'innovation': 22 },

					 { 'type': 'synapse',
					   'weight': 0.5,
					   'category': 'neuron',
					   'function': 'sigmoid',
					   'input': 0.8,
					   'output': 0,
					   'activity': 0,
					   'input_layer': 0,
					   'output_layer': 3,
					   'input_node': 3,
					   'output_node': 4,
					   'recurrent': False,
					   'skip': True,
					   'active': True,
					   'innovation': 23 },

					 { 'type': 'bias',
					   'weight': -2,
					   'category': 'neuron',
					   'function': 'sigmoid',
					   'input': 1,
					   'output': 0,
					   'activity': 0,
					   'input_layer': 2,
					   'output_layer': 3,
					   'input_node': 12,
					   'output_node': 4,
					   'recurrent': False,
					   'skip': False,
					   'active': True,
					   'innovation': 24 }],

			'activity': 0 },)]

	# out = utility.propagate(ANN[0]["network"])
	out = utility.propagate(X)

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





# weight / 8
# {'node': 5, 'input': 0.24, 'output': 0.5597136492671929, 'function': 'sigmoid', 'type': 'neuron', 'layer': 1, 'data': [{'type': 'synapse', 'weight': 0.3, 'category': 'neuron', 'function': 'sigmoid', 'input': 0.8, 'output': 0, 'activity': 0, 'input_layer': 0, 'output_layer': 1, 'input_node': 3, 'output_node': 5, 'recurrent': False, 'skip': False, 'active': True, 'innovation': 1}, {'type': 'synapse', 'weight': -2.5, 'category': 'neuron', 'function': 'sigmoid', 'input': -0.5, 'output': 0, 'activity': 0, 'input_layer': 0, 'output_layer': 1, 'input_node': 2, 'output_node': 5, 'recurrent': False, 'skip': False, 'active': False, 'innovation': 2}], 'activity': 0.5597136492671929}

# node
# 5

# input
# 0.24

# output
# 0.5597136492671929

# type
# neuron

# layer
# 1


# node (1):
# 5

# connecting to node (0):
# 3

# state: on

# branch
# {'type': 'synapse', 'weight': 0.3, 'category': 'neuron', 'function': 'sigmoid', 'input': 0.8, 'output': 0, 'activity': 0, 'input_layer': 0, 'output_layer': 1, 'input_node': 3, 'output_node': 5, 'recurrent': False, 'skip': False, 'active': True, 'innovation': 1}


# node (1):
# 5

# connecting to node (0):
# 2

# state: off

# branch
# {'type': 'synapse', 'weight': -2.5, 'category': 'neuron', 'function': 'sigmoid', 'input': -0.5, 'output': 0, 'activity': 0, 'input_layer': 0, 'output_layer': 1, 'input_node': 2, 'output_node': 5, 'recurrent': False, 'skip': False, 'active': False, 'innovation': 2}


# weight / 8
# {'node': 6, 'input': 0.020000000000000004, 'output': 0.019997333759930933, 'function': 'tanh', 'type': 'neuron', 'layer': 1, 'data': [{'type': 'synapse', 'weight': 0.1, 'category': 'neuron', 'function': 'tanh', 'input': 0.2, 'output': 0, 'activity': 0, 'input_layer': 0, 'output_layer': 1, 'input_node': 1, 'output_node': 6, 'recurrent': False, 'skip': False, 'active': True, 'innovation': 4}], 'activity': 0.019997333759930933}

# node
# 6

# input
# 0.020000000000000004

# output
# 0.019997333759930933

# type
# neuron

# layer
# 1


# node (1):
# 6

# connecting to node (0):
# 1

# state: on

# branch
# {'type': 'synapse', 'weight': 0.1, 'category': 'neuron', 'function': 'tanh', 'input': 0.2, 'output': 0, 'activity': 0, 'input_layer': 0, 'output_layer': 1, 'input_node': 1, 'output_node': 6, 'recurrent': False, 'skip': False, 'active': True, 'innovation': 4}


# weights / 3
# ({'node': 8, 'input': 0, 'output': 0, 'function': 'sigmoid', 'type': 'neuron', 'layer': 2, 'data': [], 'activity': 11}, {'node': 9, 'input': 1.68, 'output': 0.932861553437035, 'function': 'tanh', 'type': 'neuron', 'layer': 2, 'data': [{'type': 'synapse', 'weight': -0.4, 'category': 'neuron', 'function': 'tanh', 'input': 0.8, 'output': 0, 'activity': 0, 'input_layer': 0, 'output_layer': 2, 'input_node': 3, 'output_node': 9, 'recurrent': False, 'skip': True, 'active': True, 'innovation': 12}, {'type': 'bias', 'weight': 2, 'category': 'neuron', 'function': 'tanh', 'input': 1, 'output': 0, 'activity': 0, 'input_layer': 1, 'output_layer': 2, 'input_node': 7, 'output_node': 9, 'recurrent': False, 'skip': False, 'active': True, 'innovation': 18}], 'activity': 0.932861553437035}, {'node': 11, 'input': 0.5481739434317401, 'output': 0.4991503687096486, 'function': 'tanh', 'type': 'neuron', 'layer': 2, 'data': [{'type': 'synapse', 'weight': -0.6, 'category': 'neuron', 'function': 'tanh', 'input': 0, 'output': 0, 'activity': 0, 'input_layer': 1, 'output_layer': 2, 'input_node': 5, 'output_node': 11, 'recurrent': False, 'skip': False, 'active': True, 'innovation': 14}, {'type': 'synapse', 'weight': -0.8, 'category': 'neuron', 'function': 'tanh', 'input': 0, 'output': 0, 'activity': 0, 'input_layer': 1, 'output_layer': 2, 'input_node': 6, 'output_node': 11, 'recurrent': False, 'skip': False, 'active': True, 'innovation': 15}, {'type': 'synapse', 'weight': 3, 'category': 'neuron', 'function': 'tanh', 'input': 0.8, 'output': 0, 'activity': 0, 'input_layer': 0, 'output_layer': 2, 'input_node': 3, 'output_node': 11, 'recurrent': False, 'skip': True, 'active': True, 'innovation': 16}, {'type': 'bias', 'weight': -1.5, 'category': 'neuron', 'function': 'tanh', 'input': 1, 'output': 0, 'activity': 0, 'input_layer': 1, 'output_layer': 2, 'input_node': 7, 'output_node': 11, 'recurrent': False, 'skip': False, 'active': True, 'innovation': 17}], 'activity': 0.4991503687096486})
# ====================================================================================================

# weight / 8
# {'node': 8, 'input': 0, 'output': 0, 'function': 'sigmoid', 'type': 'neuron', 'layer': 2, 'data': [], 'activity': 11}

# node
# 8

# input
# 0

# output
# 0

# type
# neuron

# layer
# 2


# weight / 8
# {'node': 9, 'input': 1.68, 'output': 0.932861553437035, 'function': 'tanh', 'type': 'neuron', 'layer': 2, 'data': [{'type': 'synapse', 'weight': -0.4, 'category': 'neuron', 'function': 'tanh', 'input': 0.8, 'output': 0, 'activity': 0, 'input_layer': 0, 'output_layer': 2, 'input_node': 3, 'output_node': 9, 'recurrent': False, 'skip': True, 'active': True, 'innovation': 12}, {'type': 'bias', 'weight': 2, 'category': 'neuron', 'function': 'tanh', 'input': 1, 'output': 0, 'activity': 0, 'input_layer': 1, 'output_layer': 2, 'input_node': 7, 'output_node': 9, 'recurrent': False, 'skip': False, 'active': True, 'innovation': 18}], 'activity': 0.932861553437035}

# node
# 9

# input
# 1.68

# output
# 0.932861553437035

# type
# neuron

# layer
# 2


# node (2):
# 9

# connecting to node (0):
# 3

# state: on

# branch
# {'type': 'synapse', 'weight': -0.4, 'category': 'neuron', 'function': 'tanh', 'input': 0.8, 'output': 0, 'activity': 0, 'input_layer': 0, 'output_layer': 2, 'input_node': 3, 'output_node': 9, 'recurrent': False, 'skip': True, 'active': True, 'innovation': 12}


# node (2):
# 9

# connecting to node (1):
# 7

# state: on

# branch
# {'type': 'bias', 'weight': 2, 'category': 'neuron', 'function': 'tanh', 'input': 1, 'output': 0, 'activity': 0, 'input_layer': 1, 'output_layer': 2, 'input_node': 7, 'output_node': 9, 'recurrent': False, 'skip': False, 'active': True, 'innovation': 18}


# weight / 8
# {'node': 11, 'input': 0.5481739434317401, 'output': 0.4991503687096486, 'function': 'tanh', 'type': 'neuron', 'layer': 2, 'data': [{'type': 'synapse', 'weight': -0.6, 'category': 'neuron', 'function': 'tanh', 'input': 0, 'output': 0, 'activity': 0, 'input_layer': 1, 'output_layer': 2, 'input_node': 5, 'output_node': 11, 'recurrent': False, 'skip': False, 'active': True, 'innovation': 14}, {'type': 'synapse', 'weight': -0.8, 'category': 'neuron', 'function': 'tanh', 'input': 0, 'output': 0, 'activity': 0, 'input_layer': 1, 'output_layer': 2, 'input_node': 6, 'output_node': 11, 'recurrent': False, 'skip': False, 'active': True, 'innovation': 15}, {'type': 'synapse', 'weight': 3, 'category': 'neuron', 'function': 'tanh', 'input': 0.8, 'output': 0, 'activity': 0, 'input_layer': 0, 'output_layer': 2, 'input_node': 3, 'output_node': 11, 'recurrent': False, 'skip': True, 'active': True, 'innovation': 16}, {'type': 'bias', 'weight': -1.5, 'category': 'neuron', 'function': 'tanh', 'input': 1, 'output': 0, 'activity': 0, 'input_layer': 1, 'output_layer': 2, 'input_node': 7, 'output_node': 11, 'recurrent': False, 'skip': False, 'active': True, 'innovation': 17}], 'activity': 0.4991503687096486}

# node
# 11

# input
# 0.5481739434317401

# output
# 0.4991503687096486

# type
# neuron

# layer
# 2


# node (2):
# 11

# connecting to node (1):
# 5

# state: on

# branch
# {'type': 'synapse', 'weight': -0.6, 'category': 'neuron', 'function': 'tanh', 'input': 0, 'output': 0, 'activity': 0, 'input_layer': 1, 'output_layer': 2, 'input_node': 5, 'output_node': 11, 'recurrent': False, 'skip': False, 'active': True, 'innovation': 14}


# node (2):
# 11

# connecting to node (1):
# 6

# state: on

# branch
# {'type': 'synapse', 'weight': -0.8, 'category': 'neuron', 'function': 'tanh', 'input': 0, 'output': 0, 'activity': 0, 'input_layer': 1, 'output_layer': 2, 'input_node': 6, 'output_node': 11, 'recurrent': False, 'skip': False, 'active': True, 'innovation': 15}


# node (2):
# 11

# connecting to node (0):
# 3

# state: on

# branch
# {'type': 'synapse', 'weight': 3, 'category': 'neuron', 'function': 'tanh', 'input': 0.8, 'output': 0, 'activity': 0, 'input_layer': 0, 'output_layer': 2, 'input_node': 3, 'output_node': 11, 'recurrent': False, 'skip': True, 'active': True, 'innovation': 16}


# node (2):
# 11

# connecting to node (1):
# 7

# state: on

# branch
# {'type': 'bias', 'weight': -1.5, 'category': 'neuron', 'function': 'tanh', 'input': 1, 'output': 0, 'activity': 0, 'input_layer': 1, 'output_layer': 2, 'input_node': 7, 'output_node': 11, 'recurrent': False, 'skip': False, 'active': True, 'innovation': 17}


# weights / 1
# ({'node': 4, 'input': -0.6464264682747167, 'output': 0.343795275761663, 'function': 'sigmoid', 'type': 'neuron', 'layer': 3, 'data': [{'type': 'synapse', 'weight': -0.2, 'category': 'neuron', 'function': 'sigmoid', 'input': -0.5, 'output': 0, 'activity': 0, 'input_layer': 0, 'output_layer': 3, 'input_node': 2, 'output_node': 4, 'recurrent': False, 'skip': True, 'active': True, 'innovation': 19}, {'type': 'synapse', 'weight': 0.9, 'category': 'neuron', 'function': 'sigmoid', 'input': 0, 'output': 0, 'activity': 0, 'input_layer': 2, 'output_layer': 3, 'input_node': 9, 'output_node': 4, 'recurrent': False, 'skip': False, 'active': True, 'innovation': 20}, {'type': 'synapse', 'weight': 1.5, 'category': 'neuron', 'function': 'sigmoid', 'input': 0, 'output': 0, 'activity': 0, 'input_layer': 2, 'output_layer': 3, 'input_node': 10, 'output_node': 4, 'recurrent': False, 'skip': False, 'active': True, 'innovation': 21}, {'type': 'synapse', 'weight': 0.7, 'category': 'neuron', 'function': 'sigmoid', 'input': 0, 'output': 0, 'activity': 0, 'input_layer': 1, 'output_layer': 3, 'input_node': 6, 'output_node': 4, 'recurrent': False, 'skip': True, 'active': True, 'innovation': 22}, {'type': 'synapse', 'weight': 0.5, 'category': 'neuron', 'function': 'sigmoid', 'input': 0.8, 'output': 0, 'activity': 0, 'input_layer': 0, 'output_layer': 3, 'input_node': 3, 'output_node': 4, 'recurrent': False, 'skip': True, 'active': True, 'innovation': 23}, {'type': 'bias', 'weight': -2, 'category': 'neuron', 'function': 'sigmoid', 'input': 1, 'output': 0, 'activity': 0, 'input_layer': 2, 'output_layer': 3, 'input_node': 12, 'output_node': 4, 'recurrent': False, 'skip': False, 'active': True, 'innovation': 24}], 'activity': 0.343795275761663},)
# ====================================================================================================

# weight / 8
# {'node': 4, 'input': -0.6464264682747167, 'output': 0.343795275761663, 'function': 'sigmoid', 'type': 'neuron', 'layer': 3, 'data': [{'type': 'synapse', 'weight': -0.2, 'category': 'neuron', 'function': 'sigmoid', 'input': -0.5, 'output': 0, 'activity': 0, 'input_layer': 0, 'output_layer': 3, 'input_node': 2, 'output_node': 4, 'recurrent': False, 'skip': True, 'active': True, 'innovation': 19}, {'type': 'synapse', 'weight': 0.9, 'category': 'neuron', 'function': 'sigmoid', 'input': 0, 'output': 0, 'activity': 0, 'input_layer': 2, 'output_layer': 3, 'input_node': 9, 'output_node': 4, 'recurrent': False, 'skip': False, 'active': True, 'innovation': 20}, {'type': 'synapse', 'weight': 1.5, 'category': 'neuron', 'function': 'sigmoid', 'input': 0, 'output': 0, 'activity': 0, 'input_layer': 2, 'output_layer': 3, 'input_node': 10, 'output_node': 4, 'recurrent': False, 'skip': False, 'active': True, 'innovation': 21}, {'type': 'synapse', 'weight': 0.7, 'category': 'neuron', 'function': 'sigmoid', 'input': 0, 'output': 0, 'activity': 0, 'input_layer': 1, 'output_layer': 3, 'input_node': 6, 'output_node': 4, 'recurrent': False, 'skip': True, 'active': True, 'innovation': 22}, {'type': 'synapse', 'weight': 0.5, 'category': 'neuron', 'function': 'sigmoid', 'input': 0.8, 'output': 0, 'activity': 0, 'input_layer': 0, 'output_layer': 3, 'input_node': 3, 'output_node': 4, 'recurrent': False, 'skip': True, 'active': True, 'innovation': 23}, {'type': 'bias', 'weight': -2, 'category': 'neuron', 'function': 'sigmoid', 'input': 1, 'output': 0, 'activity': 0, 'input_layer': 2, 'output_layer': 3, 'input_node': 12, 'output_node': 4, 'recurrent': False, 'skip': False, 'active': True, 'innovation': 24}], 'activity': 0.343795275761663}

# node
# 4

# input
# -0.6464264682747167

# output
# 0.343795275761663

# type
# neuron

# layer
# 3


# node (3):
# 4

# connecting to node (0):
# 2

# state: on

# branch
# {'type': 'synapse', 'weight': -0.2, 'category': 'neuron', 'function': 'sigmoid', 'input': -0.5, 'output': 0, 'activity': 0, 'input_layer': 0, 'output_layer': 3, 'input_node': 2, 'output_node': 4, 'recurrent': False, 'skip': True, 'active': True, 'innovation': 19}


# node (3):
# 4

# connecting to node (2):
# 9

# state: on

# branch
# {'type': 'synapse', 'weight': 0.9, 'category': 'neuron', 'function': 'sigmoid', 'input': 0, 'output': 0, 'activity': 0, 'input_layer': 2, 'output_layer': 3, 'input_node': 9, 'output_node': 4, 'recurrent': False, 'skip': False, 'active': True, 'innovation': 20}


# node (3):
# 4

# connecting to node (2):
# 10

# state: on

# branch
# {'type': 'synapse', 'weight': 1.5, 'category': 'neuron', 'function': 'sigmoid', 'input': 0, 'output': 0, 'activity': 0, 'input_layer': 2, 'output_layer': 3, 'input_node': 10, 'output_node': 4, 'recurrent': False, 'skip': False, 'active': True, 'innovation': 21}


# node (3):
# 4

# connecting to node (1):
# 6

# state: on

# branch
# {'type': 'synapse', 'weight': 0.7, 'category': 'neuron', 'function': 'sigmoid', 'input': 0, 'output': 0, 'activity': 0, 'input_layer': 1, 'output_layer': 3, 'input_node': 6, 'output_node': 4, 'recurrent': False, 'skip': True, 'active': True, 'innovation': 22}


# node (3):
# 4

# connecting to node (0):
# 3

# state: on

# branch
# {'type': 'synapse', 'weight': 0.5, 'category': 'neuron', 'function': 'sigmoid', 'input': 0.8, 'output': 0, 'activity': 0, 'input_layer': 0, 'output_layer': 3, 'input_node': 3, 'output_node': 4, 'recurrent': False, 'skip': True, 'active': True, 'innovation': 23}


# node (3):
# 4

# connecting to node (2):
# 12

# state: on

# branch
# {'type': 'bias', 'weight': -2, 'category': 'neuron', 'function': 'sigmoid', 'input': 1, 'output': 0, 'activity': 0, 'input_layer': 2, 'output_layer': 3, 'input_node': 12, 'output_node': 4, 'recurrent': False, 'skip': False, 'active': True, 'innovation': 24}