# SOURCE: https://github.com/loureirod/Ant-colony-optimization

import numpy as np

from Environment import Environment


class AntColonyGeneticOptimization:
    def __init__(
        self,
        nb_individuals: int,
        nb_robbers_max: int,
        env_iterations: int,
        genetic_iterations: int,
        crossover_rate: float,
        mutations_rate: float,
        budget: float,
        resources,
        graph
    ):
        self.nb_individuals = nb_individuals
        self.population = []  # Contains [environment, best_path lenght]
        self.env_iterations = env_iterations
        self.genetic_iterations = genetic_iterations
        self.crossover_rate = crossover_rate
        self.mutations_rate = mutations_rate
        self.budget = budget
        self.resources = resources
        self.graph = graph
        self.current_best = 0

        for k in range(nb_individuals):
            number_robbers = np.random.randint(0, nb_robbers_max)
            evaporation_rate = np.random.uniform(0, 0.1)
            alpha = np.random.uniform(0, 5)
            randomness_rate = np.random.uniform(0.05, 1)
            decision_threshold = np.random.uniform(randomness_rate, 1)

            self.population.append([
                Environment(
                    graph,
                    resources,
                    budget,
                    number_robbers,
                    evaporation_rate,
                    alpha,
                    randomness_rate,
                    decision_threshold
                ), 0
            ])

    def mutations(self):
        selected = np.random.choice(
            [ind[0] for ind in self.population],
            int(self.nb_individuals * self.mutations_rate)
        )

        def mutate(value, amplitude, positive=True):
            mutated_value = value + np.random(-amplitude, amplitude)
            if positive:
                mutated_value = max(0, mutated_value)
            return mutated_value

        for ind in selected:
            ind.number_robbers = mutate(ind.number_robbers, 10)
            ind.evaporation_rate = mutate(ind.evaporation_rate, .01)
            ind.alpha = mutate(ind.alpha, .2)
            ind.randomness_rate = min(mutate(ind.randomness_rate, .1), 1)
            ind.decision_threshold = min(mutate(ind.decision_threshold, .5), 1)

    def crossover(self):
        for k in range(int(self.nb_individuals * self.crossover_rate)):
            self.population[k] = self.reproduction(
                self.population[k][0],
                self.population[k + 1][0]
            )

    def reproduction(self, ind_1, ind_2):
        number_robbers = int(0.5 * (ind_1.number_robbers + ind_2.number_robbers))
        evaporation_rate = 0.5 * (ind_1.evaporation_rate + ind_2.evaporation_rate)
        alpha = 0.5 * (ind_1.alpha + ind_2.alpha)
        randomness_rate = 0.5 * (ind_1.randomness_rate + ind_2.randomness_rate)
        decision_threshold = 0.5 * (ind_1.decision_threshold + ind_2.decision_threshold)

        newborn = Environment(
            self.graph,
            self.resources,
            self.budget,
            number_robbers,
            evaporation_rate,
            alpha,
            randomness_rate,
            decision_threshold
        )
        return [newborn, 0]

    def evaluate(self, environment):
        environment.initialize_robber_population()
        for k in range(self.env_iterations):
            environment.step()

        return environment.best_path()[0]

    def selection(self):
        for k in range(self.nb_individuals):
            self.population[k][1] = self.evaluate(self.population[k][0])

        self.population = sorted(self.population, key=lambda x: x[1])

    def animate(self):
        for k in range(self.genetic_iterations):
            print(f"Generation: {k + 1}/ {self.genetic_iterations}")
            self.crossover()
            self.mutations()
            self.selection()

    def best_individual(self):
        return self.population[0][0]

    def print_best_individual_params(self):
        print("## Best individual parameters ##")
        print(f"Alpha: {self.current_best.alpha}")
        print(f"Randomness rate: {self.current_best.randomness_rate}")
        print(f"Decision threshold: {self.current_best.decision_threshold}")
        print(f"Number of robbers: {self.current_best.number_robbers}")
        print(f"Evaporation rate: {self.current_best.evaporation_rate}")
        print(f"Best path: {self.current_best.stored_best_path[1]}")
        print(f"Best path lenght: {self.current_best.stored_best_path[0]}")

    def compute_best_individual(self):
        self.animate()
        self.current_best = self.population[0][0]
        self.current_best.initialize_robber_population()
        self.print_best_individual_params()
        return self.current_best
