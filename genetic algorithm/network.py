import random
import utility
from node import Node
from branch import Branch


class Network:

	history = []

	def __init__(self, architecture, data, recurrent = False, recurrent_rate = 0, active_rate = 1, connection_rate = 1, skip = True, bias_rate = 0.5):

		self.architecture = architecture
		self.recurrent = recurrent
		self.recurrent_rate = recurrent_rate
		self.active_rate = active_rate
		self.connection_rate = connection_rate
		self.bias_rate = bias_rate
		self.skip = skip
		self.sensor = data
		self.output = 0
		self.fitness = 0
		self.architecture["input_neurons"] = len(data)
		self.layers = self._formatSize()
		self.network = self._neuralNetwork()
		self.output = self.propagate()

	def _formatSize(self):

		if (type(self.architecture["minimum_layers"]) != int):

			self.architecture["minimum_layers"] = int(self.architecture["minimum_layers"])

		if (type(self.architecture["maximum_layers"]) != int):

			self.architecture["maximum_layers"] = int(self.architecture["maximum_layers"])

		if (type(self.architecture["minimum_neurons"]) != int):

			self.architecture["minimum_neurons"] = int(self.architecture["minimum_neurons"])

		if (type(self.architecture["maximum_neurons"]) != int):

			self.architecture["maximum_neurons"] = int(self.architecture["maximum_neurons"])

		if (type(self.architecture["input_neurons"]) != int):

			self.architecture["input_neurons"] = int(self.architecture["input_neurons"])

		if (type(self.architecture["output_neurons"]) != int):

			self.architecture["output_neurons"] = int(self.architecture["output_neurons"])

		if (self.architecture["minimum_layers"] < 0):

			self.architecture["minimum_layers"] = abs(self.architecture["minimum_layers"])

		if (self.architecture["maximum_layers"] < 0):

			self.architecture["maximum_layers"] = abs(self.architecture["maximum_layers"])

		if (self.architecture["minimum_neurons"] < 0):

			self.architecture["minimum_neurons"] = abs(self.architecture["minimum_neurons"])

		if (self.architecture["maximum_neurons"] < 0):

			self.architecture["maximum_neurons"] = abs(self.architecture["maximum_neurons"])

		if (self.architecture["minimum_neurons"] == 0):

			self.architecture["minimum_neurons"] = 1

		if (self.architecture["input_neurons"] == 0):

			self.architecture["input_neurons"] = 1

		if (self.architecture["output_neurons"] == 0):

			self.architecture["output_neurons"] = 1

		if (self.architecture["minimum_weight"] > self.architecture["maximum_weight"]):

			maximum = self.architecture["minimum_weight"]
			self.architecture["minimum_weight"] = strcuture["maximum_weight"]
			self.architecture["maximum_weight"] = maximum

		if (self.architecture["minimum_layers"] > self.architecture["maximum_layers"]):

			maximum = self.architecture["minimum_layers"]
			self.architecture["minimum_layers"] = strcuture["maximum_layers"]
			self.architecture["maximum_layers"] = maximum

		if (self.architecture["maximum_neurons"] < self.architecture["minimum_neurons"]):

			minimum = self.architecture["maximum_neurons"]
			self.architecture["minimum_neurons"] = self.architecture["maximum_neurons"]
			self.architecture["maximum_neurons"] = minimum

		layers = random.randint(self.architecture["minimum_layers"], self.architecture["maximum_layers"]) + 2
		return layers

	def _neuralNetwork(self):

		network = []

		for layer in range(self.layers):

			nodes = tuple()

			if (layer == 0):

				width = len(self.sensor)

			elif (layer == self.layers - 1):

				width = self.architecture["output_neurons"]

			else:

				width = random.randint(self.architecture["minimum_neurons"],
									   self.architecture["maximum_neurons"])

			for index in range(width):

				if (layer > 0):

					if ((index == 0) and (layer == self.layers - 1)):

						identity = network[0][-1].node + 1

					elif ((index == 0) and (layer > 1)):

						identity = network[-1][-1].node + 1

					elif ((index == 0) and (layer == 1)):

						identity = network[-1][-1].node + self.architecture["output_neurons"] + 1

					else:

						identity = nodes[-1].node + 1

				else:

					identity = index + 1

				node = Node(node = identity,
							layer = layer,
							branches = [],
							activity = self.sensor[index] if (layer == 0) else 0,
							output = self.sensor[index] if (layer == 0) else 0,
							function = None if (layer == 0) else random.choice(("relu", "sigmoid", "tanh")))

				if (layer > 0):

					for level, neurons in enumerate(network):

						for row, neuron in enumerate(neurons):
	
							if (random.random() < self.connection_rate):

								reverse = random.random()

								branch = Branch(weight = random.uniform(self.architecture["minimum_weight"], self.architecture["maximum_weight"]),
												input_node = node.node if (self.recurrent and (reverse < self.recurrent_rate)) else neuron.node,
												output_node = neuron.node if (self.recurrent and (reverse < self.recurrent_rate)) else node.node,
												input_layer = level,
												output_layer = layer,
												active = True if (random.random() < self.active_rate) else False,
												branch_type = "bias" if (neuron.node_type == "bias") else "synapse",
												recurrent = True if (self.recurrent and (reverse < self.recurent_rate)) else False,
												skip = True if (self.skip and (abs(layer - level) > 1)) else False)

								self._auditLUT(branch)
								node.branches.append(branch)

				nodes += (node, )

			if ((layer < self.layers - 1) and
				(random.random() < self.bias_rate)):

				node = Node(node = nodes[-1].node + 1,
							layer = layer,
							activity = 1,
							output = 1,
							branches = [],
							node_type = "bias")

				nodes += (node, )

			network.append(nodes)

		return network

	def _auditLUT(self, branch):

		if (len(self.history) > 0):

			if (branch.innovation == 0):

				if not any(((synapse.input_node == branch.input_node) and
							(synapse.output_node == branch.output_node) and
							(synapse.skip == branch.skip) and
							(synapse.branch_type == branch.branch_type) and
							(synapse.active == branch.active) and
							(synapse.recurrent == branch.recurrent)) for synapse in self.history):

					branch.innovation = len(self.history) + 1
					self.history.append(branch)

			else:

				if not any((synapse.innovation == branch.innovation) for synapse in self.history):

					self.history.append(branch)

		else:

			branch.innovation = 1
			self.history.append(branch)

		self.history = sorted(self.history, key = lambda dna: dna.innovation)

	def propagate(self):

		output = []

		for layer, nodes in enumerate(self.network[1:]):

			for row, node in enumerate(nodes):

				if (node.node_type != "bias"):

					for branch in node.branches:

						neuron = next((point for index, point in enumerate(self.network[branch.input_layer]) if (point.node == branch.input_node)), 0)
						node.activity += neuron.output*branch.weight

					node.output = utility.activation(node.activity, node.function)

					if (layer == self.layers - 2):
	
						output.append(node.output)

		return output
