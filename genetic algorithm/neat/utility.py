from models.network import Network


def initializeGeneration(population_size, architecture, parameters):

	population = []

	while (len(population) < population_size):

		gene = Network(architecture,
					   bias_rate = parameters["bias_rate"],
					   connection_rate = parameters["connection_rate"],
					   active_rate = parameters["active_rate"],
					   recurrent = parameters["recurrent"],
					   skip = parameters["skip"],
					   recurrent_rate = parameters["recurrent_rate"])

		while all(len(node.branches) == 0 for layer in gene.network[1:] for node in layer):

			gene = Network(architecture,
						   bias_rate = parameters["bias_rate"],
						   connection_rate = parameters["connection_rate"],
						   active_rate = parameters["active_rate"],
						   recurrent = parameters["recurrent"],
						   skip = parameters["skip"],
						   recurrent_rate = parameters["recurrent_rate"])

		population.append(gene)

	return population
