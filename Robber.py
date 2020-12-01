# SOURCE: https://github.com/loureirod/Ant-colony-optimization
import numpy as np


class Robber:
    def __init__(
        self,
        alpha: float,
        randomness_rate: float,
        budget: float,
        gamma_parameters: dict,
        greedy: bool = False
    ):
        self.alpha = alpha
        self.attractiveness_power = 1 + np.random.gamma(**gamma_parameters)
        self.trail_power = np.random.gamma(**gamma_parameters)
        self.randomness_rate = np.random.uniform(0, randomness_rate)
        self.initial_budget = budget
        self.greedy = greedy
        self.enter_the_brotherhood()

        if self.greedy:
            self.randomness_rate = 0.0
            self.attractiveness_power = 0.0
            self.trail_power = 1.0

    def enter_the_brotherhood(self):
        self.visited_banks = [0]
        self.budget_left = self.initial_budget
        self.is_too_old_for_this_shit = False
        self.newcomer = True  # Enables random decision at begining
        self.total_treasure = 0

    def is_replaced_by_youngster(self):
        self.enter_the_brotherhood()

    def heuristic(self, distances, treasures):
        """
        Gives a priori interest in going to each cities.
        Depends on return on investment:
        {money in bank} / {time to go their and rob it}
        """
        result = np.zeros_like(distances)
        for k, distance in enumerate(distances):
            if distance != 0:
                result[k] = treasures[k] / distance

        return result

    def rob_banks(self, shared_xp, graph, treasures):
        while not self.is_too_old_for_this_shit:
            self.move(shared_xp, graph, treasures)

    def move(self, shared_xp, graph, treasures):
        """
        Decide which road to take and memorize previous walk if nescessary
        """
        if self.is_too_old_for_this_shit:
            print("I'm too old for this shit")
            return

        bank = self.visited_banks[-1]

        # possible nodes are those "in budget"
        possibilities = np.copy(graph[bank, :])
        possibilities[possibilities > self.budget_left] = 0
        possibilities[self.visited_banks] = 0

        # If no nodes are reachable within budget, robber's job is done
        if np.nonzero(possibilities)[0].size == 0:
            self.is_too_old_for_this_shit = True
            if self.newcomer:
                raise Exception("Budget error: no reachable node at start")
            else:
                return  # I'm too old for this shit
        elif self.newcomer:
            new_bank = np.random.choice(np.nonzero(possibilities)[0])
            self.newcomer = False

        # robber is on the move, beware banks !
        # Random decision
        elif np.random.uniform(0, 1) < self.randomness_rate:
            new_bank = np.random.choice(np.nonzero(possibilities)[0])
        # Heuristic decision
        else:
            attractiveness = self.heuristic(possibilities, treasures)
            trail_level = np.copy(shared_xp[bank, :])

            # Normalize ?
            # attractiveness /= sum(attractiveness)
            # trail_level /= sum(trail_level)

            probabilities = np.power(trail_level, self.trail_power) \
                          * np.power(attractiveness, self.attractiveness_power)
            if self.greedy:
                new_bank = np.argmax(probabilities)
            else:
                Z = sum(probabilities)
                if Z < 1e-9:
                    new_bank = np.random.choice(np.nonzero(possibilities)[0])
                else:
                    probabilities /= Z
                    new_bank = np.random.choice(
                        len(probabilities),
                        p=probabilities
                    )

        self.total_treasure += treasures[new_bank]
        self.budget_left -= graph[bank, new_bank]
        self.visited_banks.append(new_bank)

    def share_experiences(self, shared_xp):
        """
        Secrete shared_xp on the road. To be called after decide
        """
        for i, bank_j in enumerate(self.visited_banks[1:]):
            bank_i = self.visited_banks[i]
            shared_xp[bank_i, bank_j] += self.alpha * self.total_treasure
