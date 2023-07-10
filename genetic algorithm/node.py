

class Node:

	def __init__(self, node, layer, activity = 0, output = 0, function = None, branches = [], node_type = "neuron"):

		self.node = node
		self.layer = layer
		self.activity = activity
		self.output = output
		self.function = function
		self.branches = branches
		self.node_type = node_type
