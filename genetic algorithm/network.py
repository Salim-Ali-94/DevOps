import random
import webbrowser
from pyvis.network import Network as net
import utility
from node import Node
from branch import Branch
import networkx as nx
import matplotlib.pyplot as plt

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

			for row, node in enumerate(nodes):

				if (node.node_type != "bias"):

					for branch in node.branches:

						neuron = next((vertex for index, vertex in enumerate(self.network[branch.input_layer]) if (vertex.node == branch.input_node)), 0)
						node.activity += neuron.output*branch.weight

					node.output = utility.activation(node.activity, node.function)

					if (layer == self.layers - 2):
	
						output.append(node.output)

		return output

	# def __repr__(self):

	# 	ann = net()
	# 	step = 10
	# 	height = 5

	# 	for layer, neurons in enumerate(self.network):

	# 		for row, neuron in enumerate(neurons):

	# 			ann.add_node(neuron.node,
	# 						 label = str(neuron.node),
	# 						 x = step*layer,
	# 						 y = height*row,
	# 						 color = "#e50191" if (neuron.node_type == "bias") else "#ac05f7",
	# 						 # size = 30 if (neuron.node_type == "bias") else 50)
	# 						 size = 10 if (neuron.node_type == "bias") else 20)

	# 			if (layer > 0):

	# 				for link in neuron.branches:

	# 					if link.active:

	# 						ann.add_edge(link.input_node,
	# 									 link.output_node,
	# 									 color = "#000" if (link.branch_type == "bias") else "#9cf168",
	# 									 physics = False,
	# 									 # width = 4 if (link.branch_type == "bias") else 10)
	# 									 width = 1 if (link.branch_type == "bias") else 3)

	# 	# ann.barnes_hut()
	# 	ann.show("ann.html", notebook = False)
	# 	webbrowser.open_new_tab("ann.html")
	# 	# return fr"{self.layers} layers\n{'\n'.join([str(len(nodes)) for layer, nodes in enumerate(self.network)])}"
	# 	return f"{self.layers} layers"
	# 	# return f"{self.layers} layers\n{'\n'.join([str(len(nodes)) for layer, nodes in enumerate(self.network)])}"


	# def __repr__(self):

	# 	ann = nx.Graph()
	# 	step = 10
	# 	height = 5
	# 	dnn = []
	# 	positions = {}
	# 	node_styles = {}
	# 	edge_styles = {}
	# 	axis = plt.gca()
	# 	maximum = max(abs(branch.weight) for layer in self.network for node in layer for branch in node.branches)

	# 	for layer, neurons in enumerate(self.network):

	# 		for row, neuron in enumerate(neurons):

	# 			positions[neuron.node] = (layer, -row)
	# 			node_styles[neuron.node] = { "color": "#e50191" if (neuron.node_type == "bias") else "#ac05f7",
	# 										 "size": 500 if (neuron.node_type == "bias") else 800 }

	# 			if (layer > 0):

	# 				for link in neuron.branches:

	# 					if link.active:

	# 						dnn.append((link.input_node, link.output_node))
	# 						# edge_styles[(link.input_node, link.output_node)] = { "color": "#000" if (link.branch_type == "bias") else "#9cf168",
	# 						# 							 						 "width": 1 if (link.branch_type == "bias") else 2,
	# 						# 							 						 "style": "--" if link.skip else "-" }

	# 						lines = dict(arrowstyle = "-",
	# 									 color = "#000" if (link.branch_type == "bias") else "#9cf168",
	# 									 connectionstyle = f"arc3,rad={0.05 if link.skip else 0}",
	# 									 linestyle = "--" if link.skip else "-",
	# 									 alpha = 0.8 if link.skip else 1,
	# 									 # linewidth = 1 if (link.branch_type == "bias") else 1.5,
	# 									 linewidth = 0.5 if (abs(link.weight) < 0.5) else 2*abs(link.weight) / maximum,
	# 									 zorder = -1)

	# 						axis.annotate("",
	# 									  xy = positions[link.input_node],
	# 									  xytext = positions[link.output_node],
	# 									  arrowprops = lines)

	# 	ann.add_edges_from(dnn)
	# 	# axis = plt.gca()

	# 	# for edge in ann.edges():
			
	# 	# 	source, target = edge
	# 	# 	radius = 0.2

	# 	# 	lines = dict(arrowstyle = "-", 
	# 	# 				 color = "black" if (source%2 == 0) else "blue",
	# 	# 				 connectionstyle = f"arc3,rad={radius}",
	# 	# 				 linestyle = "-" if (target%2 == 0) else "--",
	# 	# 				 alpha = 0.6,
	# 	# 				 linewidth = 5)

	# 	# 	axis.annotate("",
	# 	# 				  xy = positions[source],
	# 	# 				  xytext = positions[target],
	# 	# 				  arrowprops = lines)
		
	# 	# nx.draw_networkx_edges(ann,
	# 	# 					   positions,
	# 						   # edgelist = edge_styles.keys(),
	# 						   # width = [edge_styles[e]["width"] for e in edge_styles],
	# 						   # edge_color = [edge_styles[e]["color"] for e in edge_styles],
	# 						   # style = [edge_styles[e]["style"] for e in edge_styles])

	# 	nx.draw_networkx_nodes(ann,
	# 						   positions,
	# 						   nodelist = node_styles.keys(),
	# 						   node_size = [node_styles[n]["size"] for n in node_styles],
	# 						   node_color = [node_styles[n]["color"] for n in node_styles]).set_zorder(2)
	# 						   # node_color = [node_styles[n]["color"] for n in node_styles],
	# 						   # zorder = 2)

	# 	nx.draw_networkx_labels(ann,
	# 							positions,
	# 							font_color = "white",
	# 							font_weight = "bold",
	# 							font_family = "arial")

	# 	plt.axis("off")
	# 	plt.show()
	# 	return f"{self.layers} layers"

	def __repr__(self):

		ann = nx.Graph()
		step = 10
		height = 5
		dnn = []
		positions = {}
		node_styles = {}
		edge_styles = {}
		axis = plt.gca()
		maximum = max(abs(branch.weight) for layer in self.network for node in layer for branch in node.branches)
		height = max(len(layer) for layer in self.network)

		for layer, neurons in enumerate(self.network):

			for row, neuron in enumerate(neurons):

				# positions[neuron.node] = (layer, -row)
				positions[neuron.node] = (layer, (-2*row - abs(len(neurons) - height)) / 2)
				# node_styles[neuron.node] = { "color": "#e50191" if (neuron.node_type == "bias") else "#ac05f7",
				node_styles[neuron.node] = { "color": "#9cf168" if (neuron.node_type == "bias") else "#ac05f7",
											 "size": 500 if (neuron.node_type == "bias") else 800 }

				if (layer > 0):

					for link in neuron.branches:

						if link.active:

							dnn.append((link.input_node, link.output_node))
							# edge_styles[(link.input_node, link.output_node)] = { "color": "#000" if (link.branch_type == "bias") else "#9cf168",
							# 							 						 "width": 1 if (link.branch_type == "bias") else 2,
							# 							 						 "style": "--" if link.skip else "-" }

							lines = dict(arrowstyle = "-",
										 # color = "#000" if (link.branch_type == "bias") else "#9cf168",
										 color = "#9cf168" if (link.branch_type == "bias") else "#ac05f7",
										 connectionstyle = f"arc3,rad={0.05 if link.skip else 0}",
										 linestyle = "--" if link.skip else "-",
										 alpha = 0.6 if link.skip else 1,
										 # linewidth = 1 if (link.branch_type == "bias") else 1.5,
										 linewidth = 0.5 if (abs(link.weight) < 0.5) else 2*abs(link.weight) / maximum,
										 zorder = 1)

							axis.annotate("",
										  xy = positions[link.input_node],
										  xytext = positions[link.output_node],
										  arrowprops = lines)

		ann.add_edges_from(dnn)

		nx.draw_networkx_nodes(ann,
							   positions,
							   nodelist = node_styles.keys(),
							   node_size = [node_styles[n]["size"] for n in node_styles],
							   node_color = [node_styles[n]["color"] for n in node_styles]).set_zorder(10)

		# offset = { key: (value[0], value[1] + 0.1) for key, value in positions.items() }

		# nx.draw_networkx_labels(ann,
		# 						positions,
		# 						# offset,
		# 						font_color = "white",
		# 						# font_color = "black",
		# 						font_weight = "bold",
		# 						font_family = "arial",
		# 						clip_on = False)

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
		# plt.savefig("graph.png", dpi = 1000)
		plt.show()
		return f"{self.layers} layers"
