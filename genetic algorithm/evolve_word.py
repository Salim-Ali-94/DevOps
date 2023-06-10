import utility


if __name__ == "__main__":

	target = "cat"
	chromosome_length = len(target)
	population_size = 10*chromosome_length
	fitness = utility.wordScore
	category = "character"
	genotype = "base"
	mutation_rate = 0.5 / 100
	loop = True
	generations = 5
	display = False
	task = "evolve"
	objective = "maximize"

	natural_selection = { "function": utility.tournamentSelection,
						  "arguments": { "size": population_size // 10,
						  				 "objective": objective,
						  				 "chromosome_length": chromosome_length } }

	pairing = { "function": utility.symbolMatching,
				"arguments": { "group_size": 2,
				 			   "strategy": "random",
				 			   "chaos": False } }

	combination = { "function": utility.pointCrossOver,
					"arguments": None }

	mutation = { "function": utility.randomMutation,
				 "arguments": { "mutation_number": 1 } }

	parameters = { "population_size": population_size,
				   "function": fitness,
				   "category": category,
				   "genotype": genotype,
				   "chromosome_length": chromosome_length,
				   "mutation_rate": mutation_rate,
				   "funnel": natural_selection,
				   "pairing": pairing,
				   "combination": combination,
				   "mutator": mutation,
				   "task": task,
				   "target": target,
				   "objective": objective,
				   "loop": loop,
				   "generations": generations,
				   "display": display }

	alpha, iterations, initial = utility.evolve(parameters)
	if (alpha["chromosome"] == target): print(f"\nEvolved '{ initial['chromosome'] }' to '{ alpha['chromosome'] }' in { iterations } generation(s) with a fitness score of { alpha['fitness'] }\n")
	else: print("ALGORITHM FAILED TO CONVERGE TO A SOLUTION")
