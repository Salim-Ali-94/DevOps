import random
import uuid
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from .node import Node
from .branch import Branch


class Network:

	history = []

	def __init__(self, architecture, recurrent = False, recurrent_rate = 0, active_rate = 1, connection_rate = 1, skip = True, skip_rate = 1, bias_rate = 0.5, generate = True):

		self.architecture = architecture
		self.output = [0]*self.architecture["output_neurons"]
		self.id = str(uuid.uuid4()).replace("-", "")
		self.fitness = 0
		self.species = 0
		self.network = []
		self.genome = []
		self.neurons = []
		self.modified_fitness = 0
		self.layers = 0

		if generate:

			self.recurrent_rate = recurrent_rate
			self.skip_rate = skip_rate
			self.active_rate = active_rate
			self.connection_rate = connection_rate
			self.bias_rate = bias_rate
			self.recurrent = recurrent
			self.skip = skip
			self.layers = self._formatSize()
			self._neuralNetwork()

	def _formatSize(self):

		self.architecture["output_function"] = self.architecture["output_function"].lower().lstrip().rstrip()

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

		if (self.architecture["output_function"] not in ("sigmoid", "relu", "tanh", "step", "switch")):

			self.architecture["output_function"] = random.choice(("sigmoid", "relu", "tanh"))

		layers = random.randint(self.architecture["minimum_layers"], self.architecture["maximum_layers"]) + 2
		return layers

	def _neuralNetwork(self):

		for layer in range(self.layers):

			nodes = tuple()
			width = self._length(layer)

			for index in range(width):

				identity = self._identify(nodes, layer, index)

				node = Node(node = identity,
							layer = layer,
							branches = [],
							activity = 0,
							output = 0,
							function = None if (layer == 0) else self.architecture["output_function"] if (layer == self.layers - 1) else random.choice(("relu", "sigmoid", "tanh")))

				if (layer > 0):

					self._attachNodes(layer, node)

				nodes += (node, )
				self.neurons.append(node)

			if ((layer < self.layers - 1) and
				(random.random() < self.bias_rate)):

				node = Node(node = nodes[-1].node + 1 if (layer > 0) else self.architecture["input_neurons"] + self.architecture["output_neurons"] + 1,
							layer = layer,
							activity = 1,
							output = 1,
							branches = [],
							node_type = "bias")

				nodes += (node, )
				self.neurons.append(node)

			self.network.append(nodes)

		self.neurons = sorted(self.neurons, key = lambda dna: dna.node)

	def _length(self, layer):

		if (layer == 0):

			width = self.architecture["input_neurons"]

		elif (layer == self.layers - 1):

			width = self.architecture["output_neurons"]

		else:

			width = random.randint(self.architecture["minimum_neurons"],
								   self.architecture["maximum_neurons"])

		return width

	def _identify(self, nodes, layer, index):

		if (layer > 0):

			if ((index == 0) and (layer == self.layers - 1)):

				identity = self.architecture["input_neurons"] + 1

			elif ((index == 0) and (layer > 1)):

				identity = self.network[-1][-1].node + 1

			elif ((index == 0) and (layer == 1)):

				identity = self.network[-1][-1].node + self.architecture["output_neurons"] + 1

			else:

				identity = nodes[-1].node + 1

		else:

			identity = index + 1

		return identity

	def _attachNodes(self, layer, node):

		for level, neurons in enumerate(self.network):

			if ((self.skip and (abs(layer - level) > 1)) or
				(abs(layer - level) == 1)):

				for neuron in neurons:

					if ((random.random() < self.connection_rate) and
						((self.skip and (abs(layer - level) > 1) and
						(random.random() < self.skip_rate)) or
						(abs(layer - level) == 1))):

						reverse = random.random()

						branch = Branch(weight = random.uniform(self.architecture["minimum_weight"], self.architecture["maximum_weight"]),
										input_node = node.node if (self.recurrent and (reverse < self.recurrent_rate)) else neuron.node,
										output_node = neuron.node if (self.recurrent and (reverse < self.recurrent_rate)) else node.node,
										input_neuron = node if (self.recurrent and (reverse < self.recurrent_rate)) else neuron,
										output_neuron = neuron if (self.recurrent and (reverse < self.recurrent_rate)) else node,
										input_layer = level,
										output_layer = layer,
										active = True if (random.random() < self.active_rate) else False,
										branch_type = "bias" if (neuron.node_type == "bias") else "synapse",
										recurrent = True if (self.recurrent and (reverse < self.recurrent_rate)) else False,
										skip = True if (self.skip and (abs(layer - level) > 1)) else False)

						self.auditLUT(branch)
						node.branches.append(branch)
						self.genome.append(branch)

		self.genome = sorted(self.genome, key = lambda dna: dna.innovation)

	def _activation(self, data, function = "sigmoid"):

		if (function.lower().lstrip().rstrip() == "sigmoid"):

			return 1 / (1 + np.exp(-data))

		elif (function.lower().lstrip().rstrip() == "tanh"):

			return np.tanh(data)

		elif (function.lower().lstrip().rstrip() == "relu"):

			return np.maximum(data, 0)

		elif (function.lower().lstrip().rstrip() == "step"):

			return np.heaviside(data, 0).astype(int)

		elif (function.lower().lstrip().rstrip() == "switch"):

			return np.sign(data).astype(int)

		return data

	def auditLUT(self, branch):

		if (len(Network.history) > 0):

			if (branch.innovation == 0):

				if not any(((synapse.input_node == branch.input_node) and
							(synapse.output_node == branch.output_node) and
							(synapse.skip == branch.skip) and
							(synapse.branch_type == branch.branch_type) and
							(synapse.recurrent == branch.recurrent)) for synapse in Network.history):

					branch.innovation = len(Network.history) + 1
					Network.history.append(branch)

				else:

					innovation = next((synapse.innovation for synapse in Network.history if (((synapse.input_node == branch.input_node) and
																							  (synapse.output_node == branch.output_node) and
																							  (synapse.skip == branch.skip) and
																							  (synapse.branch_type == branch.branch_type) and
																							  (synapse.recurrent == branch.recurrent)))), 0)

					branch.innovation = innovation

			else:

				if not any((synapse.innovation == branch.innovation) for synapse in Network.history):

					Network.history.append(branch)

		else:

			branch.innovation = 1
			Network.history.append(branch)

		Network.history = sorted(Network.history, key = lambda dna: dna.innovation)

	def propagate(self, data):

		self.output = []

		for layer, nodes in enumerate(self.network[1:]):

			for (address, node) in enumerate(nodes):

				if (node.node_type != "bias"):

					for branch in node.branches:

						if branch.active:

							neuron = next((vertex for index, vertex in enumerate(self.network[branch.input_layer]) if (vertex.node == branch.input_node)), 0)

							if (branch.input_layer == 0):

								if (neuron.node_type != "bias"):

									neuron.activity = data[neuron.node - 1]
									neuron.output = data[neuron.node - 1]

								else:

									neuron.activity = 1
									neuron.output = 1

							if (address == 0):

								node.activity = neuron.output*branch.weight

							else:

								node.activity += neuron.output*branch.weight

					node.output = self._activation(node.activity, node.function)

					if (layer == self.layers - 2):

						self.output.append(node.output)

		return self.output

	def render(self):

		canvas = nx.Graph()
		connections = []
		positions = {}
		styling = {}
		axis = plt.gca()
		maximum = max(abs(branch.weight) for layer in self.network for node in layer for branch in node.branches)
		height = max(len(layer) for layer in self.network)
		info = "\n"
		info += "="*50
		info += f"\n{self.layers} layer(s):\n"
		for index, layer in enumerate(self.network): info += f"\nlayer {index} --> {len(layer) - 1 if any(node.node_type == 'bias' for node in layer) else len(layer)}x node(s){' + bias' if any(node.node_type == 'bias' for node in layer) else ''}"
		info += "\n"
		info += "="*50

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
									  "connectionstyle": f"arc3,rad={ -0.08 if (link.skip and (positions[link.input_node][1] < -height / 2)) else 0.08 if (link.skip and (positions[link.input_node][1] >= -height / 2)) else 0 }",
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
		print(info + "\n")
		plt.show()
