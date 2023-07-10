

class Branch:

	def __init__(self, weight, input_node, output_node, input_layer, output_layer, active = True, branch_type = "synapse", recurrent = False, skip = False, innovation = 0):

		self.weight = weight
		self.input_node = input_node
		self.output_node = output_node
		self.input_layer = input_layer
		self.output_layer = output_layer
		self.branch_type = branch_type
		self.active = active
		self.recurrent = recurrent
		self.skip = skip
		self.innovation = innovation
