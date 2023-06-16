import utility


if __name__ == "__main__":

	function = lambda x: x**2 - 3
	chromosome_length = 1
	population_size = 10
	generations = 5
	category = "number"
	genotype = "base"
	mutation_rate = 0.5 / 100
	loop = False
	display = False
	objective = "minimize"
	task = "search"

	domain = { "minimum": -1e12,
    		   "maximum": 1e12 }

	horizon = { "window": generations // 2,
				"tolerance": 1e-12 }

	natural_selection = { "function": utility.tournamentSelection,
						  "arguments": { "size": population_size // 2,
						  				 "objective": objective,
						  				 "chromosome_length": chromosome_length } }

	pairing = { "function": None,
				"arguments": None }

	combination = { "function": utility.heuristicAverage,
					"arguments": { "objective": objective } }

	mutation = { "function": utility.randomMutation,
				 "arguments": { "mutation_number": 1,
				 				"chromosome_length": 1 } }

	parameters = { "population_size": population_size,
				   "function": function,
				   "category": category,
				   "genotype": genotype,
				   "chromosome_length": chromosome_length,
				   "mutation_rate": mutation_rate,
				   "funnel": natural_selection,
				   "pairing": pairing,
				   "combination": combination,
				   "mutator": mutation,
				   "task": task,
				   "objective": objective,
				   "loop": loop,
				   "domain": domain,
				   "horizon": horizon,
				   "generations": generations,
				   "display": display }

	alpha, iterations, initial = utility.evolve(parameters)
	if (not(loop) and (iterations < generations)): print(f"\nSUMMARY OF RESULTS:\nsolution: {alpha['chromosome']}\nnumber of iterations: {iterations}\noptimum fitness: {alpha['fitness']}\n")
	elif (iterations < generations): print(f"\nSUMMARY OF RESULTS:\nsolution: {alpha['chromosome']}\nnumber of iterations: {iterations}\noptimum fitness: {alpha['fitness']}\n")
	else: print(f"ALGORITHM TERMINATED EARLY WITH THE FOLLOWING SOLUTION:\nsolution: {alpha['chromosome']}\noptimum fitness: {alpha['fitness']}\n")
