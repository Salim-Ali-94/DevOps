import random
import uuid
import matplotlib.pyplot as plt
import networkx as nx
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
		self.id = str(uuid.uuid4()).replace("-", "")

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
			self.architecture["minimum_weight"] = self.architecture["maximum_weight"]
			self.architecture["maximum_weight"] = maximum

		if (self.architecture["minimum_layers"] > self.architecture["maximum_layers"]):

			maximum = self.architecture["minimum_layers"]
			self.architecture["minimum_layers"] = self.architecture["maximum_layers"]
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
			width = self._length(layer)

			for index in range(width):

				identity = self._identify(network, nodes, layer, index)

				node = Node(node = identity,
							layer = layer,
							branches = [],
							activity = self.sensor[index] if (layer == 0) else 0,
							output = self.sensor[index] if (layer == 0) else 0,
							function = None if (layer == 0) else random.choice(("relu", "sigmoid", "tanh")))

				if (layer > 0):

					self._attachLinks(network, layer, node)

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

	def _length(self, layer):

		if (layer == 0):

			width = len(self.sensor)

		elif (layer == self.layers - 1):

			width = self.architecture["output_neurons"]

		else:

			width = random.randint(self.architecture["minimum_neurons"],
								   self.architecture["maximum_neurons"])

		return width

	def _identify(self, network, nodes, layer, index):

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

		return identity

	def _attachLinks(self, network, layer, node):

		for level, neurons in enumerate(network):

			for neuron in neurons:

				if (random.random() < self.connection_rate):

					reverse = random.random()

					branch = Branch(weight = random.uniform(self.architecture["minimum_weight"], self.architecture["maximum_weight"]),
									input_node = node.node if (self.recurrent and (reverse < self.recurrent_rate)) else neuron.node,
									output_node = neuron.node if (self.recurrent and (reverse < self.recurrent_rate)) else node.node,
									input_layer = level,
									output_layer = layer,
									active = True if (random.random() < self.active_rate) else False,
									branch_type = "bias" if (neuron.node_type == "bias") else "synapse",
									recurrent = True if (self.recurrent and (reverse < self.recurrent_rate)) else False,
									skip = True if (self.skip and (abs(layer - level) > 1)) else False)

					self._auditLUT(branch)
					node.branches.append(branch)

	def _auditLUT(self, branch):

		if (len(self.history) > 0):

			if (branch.innovation == 0):

				if not any(((link.input_node == branch.input_node) and
							(link.output_node == branch.output_node) and
							(link.skip == branch.skip) and
							(link.branch_type == branch.branch_type) and
							(link.active == branch.active) and
							(link.recurrent == branch.recurrent)) for link in self.history):

					branch.innovation = len(self.history) + 1
					self.history.append(branch)

			else:

				if not any((link.innovation == branch.innovation) for link in self.history):

					self.history.append(branch)

		else:

			branch.innovation = 1
			self.history.append(branch)

		self.history = sorted(self.history, key = lambda dna: dna.innovation)

	def propagate(self):

		output = []

		for layer, nodes in enumerate(self.network[1:]):

			for node in nodes:

				if (node.node_type != "bias"):

					for branch in node.branches:

						neuron = next((vertex for index, vertex in enumerate(self.network[branch.input_layer]) if (vertex.node == branch.input_node)), 0)
						node.activity += neuron.output*branch.weight

					node.output = utility.activation(node.activity, node.function)

					if (layer == self.layers - 2):

						output.append(node.output)

		return output

	def __repr__(self):

		canvas = nx.Graph()
		connections = []
		positions = {}
		styling = {}
		axis = plt.gca()
		maximum = max(abs(branch.weight) for layer in self.network for node in layer for branch in node.branches)
		height = max(len(layer) for layer in self.network)
		info = "\n"
		info += "-"*50
		info += f"\n{self.layers} layers:\n"
		for index, layer in enumerate(self.network): info += f"\nlayer {index} --> {len(layer)} nodes"
		info += "\n"
		info += "-"*50

		for layer, neurons in enumerate(self.network):

			for row, neuron in enumerate(neurons):

				positions[neuron.node] = (layer, (-2*row - abs(len(neurons) - height)) / 2)
				styling[neuron.node] = { "color": "#9cf168" if (neuron.node_type == "bias") else "#ac05f7",
										 "size": 500 if (neuron.node_type == "bias") else 800 }

				if (layer > 0):

					for link in neuron.branches:

						if link.active:

							connections.append((link.input_node, link.output_node))

							lines = { "arrowstyle": "-",
									  "color": "#9cf168" if (link.branch_type == "bias") else "#ac05f7",
									  "connectionstyle": f"arc3,rad={ -0.08 if (link.skip and (positions[link.output_node][1] < -height / 2)) else 0.08 if (link.skip and (positions[link.output_node][1] >= -height / 2)) else 0 }",
									  "linestyle": "--" if link.skip else "-",
									  "alpha": 0.4 if link.skip else 1,
									  "linewidth": 0.5 if ((2*abs(link.weight) / maximum) < 0.5) else 2*abs(link.weight) / maximum,
									  "zorder": 1 }

							axis.annotate("",
										  xy = positions[link.input_node],
										  xytext = positions[link.output_node],
										  arrowprops = lines)

		canvas.add_edges_from(connections)

		nx.draw_networkx_nodes(canvas,
							   positions,
							   nodelist = styling.keys(),
							   node_size = [value["size"] for key, value in styling.items()],
							   node_color = [value["color"] for key, value in styling.items()]).set_zorder(10)

		for key, value in positions.items():

			plt.text(value[0],
					 value[1],
					 s = str(key),
					 horizontalalignment = "center",
					 verticalalignment = "center",
					 zorder = 20,
					 color = "white",
					 family = "Arial",
					 weight = "bold")

		plt.axis("off")
		plt.show()
		return info + "\n"
