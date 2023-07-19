import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.network import Network


if __name__ == "__main__":

	x = [0.2, -0.5, 0.8]

	structure = { "output_neurons": 2,
				  "input_neurons": len(x),
				  "maximum_layers": 10,
				  "minimum_layers": 1,
				  "maximum_weight": 2,
				  "minimum_weight": -2,
				  "maximum_neurons": 10,
				  "minimum_neurons": 1 }

	ann = Network(structure, active_rate = 0.75, connection_rate = 0.5)
	print(ann)
