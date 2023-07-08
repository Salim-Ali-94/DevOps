

class Branch:

	def __init__(self,
				 weight,
				 input_node,
				 output_node,
				 category,
				 _type,
				 recurrent,
				 skip,
				 active,
				 _input,
				 output,
				 function,
				 input_layer,
				 output_layer,
				 innovation = 0):

		self.weight = weight
		self.input_node = input_node
		self.output_node = output_node
		self.category = category
		# self.category = category
		self._type = _type
		self.recurrent = recurrent
		self.skip = skip
		self.active = active
		# self.activity = activity
		self._input = _input
		self.output = output
		# self.activation = activation
		self.function = function
		self.innovation = innovation
		self.input_layer = input_layer
		self.output_layer = output_layer
