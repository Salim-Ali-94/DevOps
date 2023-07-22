import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.network import Network
import utility


if __name__ == "__main__":

	x = [0.2, -0.5, 0.8]

	structure = { "output_neurons": 2,
				  "input_neurons": len(x),
				  "output_function": "sigmoid",
				  "maximum_layers": 10,
				  "minimum_layers": 1,
				  "maximum_weight": 2,
				  "minimum_weight": -2,
				  "maximum_neurons": 10,
				  "minimum_neurons": 1 }

	params = { "bias_rate": 0.5,
			   "connection_rate": 0.5,
			   "active_rate": 0.5,
			   "recurrent_rate": 0.5,
			   "skip_rate": 0.1,
			   "recurrent": False,
			   "skip": True }

	N = 5
	delta = random.randint(10, 20)
	ann = Network(structure, skip = True, active_rate = 0.75, skip_rate = 0.25, connection_rate = 0.5)
	pop = utility.initializeGeneration(N, structure, params)
	print(ann), print(pop)
