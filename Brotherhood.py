# SOURCE: https://github.com/loureirod/Ant-colony-optimization
import numpy as np

from Robber import Robber


class Brotherhood:
    def __init__(
        self,
        graph: np.ndarray,
        budget: int,
        treasures: list,
        number_robbers: int,
        evaporation_rate: float,
        alpha: float,
        randomness_rate: float,
        gamma_parameters: dict
    ):
        self.graph = np.copy(graph)  # Matrix of distances between node i and j
        self.budget = budget
        self.treasures = treasures
        self.number_robbers = number_robbers
        self.evaporation_rate = evaporation_rate
        self.generation_counter = 0
        self.alpha = alpha
        self.randomness_rate = np.random.uniform(0, randomness_rate)
        self.gamma_parameters = gamma_parameters
        self.hall_of_fame = [0, [0]]  # treasures obtained, best_path nodes

        self.initialize_robber_population()

    def initialize_robber_population(self):
        self.population = []
        # Matrix of shared_xp level between node i and j
        self.shared_xp = np.zeros_like(self.graph)

        for k in range(self.number_robbers):
            self.population.append(Robber(
                self.alpha,
                self.randomness_rate,
                self.budget,
                self.gamma_parameters
            ))

    def evaporate(self):
        """
        Shared_XP fade away with time as experiences cannot
        be shared exactly between old robbers and newcomers
        """
        self.shared_xp = (1 - self.evaporation_rate) * self.shared_xp

    def generation(self):
        """
        A generation passes as all the robber within the brotherhood
        try their luck to gather the maximum treasures.
        But those robbers are smart and don't want a robber-less future!
        Therefore, they will share their experiences by leaving hints
        along the path they took.
        The bigger their treasure, the bigger the hints!
        """
        self.evaporate()

        for robber in self.population:
            robber.rob_banks(self.shared_xp, self.graph, self.treasures)

        for robber in self.population:
            # Share experience with the brotherhood
            robber.share_experiences(self.shared_xp)

            # Access Hall of Fame !
            if robber.total_treasure > self.hall_of_fame[0]:
                self.hall_of_fame = [
                    robber.total_treasure,
                    robber.visited_banks
                ]

            robber.is_replaced_by_youngster()

    def greedy_path(self):
        """
        Follow current shared experiences to create a greedy path.
        Best path is determined by choosing the road with
        max
        """
        greedy_robber = Robber(
            self.alpha,
            self.randomness_rate,
            self.budget,
            self.gamma_parameters
        )
        greedy_robber.rob_banks(self.shared_xp, self.graph, self.treasures)
        return greedy_robber.total_treasure, greedy_robber.visited_banks
