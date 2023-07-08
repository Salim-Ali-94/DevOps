

# class Network:

# 	def __init__(self, structure):

# 		pass
# 		


import random
import branch
import node

neuron = node.Node(5, 2, 0, 0, "sigmoid", [], "neuron")
# synapse = branch.Branch(random.uniform(-2, 2), 1, 5, "synapse", False, False, True, 0, 1, 1)
synapse = branch.Branch(random.uniform(-2, 2), 1, 5, "synapse", "node", False, False, True, 0, 0, "relu", 0, 1, 1)
# line = branch.Branch(random.uniform(-2, 2), 1, 5, "synapse", False, False, True, 0, 1, 1)
line = branch.Branch(random.uniform(-2, 2), 1, 5, "synapse", "node", False, False, True, 0, 0, "relu", 0, 1, 1)
print(neuron.node)
print(neuron.layer)
# print(neuron.activity)
print(neuron._input)
print(neuron.output)
# print(neuron.activation)
print(neuron.function)
# neuron.weights.append(random.uniform(-2, 2))
neuron.weights.append(synapse)
print(neuron.weights)
# print(neuron.category)
print(neuron._type)

for w in neuron.weights:

	print(w.weight)
	# print(w.source)
	print(w.input_node)
	# print(w.target)
	print(w.output_node)
	# print(w.category)
	print(w._type)
	print(w.category)
	print(w.recurrent)
	print(w.skip)
	print(w.active)
	print(w.input_layer)
	print(w.output_layer)
	print(w.innovation)
	print(w._input)
	print(w.output)
	print(w.function)

# print(line == synapse)
print(line.innovation == synapse.innovation)

def foo(x, y):

	print("X =", x)
	print("Y =", y)

foo(y = "_Y_", x = "_X_")