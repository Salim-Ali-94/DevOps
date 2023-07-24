import random
from models.network import Network
from models.node import Node
from models.branch import Branch


def initializeGeneration(population_size, architecture, parameters):

	population = []

	while (len(population) < population_size):

		gene = Network(architecture,
					   bias_rate = parameters["bias_rate"],
					   connection_rate = parameters["connection_rate"],
					   active_rate = parameters["active_rate"],
					   skip_rate = parameters["skip_rate"],
					   recurrent_rate = parameters["recurrent_rate"],
					   recurrent = parameters["recurrent"],
					   skip = parameters["skip"])

		while (all(not(dna.active) for dna in gene.genome) or
			  (len(gene.genome) == 0)):

			gene = Network(architecture,
						   bias_rate = parameters["bias_rate"],
						   connection_rate = parameters["connection_rate"],
						   active_rate = parameters["active_rate"],
						   skip_rate = parameters["skip_rate"],
						   recurrent_rate = parameters["recurrent_rate"],
						   recurrent = parameters["recurrent"],
						   skip = parameters["skip"])

		population.append(gene)

	return population


def evaluateFitness(population, sensor, action, function):

	for chromosome in population:

		decision = chromosome.propagate(sensor)
		chromosome.fitness = action(decision, function, sensor)


def speciation(population, threshold = 0.3, c1 = 1, c2 = 1, c3 = 0.4):

	species = []

	for (group, chromosome_a) in enumerate(population[:-1]):

		if not any(chromosome_a in dna["chromosomes"] for dna in species):

			chromosome_a.species = group + 1
			species.append({ "group": group + 1,
							 "chromosomes": [chromosome_a],
							 "group_size": 1,
							 "group_fitness": chromosome_a.fitness,
							 "distributed_fitness": 0 })

			for chromosome_b in population[group + 1:]:

				if not any(chromosome_b in dna["chromosomes"] for dna in species):

					pairs = alignGenes(chromosome_a.genome, chromosome_b.genome)
					disjoint_a = countUnpaired(chromosome_a.genome, chromosome_b.genome)
					disjoint_b = countUnpaired(chromosome_b.genome, chromosome_a.genome)
					excess_a = countOffset(chromosome_a.genome, chromosome_b.genome)
					excess_b = countOffset(chromosome_b.genome, chromosome_a.genome)
					weight = sum(abs(pair[0].weight - pair[1].weight) for pair in pairs) / (len(pairs) if (len(pairs) > 0) else 1)
					disjoint = disjoint_a + disjoint_b
					excess = excess_a + excess_b
					factor = max(sum(1 for gene in chromosome_a.genome if gene.active), sum(1 for gene in chromosome_b.genome if gene.active), 1)
					compatibility = disjoint*c1 / factor + excess*c2 / factor + weight*c3

					if (compatibility < threshold):

						species[group]["chromosomes"].append(chromosome_b)
						species[group]["group_size"] += 1
						species[group]["group_fitness"] = sum(chromosome.fitness for chromosome in species[group]["chromosomes"]) / species[group]["group_size"]
						chromosome_b.species = group + 1

					if (group == len(population) - 2):

						if not any(chromosome_b in dna["chromosomes"] for dna in species):

							chromosome_b.species = group + 2
							species.append({ "group": len(species) + 1,
											 "chromosomes": [chromosome_b],
											 "group_size": 1,
											 "group_fitness": chromosome_b.fitness,
											 "distributed_fitness": 0 })

	modifyFitness(species)
	return species


def crossover(species, topology):

	generation = []

	for group in species:

		population = []

		while (len(population) < group["group_limit"]):

			offspring = []
			network_a = rouletteWheel(group)
			group["chromosomes"].remove(network_a)
			network_b = rouletteWheel(group)
			group["chromosomes"].append(network_a)
			pairs = alignGenes(network_a.genome, network_b.genome, True)
			detached_a = segmentGenes(network_a.genome, network_b.genome)
			detached_b = segmentGenes(network_b.genome, network_a.genome)
			offset_a = segmentGenes(network_a.genome, network_b.genome, "exterior")
			offset_b = segmentGenes(network_b.genome, network_a.genome, "exterior")
			detached = detached_a + detached_b
			offset = offset_a + offset_b
			offspring.extend(detached)

			for pair in pairs:

				gene = random.choice(pair)
				offspring.append(gene)

			for synapse in offset:

				if (((network_a.fitness > network_b.fitness) and
					  synapse in network_a.genome) or
					((network_b.fitness > network_a.fitness) and
					  synapse in network_b.genome)):

					offspring.append(synapse)

				elif (network_a.fitness == network_b.fitness):

					if (random.random() < 0.5):

						offspring.append(synapse)

			population.append(decodeGenome(offspring, topology))

		generation.extend(population)

	return generation


def decodeGenome(genome, architecture):
# def decodeGenome(genome):

	print(":"*100)
	print("GENOME:")
	print(":"*100)

	for gene in genome:

		print()
		print()
		print(f"N{gene.input_node} (@L{gene.input_layer}) / N{gene.output_node} (@L{gene.output_layer}) / id = {gene.innovation} / active = {gene.active} / w = {gene.weight} ({gene.branch_type})")
		print()
		print()

	# print(":"*100)


	network = Network(architecture, generate = False)
	network.layers = max(gene.output_layer for gene in genome) + 1
	# network = Network(generate = False)
	network.genome = genome[:]
	neurons = []
	network.network = [tuple()]*network.layers

	for gene in genome:

		# if gene.input_neuron not in network.neurons:
		if gene.input_neuron not in neurons:

			# network.neurons.append(gene.input_neuron)
			neurons.append(gene.input_neuron)

		# if gene.output_neuron not in network.neurons:
		if gene.output_neuron not in neurons:

			# network.neurons.append(gene.output_neuron)
			neurons.append(gene.output_neuron)

	# neurons = network.neurons[:]
	nodes = neurons[:]
	print(":"*100)
	print("NODES BEFORE:")
	print(":"*100)

	for node in nodes:

		print()
		print()
		print(f"N{node.node} (@L{node.layer}) / {node.node_type} & Ws = {len(node.branches)}")
		print()
		print()

	# for node in network.neurons:

	# for node in neurons:
	for (index, node) in enumerate(neurons):

		for branch in node.branches:
		# for (ID, branch) in enumerate(node.branches):

			if branch not in genome:

				# # # neurons.remove(branch)
				# # nodes.remove(branch)
				# # nodes[index].branches.pop(ID)
				# nodes[index].branches.remove(branch)

				if branch in nodes[index].branches:

					nodes[index].branches.remove(branch)

	# for (index, node) in enumerate(nodes):

	for gene in genome:
	# for (ID, branch) in enumerate(node.branches):

		# a = next((node for node in nodes if node.node == gene.input_node), [])
		a = next((node for node in nodes if node == gene.input_neuron), [])
		# b = next((node for node in nodes if node.neuron == gene.output_neuron), [])

		# if branch not in genome:
		if gene not in a.branches:

			a.branches.append(gene)

			# # # neurons.remove(branch)
			# # nodes.remove(branch)
			# # nodes[index].branches.pop(ID)
			# nodes[index].branches.remove(branch)

			# if branch in nodes[index].branches:

			# 	nodes[index].branches.remove(branch)

	# network.neurons = neurons[:]
	network.neurons = nodes[:]



	# for node in network.neurons:

	# 	for branch in node.branches:

	# 		if branch not in genome:

	# 			if branch in node.branches:

	# 				node.branches.remove(branch)

	# network.neurons = neurons[:]
	# # network.neurons = nodes[:]

	# print()
	# print()
	# print()
	# print()

	print(":"*100)
	print("NODES AFTER:")
	print(":"*100)

	for node in nodes:

		print()
		print()
		print(f"N{node.node} (@L{node.layer}) / {node.node_type} & Ws = {len(node.branches)}")
		print()
		print()

	print(":"*100)

	for node in nodes:

		# print(f"node = {node.node} @{node.layer} / type = {node.node_type}")
		network.network[node.layer] += (node, )
		network.network[node.layer] = sorted(network.network[node.layer], key = lambda dna: dna.node)

	# print()
	# print()
	# print()
	# print()
	return network
# def decodeGenome(genome, architecture):
# # def decodeGenome(genome):

# 	print(":"*100)
# 	print("GENOME:")
# 	print(":"*100)

# 	for gene in genome:

# 		print()
# 		print()
# 		print(f"N{gene.input_node} (@L{gene.input_layer}) / N{gene.output_node} (@L{gene.output_layer}) / id = {gene.innovation} / active = {gene.active} / w = {gene.weight} ({gene.branch_type})")
# 		print()
# 		print()

# 	# print(":"*100)


# 	network = Network(architecture, generate = False)
# 	network.layers = max(gene.output_layer for gene in genome) + 1
# 	# network = Network(generate = False)
# 	network.genome = genome[:]
# 	neurons = []
# 	network.network = [tuple()]*network.layers

# 	for gene in genome:

# 		if gene.input_neuron not in network.neurons:
# 		# if gene.input_neuron not in neurons:

# 			network.neurons.append(gene.input_neuron)
# 			# neurons.append(gene.input_neuron)

# 		if gene.output_neuron not in network.neurons:
# 		# if gene.output_neuron not in neurons:

# 			network.neurons.append(gene.output_neuron)
# 			# neurons.append(gene.output_neuron)

# 	print(":"*100)
# 	print("NODES AFTER:")
# 	print(":"*100)

# 	for node in nodes:

# 		print()
# 		print()
# 		print(f"N{node.node} (@L{node.layer}) / {node.node_type} & Ws = {len(node.branches)}")
# 		print()
# 		print()

# 	print(":"*100)

# 	for node in nodes:

# 		# print(f"node = {node.node} @{node.layer} / type = {node.node_type}")
# 		network.network[node.layer] += (node, )
# 		network.network[node.layer] = sorted(network.network[node.layer], key = lambda dna: dna.node)

# 	# print()
# 	# print()
# 	# print()
# 	# print()
# 	return network


def modifyFitness(species):

	global_fitness = 0
	size = 0

	for group in species:

		for chromosome in group["chromosomes"]:

			chromosome.modified_fitness = chromosome.fitness / group["group_size"]
			group["distributed_fitness"] += chromosome.modified_fitness
			global_fitness += chromosome.modified_fitness

		group["distributed_fitness"] /= group["group_size"]
		size += group["group_size"]

	global_fitness /= size

	for group in species:

		limit = round(group["group_size"]*group["distributed_fitness"] / global_fitness)
		group["group_limit"] = max(limit, 1)


def alignGenes(genome_a, genome_b, off = False):

	group = []

	for a in genome_a:

		for b in genome_b:

			if ((a.innovation == b.innovation) and
				(off or (a.active and b.active))):

				group.append((a, b))

	return group


def segmentGenes(genome_a, genome_b, region = "interior"):

	unpaired = []
	maximum_b = genome_b[-1].innovation

	for a in genome_a:

		if all(((b.innovation != a.innovation) and
				((a.innovation < maximum_b) if (region == "interior") else
				 (a.innovation > maximum_b))) for b in genome_b):

			unpaired.append(a)

	return unpaired


def countUnpaired(genome_a, genome_b):

	count = 0
	maximum_b = genome_b[-1].innovation

	for a in genome_a:

		if (a.active and
		   ((a.innovation < maximum_b) and
		   	not any(b.innovation == a.innovation for b in genome_b) or
		   	any((a.innovation == b.innovation) and
				(not b.active and a.active) for b in genome_b))):

			count += 1

	return count


def countOffset(genome_a, genome_b):

	count = 0
	maximum_b = genome_b[-1].innovation

	for a in genome_a:

		if (a.active and
		   ((a.innovation > maximum_b) and
			not any(b.innovation == a.innovation for b in genome_b) or
			any((not b.active and (a.innovation == b.innovation)) for b in genome_b))):

			count += 1

	return count


def rouletteWheel(group):

	absolute_fitness = group["distributed_fitness"]*group["group_size"]
	random.shuffle(group["chromosomes"])
	theta = random.uniform(0, 1)
	probability = 0

	for chromosome in group["chromosomes"]:

		probability += chromosome.modified_fitness / absolute_fitness

		if (probability >= theta):

			return chromosome

	maximum = max(dna.fitness for dna in group["chromosomes"])
	candidate = next((gene for gene in group["chromosomes"] if (gene.fitness == maximum)), random.choice(group["chromosomes"]))
	return candidate
