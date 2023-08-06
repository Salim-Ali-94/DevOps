import random
import copy
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
			buffer = {}
			network_a = rouletteWheel(group)
			group["chromosomes"].remove(network_a)
			network_b = rouletteWheel(group)
			group["chromosomes"].append(network_a)
			pairs = alignGenes(network_a.genome, network_b.genome, True)
			# pairs = alignGenes({"dna": network_a.genome, "net": "a" }, network_b.genome, True)
			detached_a = segmentGenes(network_a.genome, network_b.genome)
			# detached_a = segmentGenes({ "dna": network_a.genome, "net": "a" }, network_b.genome)
			detached_b = segmentGenes(network_b.genome, network_a.genome)
			# detached_b = segmentGenes({ "dna": network_b.genome, "net": "b" }, network_a.genome)
			offset_a = segmentGenes(network_a.genome, network_b.genome, "exterior")
			# offset_a = segmentGenes({"dna": network_a.genome, "net": "a" }, network_b.genome, "exterior")
			offset_b = segmentGenes(network_b.genome, network_a.genome, "exterior")
			# offset_b = segmentGenes({"dna": network_b.genome, "net": "b" }, network_a.genome, "exterior")
			detached = detached_a + detached_b
			# detached = [(a, "a") for a in detached_a] + [(b, "b") for b in detached_b]
			offset = offset_a + offset_b
			# offset = [(a, "a") for a in offset_a] + [(b, "b") for b in offset_b]
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

			# # print("*"*100)
			# # print("KID BEFORE:")
			# # for kid in offspring:
			# # 	print("Ni:", kid.input_node)
			# # 	print("Li:", kid.input_layer)
			# # 	print("No:", kid.output_node)
			# # 	print("Lo:", kid.output_layer)
			# # print("*"*100)

			# for branch in offspring:

			# 	if (branch.branch_type == "bias"):

			# 		if not any(branch.input_layer == link.input_layer for _, links in buffer.items() for link in links):

			# 			buffer[branch.input_layer] = [branch]

			# 		else:

			# 			buffer[branch.input_layer].append(branch)

			# print("*"*100)
			# print("BUFFER SIZE:", len(buffer))
			# print("*"*100)

			# for layer, collection in buffer.items():

			# 	if (len(collection) > 1):

			# 		print("MODDING", len(collection))
			# 		# ID = sum(link.input_node for link in collection)
			# 		ID = min([link.input_node for link in network_a.genome if (link.branch_type == "bias")] +
			# 				 [link.input_node for link in network_b.genome if (link.input_node < 0)] +
			# 				 [link.input_node for link in collection if (link.input_node < 0)]) - 1
			# 		# innovation = max([link.innovation for link in offspring] + [link.innovation for _, links in buffer for link in links]) + 1
			# 		neuron = Node(node = ID,
			# 				      layer = layer,
			# 				      branches = [],
			# 				      function = None,
			# 				      activity = 1,
			# 				      output = 1,
			# 				      node_type = "bias")

			# 		for branch in collection:

			# 			net = next((net for net in [network_a, network_b] if branch in net.genome), None)
			# 			branch.input_neuron = neuron
			# 			branch.input_node = ID
			# 			# branch.innovation = innovation
			# 			branch.innovation = 0
			# 			net.auditLUT(branch)

			# # print("*"*100)
			# # print("KID AFTER:")
			# # for kid in offspring:
			# # 	print("Ni:", kid.input_node)
			# # 	print("Li:", kid.input_layer)
			# # 	print("No:", kid.output_node)
			# # 	print("Lo:", kid.output_layer)
			# # print("*"*100)

			population.append(decodeGenome(offspring, topology))

		generation.extend(population)

	return generation


# # # def decodeGenome(genome, architecture):

# # # 	network = Network(architecture, generate = False)

# # # 	for gene in genome:

# # # 		if not any(dna.node == gene.input_node for dna in network.neurons):

# # # 			input_neuron = Node(node = gene.input_node,
# # # 							    layer = gene.input_layer,
# # # 							    branches = [],
# # # 							    function = gene.input_neuron.function,
# # # 							    activity = 1 if (gene.input_neuron.node_type == "bias") else 0,
# # # 							    output = 1 if (gene.input_neuron.node_type == "bias") else 0,
# # # 							    node_type = gene.input_neuron.node_type)

# # # 			network.neurons.append(input_neuron)

# # # 		else:

# # # 			input_neuron = next((dna for dna in network.neurons if (dna.node == gene.input_node)), None)

# # # 			if (gene.input_layer < input_neuron.layer):

# # # 				input_neuron.layer = gene.input_layer
# # # 				input_neuron.function = random.choice((gene.input_neuron.function, input_neuron.function))

# # # 		if not any(dna.node == gene.output_node for dna in network.neurons):

# # # 			output_neuron = Node(node = gene.output_node,
# # # 							     layer = gene.output_layer,
# # # 							     branches = [],
# # # 							     function = gene.output_neuron.function,
# # # 							     activity = 1 if (gene.output_neuron.node_type == "bias") else 0,
# # # 							     output = 1 if (gene.output_neuron.node_type == "bias") else 0,
# # # 							     node_type = gene.output_neuron.node_type)

# # # 			network.neurons.append(output_neuron)

# # # 		else:

# # # 			output_neuron = next((dna for dna in network.neurons if (dna.node == gene.output_node)), None)

# # # 			if (gene.output_layer < output_neuron.layer):

# # # 				output_neuron.layer = gene.output_layer
# # # 				output_neuron.function = random.choice((gene.output_neuron.function, output_neuron.function))

# # # 		synapse = Branch(weight = gene.weight,
# # # 						 input_node = gene.input_node,
# # # 						 output_node = gene.output_node,
# # # 						 input_neuron = input_neuron,
# # # 						 output_neuron = output_neuron,
# # # 						 input_layer = input_neuron.layer,
# # # 						 output_layer = output_neuron.layer,
# # # 						 active = gene.active,
# # # 						 branch_type = gene.branch_type,
# # # 						 recurrent = gene.recurrent,
# # # 						 skip = gene.skip,
# # # 						 innovation = gene.innovation)

# # # 		if (output_neuron.node_type != "bias"):

# # # 			output_neuron.branches.append(synapse)

# # # 		network.genome.append(synapse)

# # # 	network.layers = max(dna.layer for dna in network.neurons) + 1
# # # 	network.network = [tuple()]*network.layers

# # # 	for node in network.neurons:

# # # 		network.network[node.layer] += (node, )
# # # 		# network.network[node.layer] = sorted(network.network[node.layer], key = lambda dna: (dna.node < 0, dna.node))
# # # 		network.network[node.layer] = sorted(network.network[node.layer], key = lambda dna: dna.node)
# # # 		# network.network[node.layer] = sorted(network.network[node.layer], key = lambda dna: (dna.node_type != "bias", dna.node))

# # # 	return network
# # def decodeGenome(genome, architecture):

# # 	network = Network(architecture, generate = False)
# # 	groups = {}

# # 	for gene in genome:

# # 		input_neuron = Node(node = gene.input_node,
# # 						    layer = gene.input_layer,
# # 						    branches = [],
# # 						    function = gene.input_neuron.function,
# # 						    activity = 1 if (gene.input_neuron.node_type == "bias") else 0,
# # 						    output = 1 if (gene.input_neuron.node_type == "bias") else 0,
# # 						    node_type = gene.input_neuron.node_type)

# # 		output_neuron = Node(node = gene.output_node,
# # 						     layer = gene.output_layer,
# # 						     branches = [],
# # 						     function = gene.output_neuron.function,
# # 						     activity = 1 if (gene.output_neuron.node_type == "bias") else 0,
# # 						     output = 1 if (gene.output_neuron.node_type == "bias") else 0,
# # 						     node_type = gene.output_neuron.node_type)

# # 		synapse = Branch(weight = gene.weight,
# # 						 input_node = gene.input_node,
# # 						 output_node = gene.output_node,
# # 						 input_neuron = input_neuron,
# # 						 output_neuron = output_neuron,
# # 						 input_layer = input_neuron.layer,
# # 						 output_layer = output_neuron.layer,
# # 						 active = gene.active,
# # 						 branch_type = gene.branch_type,
# # 						 recurrent = gene.recurrent,
# # 						 skip = gene.skip,
# # 						 innovation = gene.innovation)

# # 		if not any(level == gene.input_layer for level, _ in group.items()):

# # 			group[gene.input_layer] = [{ "ID": gene.input_node, "connections":  [(gene.output_node, gene.output_layer)] }]

# # 		else:

# # 			neuron = next((ID for ID, _ in group[gene.input_layer] if ID == gene.input_node), None)

# # 			if neuron is not None:

# # 				neuron["connections"].append((gene.output_node, gene.output_layer))

# # 			else:

# # 				group[gene.input_layer].append({ "ID": gene.input_node, "connections":  [(gene.output_node, gene.output_layer)] })

# # 		if not any(level == gene.output_layer for level, _ in group.items()):

# # 			group[gene.output_layer] = [{ "ID": gene.output_node, "connections":  [(gene.input_node, gene.input_layer)] }]

# # 		else:

# # 			neuron = next((ID for ID, _ in group[gene.output_layer] if ID == gene.output_node), None)

# # 			if neuron is not None:

# # 				neuron["connections"].append((gene.input_node, gene.input_layer))

# # 			else:

# # 				group[gene.output_layer].append({ "ID": gene.output_node, "connections":  [(gene.input_node, gene.input_layer)] })
# # 		# if not any(level == gene.input_layer for level, _ in group.items()):

# # 		# 	group[gene.input_layer] = [gene.input_node]

# # 		# else:

# # 		# 	group[gene.input_layer].append(gene.input_node)

# # 		# if not any(level == gene.output_layer for level, _ in group.items()):

# # 		# 	group[gene.output_layer] = [gene.output_node]

# # 		# else:

# # 		# 	group[gene.output_layer].append(gene.output_node)

# # 	# group = { index: group[key] for index, key in enumerate(sorted(group)) }
# # 	group = { index: list(set(group[key])) for index, key in enumerate(sorted(group)) }
# # 	# last = list(group.keys())[-1]
# # 	# duplicates = {}

# # 	# for layer, nodes in group.items():

# # 	# 	# nodes = list(set(nodes))

# # 	# 	if ((layer < last) and
# # 	# 		(layer > 0)):

# # 	# 		for node in nodes:

# # 	# 			# clones = [neuron for _, nodes in dict(list(group.items())[layer + 1:]).items() for neuron in nodes if (neuron == node)]
# # 	# 			# clones = [neuron for nodes in list(group.values())[layer + 1:] for neuron in nodes if (neuron == node)]
# # 	# 			layers = [depth for depth in list(group)[layer + 1:] for neuron in list(group.values())[layer + 1:][depth] if (neuron == node)]

# # 	# 			if (len(layers) > 1):

# # 	# 				duplicates[node] = layers

# # 	network.layers = max(dna.layer for dna in network.neurons) + 1
# # 	network.network = [tuple()]*network.layers

# # 	for node in network.neurons:

# # 		network.network[node.layer] += (node, )
# # 		# network.network[node.layer] = sorted(network.network[node.layer], key = lambda dna: (dna.node < 0, dna.node))
# # 		network.network[node.layer] = sorted(network.network[node.layer], key = lambda dna: dna.node)
# # 		# network.network[node.layer] = sorted(network.network[node.layer], key = lambda dna: (dna.node_type != "bias", dna.node))

# # 	return network

# def decodeGenome(genome, architecture):

# 	network = Network(architecture, generate = False)
# 	connections = {}
# 	mapping = {}
# 	group = {}

# 	for gene in genome:

# 		input_neuron = Node(node = gene.input_node,
# 						    layer = gene.input_layer,
# 						    branches = [],
# 						    function = gene.input_neuron.function,
# 						    activity = 1 if (gene.input_neuron.node_type == "bias") else 0,
# 						    output = 1 if (gene.input_neuron.node_type == "bias") else 0,
# 						    node_type = gene.input_neuron.node_type)

# 		output_neuron = Node(node = gene.output_node,
# 						     layer = gene.output_layer,
# 						     branches = [],
# 						     function = gene.output_neuron.function,
# 						     activity = 1 if (gene.output_neuron.node_type == "bias") else 0,
# 						     output = 1 if (gene.output_neuron.node_type == "bias") else 0,
# 						     node_type = gene.output_neuron.node_type)

# 		synapse = Branch(weight = gene.weight,
# 						 input_node = gene.input_node,
# 						 output_node = gene.output_node,
# 						 input_neuron = input_neuron,
# 						 output_neuron = output_neuron,
# 						 input_layer = input_neuron.layer,
# 						 output_layer = output_neuron.layer,
# 						 active = gene.active,
# 						 branch_type = gene.branch_type,
# 						 recurrent = gene.recurrent,
# 						 skip = gene.skip,
# 						 innovation = gene.innovation)

# 		# if not any(level == gene.input_layer for level, _ in group.items()):
# 		if not any(level == gene.input_layer for level in group.keys()):

# 			# group[gene.input_layer] = [{ "ID": gene.input_node, "connections":  [(gene.output_node, gene.output_layer)] }]
# 			group[gene.input_layer] = [{ "ID": gene.input_node,
# 										 "connections":  [] }]

# 		else:

# 			# neuron = next((ID for ID, _ in group[gene.input_layer] if ID == gene.input_node), None)

# 			# if neuron is not None:

# 			# 	neuron["connections"].append((gene.output_node, gene.output_layer))

# 			# else:

# 				# group[gene.input_layer].append({ "ID": gene.input_node, "connections":  [(gene.output_node, gene.output_layer)] })
# 			group[gene.input_layer].append({ "ID": gene.input_node,
# 											 "connections":  [] })

# 		# if not any(level == gene.output_layer for level, _ in group.items()):
# 		if not any(level == gene.output_layer for level in group.keys()):

# 			group[gene.output_layer] = [{ "ID": gene.output_node,
# 										  "connections":  [(gene.input_node, gene.input_layer)] }]

# 		else:

# 			# neuron = next((ID for ID, _ in enumerate(group[gene.output_layer]) if ID == gene.output_node), None)
# 			neuron = next((ID["ID"] for ID in group[gene.output_layer] if ID["ID"] == gene.output_node), None)

# 			if neuron is not None:

# 				neuron["connections"].append((gene.input_node, gene.input_layer))

# 			else:

# 				group[gene.output_layer].append({ "ID": gene.output_node,
# 												  "connections":  [(gene.input_node, gene.input_layer)] })



# 	group = { index: group[key] for index, key in enumerate(sorted(group)) }
# 	# group = { index: list(set(group[key])) for index, key in enumerate(sorted(group)) }
# 	# last = list(group.keys())[-1]
# 	# duplicates = {}

# 	for index, key in enumerate(sorted(group)):

# 		# group[index] = group.pop(key)
# 		mapping[key] = index

# 		# for node in group[index]["connections"]:

# 		# 	if (node[1] == key):

# 		# 		node[1] = index

# 	# for key, element in group.items():
# 	# for _, element in group.items():
# 	for element in group.values():

# 		for node in element["connections"]:

# 			node[1] = mapping[node[1]]

# 	for layer, nodes in group.items():

# 		if (layer > 0):

# 			for node in nodes:

# 			    if (layer < len(group) - 1):

# 					if any(neuron[1] >= layer for neuron in node["connections"]):
# 					# if (any(neuron[1] >= layer for neuron in node["connections"]) and
# 					#     (layer < len(group) - 1)):

# 						if not any(neuron["ID"] == node["ID"] for vertex in list(group.values())[layer + 1:] for neuron in vertex):

# 							# if not any(node["ID"] in neuron for _, neuron in connections.items()):
# 							if not any(node["ID"] in neuron for neuron in connections.values()):

# 								connections[layer] = [-node["ID"]]

# 							else:

# 								connections[layer].append(-node["ID"])

# 				else:

# 					# if not any(node["ID"] in neuron for _, neuron in connections.items()):
# 					if not any(node["ID"] in neuron for neuron in connections.values()):

# 						connections[layer] = [node["ID"]]

# 					else:

# 						connections[layer].append(node["ID"])

# 		else:

# 			for node in nodes:

# 				# if not any(node["ID"] in neuron for _, neuron in connections.items()):
# 				if not any(node["ID"] in neuron for neuron in connections.values()):

# 					connections[layer] = [node["ID"]]

# 				else:

# 					connections[layer].append(node["ID"])



# 	# for layer, nodes in group.items():

# 	# 	# nodes = list(set(nodes))

# 	# 	if ((layer < last) and
# 	# 		(layer > 0)):

# 	# 		for node in nodes:

# 	# 			# clones = [neuron for _, nodes in dict(list(group.items())[layer + 1:]).items() for neuron in nodes if (neuron == node)]
# 	# 			# clones = [neuron for nodes in list(group.values())[layer + 1:] for neuron in nodes if (neuron == node)]
# 	# 			layers = [depth for depth in list(group)[layer + 1:] for neuron in list(group.values())[layer + 1:][depth] if (neuron == node)]

# 	# 			if (len(layers) > 1):

# 	# 				duplicates[node] = layers

# 	# network.layers = max(dna.layer for dna in network.neurons) + 1


# 	for layer in connections:

# 		for node in layer:

# 			if (node < 0):
		
# 				for ID in reversed(group):











# 	network.layers = len(connections)
# 	network.network = [tuple()]*network.layers

# 	# for node in network.neurons:
# 	for node in connections:

# 		network.network[node.layer] += (node, )
# 		# network.network[node.layer] = sorted(network.network[node.layer], key = lambda dna: (dna.node < 0, dna.node))
# 		network.network[node.layer] = sorted(network.network[node.layer], key = lambda dna: dna.node)
# 		# network.network[node.layer] = sorted(network.network[node.layer], key = lambda dna: (dna.node_type != "bias", dna.node))

# 	return network


def decodeGenome(genome, architecture):

	# network = Network(architecture, generate = False)
	connections = {}
	mapping = {}
	group = {}
	duplicates = []
	replacements = []

	# for gene in genome:

	# 	if (gene.input_layer == 0):

	# 		# if (gene.input_layer not in group.keys()):

	# 		if ((gene.input_layer, gene.id) not in group.keys()):

	# 			# group[gene.input_layer] = [gene.input_neuron]

	# 			group[(gene.input_layer, gene.id)] = [gene.input_neuron]

	# 		else:

	# 			# if (gene.input_neuron not in group[gene.input_layer]):
	# 			# if not any(gene.input_node == node.node for node in group[gene.input_layer]):

	# 			if (gene.input_neuron not in group[(gene.input_layer, gene.id)]):
	# 			# if not any(gene.input_node == node.node for node in group[(gene.input_layer, gene.id)]):

	# 				# group[gene.input_layer] = [gene.input_neuron]

	# 				group[(gene.input_layer, gene.id)] = [gene.input_neuron]

	# 			else:

	# 				# group[gene.input_layer].append(gene.input_neuron)

	# 				group[(gene.input_layer, gene.id)].append(gene.input_neuron)

	# 	# if (gene.output_layer not in group.keys()):

	# 	if ((gene.output_layer, gene.id) not in group.keys()):

	# 		# group[gene.output_layer] = [gene.output_neuron]

	# 		group[(gene.output_layer, gene.id)] = [gene.output_neuron]

	# 	else:

	# 		# if (gene.output_neuron not in group[gene.output_layer]):

	# 		if (gene.output_neuron not in group[(gene.output_layer, gene.id)]):

	# 			# group[gene.output_layer] = [gene.output_neuron]

	# 			group[(gene.output_layer, gene.id)] = [gene.output_neuron]

	# 		else:

	# 			# group[gene.output_layer].append(gene.output_neuron)

	# 			group[(gene.output_layer, gene.id)].append(gene.output_neuron)

	# for gene in genome:

	# 	if ((gene.input_layer, gene.id) not in group.keys()):

	# 		group[(gene.input_layer, gene.id)] = [gene.input_neuron]

	# 	else:

	# 		if (gene.input_neuron not in group[(gene.input_layer, gene.id)]):

	# 			group[(gene.input_layer, gene.id)] = [gene.input_neuron]

	# 		else:

	# 			group[(gene.input_layer, gene.id)].append(gene.input_neuron)

	# 	if ((gene.output_layer, gene.id) not in group.keys()):

	# 		group[(gene.output_layer, gene.id)] = [gene.output_neuron]

	# 	else:

	# 		if (gene.output_neuron not in group[(gene.output_layer, gene.id)]):

	# 			group[(gene.output_layer, gene.id)] = [gene.output_neuron]

	# 		else:

	# 			group[(gene.output_layer, gene.id)].append(gene.output_neuron)

	# 	group_a = { index: group[key] for index, key in enumerate(sorted(group, key = lambda layer: layer[0])) if key[1] == next(iter(group.keys()))[1] }
	# 	group_b = { index: group[key] for index, key in enumerate(sorted(group, key = lambda layer: layer[0])) if key[1] != next(iter(group.keys()))[1] }
	# 	group = { index: group_a.get(key, []) + group_b.get(key, []) for key in set(group_a.keys()) | set(group_b) }
	for gene in genome:

		if (gene.input_layer not in group.keys()):

			# group[gene.input_layer] = [gene.input_neuron]
			group[gene.input_layer] = [copy.deepcopy(gene.input_neuron)]

		else:

			if (gene.input_neuron not in group[gene.input_layer]):

				# group[gene.input_layer] = [gene.input_neuron]
				group[gene.input_layer] = [copy.deepcopy(gene.input_neuron)]

			else:

				# group[gene.input_layer].append(gene.input_neuron)
				group[gene.input_layer].append(copy.deepcopy(gene.input_neuron))

		if (gene.output_layer not in group.keys()):

			# group[gene.output_layer] = [gene.output_neuron]
			group[gene.output_layer] = [copy.deepcopy(gene.output_neuron)]

		else:

			if (gene.output_neuron not in group[gene.output_layer]):

				# group[gene.output_layer] = [gene.output_neuron]
				group[gene.output_layer] = [copy.deepcopy(gene.output_neuron)]

			else:

				# group[gene.output_layer].append(gene.output_neuron)
				group[gene.output_layer].append(copy.deepcopy(gene.output_neuron))

	offset = min(group.keys())
	final = max(group.keys())
	group = { index: group[key] for index, key in enumerate(sorted(group)) }

	for layer, nodes in group.items():

		for node in nodes:

			if (node.layer >= offset):

				node.layer -= (offset - 1)

				for link in node.branches:

					link.output_layer -= (offset - 1)

				for link in node.paths:

					link.input_layer -= (offset - 1)

	for layer, nodes in reversed(group.items()):

		for node in nodes:

			# if (node.node not in duplicates):
			if not any(node.node == neurons[0] for neurons in duplicates):

				buffer = [neuron for neurons in list(group.values()) for neuron in neurons if (neuron.node == node.node)]
				# if any(neuron.node == node.node for neurons in list(group.values())[layer + 1:] for neuron in neurons):

				if (len(buffer) > 0):

					# duplicates.append(node.node)
					last = max(neuron.layer for neuron in buffer)

					if all(link.input_layer < last for neuron in buffer for link in neuron.branches):

						# duplicates.append((node.node, last))
						duplicates.append((node.node, node, last))

						for link in node.branches:

							link.output_layer = last

						for link in node.paths:

							link.input_layer = last

					else:

						# if (node.node < final):

						# 	duplicates.append((node.node, last + 1))

						# else:

						# 	duplicates.append((node.node, last + 1))
						# 	final += 1

						# duplicates.append((node.node, last + 1))
						duplicates.append((node.node, node, last + 1))

						for link in node.branches:

							link.output_layer = last + 1

						for link in node.paths:

							link.input_layer = last + 1

						# if (node.node >= final):

						# 		final += 1

					# for neuron in buffer:

					# 	for weights in neuron.branches:

			else:

				replacements.append(node)
				group[node.layer].remove(node)

	for clone in duplicates:

		if (clone[1].layer != clone[2]):

			if (clone[2] >= final):

				# group[clone[2] + 1] = group[clone[2]][:]
				# group[final + 1] = group[clone[2]][:]
				final += 1
				group[final] = group[clone[2]][:]
				group[clone[2]] = []
				# group[clone[2]] = [neuron for neuron in group[clone[2]] if not any(neuron.node == node.node for node in group[final])]

				# for node in group[final + 1]:
				for node in group[final]:

					for link in node.branches:

						# link.output_layer = final + 1
						link.output_layer = final

					# for link in node.paths:

					# 	link.input_layer = final + 1

				# final += 1

			group[clone[1].layer].remove(clone[1])
			group[clone[2]].append(clone[1])
			clone[1].layer = clone[2]

		elif (any(link.output_layer == clone[2] for link in clone[1].paths) or
			  any(link.intput_layer == clone[2] for link in clone[1].branches)):

			

		# # elif (any(link.output_layer == clone[2] for link in clone[1].paths) or
		# if (any(link.output_layer == clone[2] for link in clone[1].paths) or
		# 	# any(link.intput_layer == clone[2] for link in clone[1].branches)):
		# 	any(link.intput_layer == clone[2] for link in clone[1].branches) or
		#     any(link.output_layer == clone[2] for links in group[clone[2]] for link in links.paths) or
		#     # any(link.input_layer == clone[2] for links in group[clone[2]] for link in links.branches)):
		#     any(node.layer == clone[2] for node in group[clone[2]]) or
		#     any(link.input_layer == clone[2] for links in group[clone[2]] for link in links.branches)):
		# 	  # any(link.output_layer == clone[2] for links in group[clone[2]] for link in links.paths) or
		# 	  # any(link.input_layer == clone[2] for links in group[clone[2]] for link in links.branches)):

		# # elif any(in replacements):








	for gene in genome:

		input_neuron = Node(node = gene.input_node,
						    layer = gene.input_layer,
						    branches = [],
						    function = gene.input_neuron.function,
						    activity = 1 if (gene.input_neuron.node_type == "bias") else 0,
						    output = 1 if (gene.input_neuron.node_type == "bias") else 0,
						    node_type = gene.input_neuron.node_type)

		output_neuron = Node(node = gene.output_node,
						     layer = gene.output_layer,
						     branches = [],
						     function = gene.output_neuron.function,
						     activity = 1 if (gene.output_neuron.node_type == "bias") else 0,
						     output = 1 if (gene.output_neuron.node_type == "bias") else 0,
						     node_type = gene.output_neuron.node_type)

		synapse = Branch(weight = gene.weight,
						 input_node = gene.input_node,
						 output_node = gene.output_node,
						 input_neuron = input_neuron,
						 output_neuron = output_neuron,
						 input_layer = input_neuron.layer,
						 output_layer = output_neuron.layer,
						 active = gene.active,
						 branch_type = gene.branch_type,
						 recurrent = gene.recurrent,
						 skip = gene.skip,
						 innovation = gene.innovation)

		# if not any(level == gene.input_layer for level, _ in group.items()):
		if not any(level == gene.input_layer for level in group.keys()):

			# group[gene.input_layer] = [{ "ID": gene.input_node, "connections":  [(gene.output_node, gene.output_layer)] }]
			group[gene.input_layer] = [{ "ID": gene.input_node,
										 "connections":  [] }]

		else:

			# neuron = next((ID for ID, _ in group[gene.input_layer] if ID == gene.input_node), None)

			# if neuron is not None:

			# 	neuron["connections"].append((gene.output_node, gene.output_layer))

			# else:

				# group[gene.input_layer].append({ "ID": gene.input_node, "connections":  [(gene.output_node, gene.output_layer)] })
			group[gene.input_layer].append({ "ID": gene.input_node,
											 "connections":  [] })

		# if not any(level == gene.output_layer for level, _ in group.items()):
		if not any(level == gene.output_layer for level in group.keys()):

			group[gene.output_layer] = [{ "ID": gene.output_node,
										  "connections":  [(gene.input_node, gene.input_layer)] }]

		else:

			# neuron = next((ID for ID, _ in enumerate(group[gene.output_layer]) if ID == gene.output_node), None)
			neuron = next((ID["ID"] for ID in group[gene.output_layer] if ID["ID"] == gene.output_node), None)

			if neuron is not None:

				neuron["connections"].append((gene.input_node, gene.input_layer))

			else:

				group[gene.output_layer].append({ "ID": gene.output_node,
												  "connections":  [(gene.input_node, gene.input_layer)] })



	group = { index: group[key] for index, key in enumerate(sorted(group)) }
	# group = { index: list(set(group[key])) for index, key in enumerate(sorted(group)) }
	# last = list(group.keys())[-1]
	# duplicates = {}

	for index, key in enumerate(sorted(group)):

		# group[index] = group.pop(key)
		mapping[key] = index

		# for node in group[index]["connections"]:

		# 	if (node[1] == key):

		# 		node[1] = index

	# for key, element in group.items():
	# for _, element in group.items():
	for element in group.values():

		for node in element["connections"]:

			node[1] = mapping[node[1]]

	for layer, nodes in group.items():

		if (layer > 0):

			for node in nodes:

			    if (layer < len(group) - 1):

					if any(neuron[1] >= layer for neuron in node["connections"]):
					# if (any(neuron[1] >= layer for neuron in node["connections"]) and
					#     (layer < len(group) - 1)):

						if not any(neuron["ID"] == node["ID"] for vertex in list(group.values())[layer + 1:] for neuron in vertex):

							# if not any(node["ID"] in neuron for _, neuron in connections.items()):
							if not any(node["ID"] in neuron for neuron in connections.values()):

								connections[layer] = [-node["ID"]]

							else:

								connections[layer].append(-node["ID"])

				else:

					# if not any(node["ID"] in neuron for _, neuron in connections.items()):
					if not any(node["ID"] in neuron for neuron in connections.values()):

						connections[layer] = [node["ID"]]

					else:

						connections[layer].append(node["ID"])

		else:

			for node in nodes:

				# if not any(node["ID"] in neuron for _, neuron in connections.items()):
				if not any(node["ID"] in neuron for neuron in connections.values()):

					connections[layer] = [node["ID"]]

				else:

					connections[layer].append(node["ID"])



	# for layer, nodes in group.items():

	# 	# nodes = list(set(nodes))

	# 	if ((layer < last) and
	# 		(layer > 0)):

	# 		for node in nodes:

	# 			# clones = [neuron for _, nodes in dict(list(group.items())[layer + 1:]).items() for neuron in nodes if (neuron == node)]
	# 			# clones = [neuron for nodes in list(group.values())[layer + 1:] for neuron in nodes if (neuron == node)]
	# 			layers = [depth for depth in list(group)[layer + 1:] for neuron in list(group.values())[layer + 1:][depth] if (neuron == node)]

	# 			if (len(layers) > 1):

	# 				duplicates[node] = layers

	# network.layers = max(dna.layer for dna in network.neurons) + 1


	for layer in connections:

		for node in layer:

			if (node < 0):
		
				for ID in reversed(group):











	network.layers = len(connections)
	network.network = [tuple()]*network.layers

	# for node in network.neurons:
	for node in connections:

		network.network[node.layer] += (node, )
		# network.network[node.layer] = sorted(network.network[node.layer], key = lambda dna: (dna.node < 0, dna.node))
		network.network[node.layer] = sorted(network.network[node.layer], key = lambda dna: dna.node)
		# network.network[node.layer] = sorted(network.network[node.layer], key = lambda dna: (dna.node_type != "bias", dna.node))

	return network

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

	# for a in genome_a:
	for a in genome_a["dna"]:

		if all(((b.innovation != a.innovation) and
				((a.innovation < maximum_b) if (region == "interior") else
				 (a.innovation > maximum_b))) for b in genome_b):

			# unpaired.append(a)
			unpaired.append((a, genome_a["net"]))

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
