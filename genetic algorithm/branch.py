

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

	def __str__(self):

		details = f"innovation: {self.innovation}\n"
		details += f"type: {self.branch_type}\n"
		details += f"weight: {self.weight}\n"
		details += f"active: {self.active}\n"
		details += f"connection: N{self.input_node} --> N{self.output_node}\n"
		details += f"recurrent: {self.recurrent}\n"
		details += f"path: L{self.input_layer} --> L{self.output_layer}\n"
		details += f"skip: {self.skip}\n"
		return details + "\n"
