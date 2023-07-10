

class Node:

	def __init__(self, node, layer, activity = 0, output = 0, function = None, branches = [], node_type = "neuron"):

		self.node = node
		self.layer = layer
		self.activity = activity
		self.output = output
		self.function = function
		self.branches = branches
		self.node_type = node_type

	def __repr__(self):

		info = f"node: {self.node}\n"
		info += f"type: {self.node_type}\n"
		info += f"layer: {self.layer}\n"
		info += f"input: {self.activity}\n"
		info += f"function: {self.function}\n"
		info += f"output: {self.output}\n"

		if (len(self.branches) == 0):

			info += "branches: []"

		else:

			info += "\nbranches:\n"
			info += "="*50
			info += "\n"

			for index, branch in enumerate(self.branches):

				if (index > 0):

					info += "\n"
					info += "_"*50
					info += "\n"

				for key, value in vars(branch).items():

					info += f"\n\t{key.replace('_', ' ')}: {value}"

		return info + "\n"
