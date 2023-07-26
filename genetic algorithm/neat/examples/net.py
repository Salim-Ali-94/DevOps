# import random
# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from models.network import Network
# import utility


# if __name__ == "__main__":

# 	x = [0.2, -0.5, 0.8]

# 	structure = { "output_neurons": 2,
# 				  "input_neurons": len(x),
# 				  "output_function": "sigmoid",
# 				  "maximum_layers": 10,
# 				  "minimum_layers": 1,
# 				  "maximum_weight": 2,
# 				  "minimum_weight": -2,
# 				  "maximum_neurons": 10,
# 				  "minimum_neurons": 1 }

# 	params = { "bias_rate": 0.5,
# 			   "connection_rate": 0.5,
# 			   "active_rate": 0.5,
# 			   "recurrent_rate": 0.5,
# 			   "skip_rate": 0.1,
# 			   "recurrent": False,
# 			   "skip": True }

# 	N = 5
# 	delta = random.randint(10, 20)
# 	ann = Network(structure, skip = True, active_rate = 0.75, skip_rate = 0.25, connection_rate = 0.5)
# 	pop = utility.initializeGeneration(N, structure, params)
# 	ann.render()
# 	print(pop)

# # x = [1, 2, 3]
# # # y = x.append(4)
# # y = x + [4]
# # print(y)

# class ClassA:
#     def __init__(self):
#         self.list_property = []

# class ClassB:
#     def __init__(self, obj):
#         self.reference_to_obj = obj

# # Instantiate objects
# obj_a = ClassA()
# obj_b = ClassB(obj_a)

# # Modify the list property in object A
# obj_a.list_property.append(42)

# # Access the list property through object B
# print(obj_b.reference_to_obj.list_property)  # Output: [42]
class Neuron:
    def __init__(self, id):
        self.id = id
        self.branches = []

class Synapse:
    def __init__(self, innovation, input_neuron, output_neuron):
        self.innovation = innovation
        self.input_neuron = input_neuron
        self.output_neuron = output_neuron

neuron1 = Neuron(1)
neuron2 = Neuron(2)
synapse1 = Synapse(1, neuron1, neuron2)
neuron1.branches.append(synapse1)
neuron2.branches.append(synapse1)
synapse1.innovation = 2
neuron3 = Neuron(3)
neuron3.branches.extend((synapse1, synapse1, synapse1, synapse1))
synapse1.input_neuron = neuron3
# synapse1.output_neuron = neuron3
print(synapse1.input_neuron.id)
print(synapse1.input_neuron.branches)

print("Neuron 1 branches:", [synapse.innovation for synapse in neuron1.branches])
print("Neuron 2 branches:", [synapse.innovation for synapse in neuron2.branches])
print("Neuron 3 branches:", [synapse.innovation for synapse in neuron3.branches])
