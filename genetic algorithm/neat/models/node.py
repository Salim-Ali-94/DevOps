

class Node:

	def __init__(self, node, layer, activity = 0, output = 0, function = None, branches = None, node_type = "neuron"):

		if (branches is None): branches = []
		self.node = node
		self.layer = layer
		self.activity = activity
		self.output = output
		self.function = function
		self.branches = branches
		self.node_type = node_type
