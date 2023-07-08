

class Node:

	def __init__(self, node, layer, _input, output, function, weights, _type):

		self.node = node
		self.layer = layer
		# self.activity = activity
		self._input = _input
		self.output = output
		self.function = function
		self.weights = weights
		# self.category = category
		self._type = _type
