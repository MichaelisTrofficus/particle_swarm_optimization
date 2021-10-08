from __future__ import annotations
from typing import Tuple, List, Callable, Dict

import numpy as np


class Particle:
    """
    Class that implements a Particle / Candidate Solution
    """
    def __init__(self,
                 fitness_fun: Callable,
                 alpha: float,
                 beta: float,
                 gamma: float,
                 delta: float,
                 epsilon: float,
                 lower_limit: float,
                 upper_limit: float,
                 dimension: int = 3):
        """
        :param lower_limit: The lower limit of the random selection
        interval of the starting position
        :param upper_limit: The upper limit of the random selection
        interval of the starting position
        :param fitness_fun: Fitness function
        :param dimension: Dimension of the problem
        """
        self.fitness_fun = fitness_fun
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.delta = delta
        self.epsilon = epsilon
        self.dimension = dimension

        self.individual_position, self.velocity = self._get_initial_pos_vel(lower_limit, upper_limit, dimension)
        self.individual_position_best = self.individual_position.copy()
        self.individual_position_fitness = self.fitness_fun(self.individual_position)
        self.individual_position_best_fitness = self.individual_position_fitness

    @classmethod
    def from_dict(cls, data: Dict) -> 'Particle':
        return cls(fitness_fun=data.get("fitness_fun"),
                   alpha=data.get("alpha"),
                   beta=data.get("beta"),
                   gamma=data.get("gamma"),
                   delta=data.get("delta"),
                   epsilon=data.get("epsilon"),
                   lower_limit=data.get("lower_limit"),
                   upper_limit=data.get("upper_limit"),
                   dimension=data.get("dimension")
                   )

    @staticmethod
    def _get_initial_pos_vel(lower_limit: float, upper_limit: float, dimension: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        :param lower_limit: The lower limit of the random selection
        interval of the starting position
        :param upper_limit: The upper limit of the random selection
        interval of the starting position
        :param dimension: Dimension of the problem
        """
        vel_limit = np.abs(upper_limit - lower_limit)
        individual_position = np.random.uniform(low=lower_limit, high=upper_limit, size=dimension)
        velocity = np.random.uniform(low=-vel_limit, high=vel_limit, size=dimension)
        return individual_position, velocity

    def get_individual_position(self) -> np.ndarray:
        return self.individual_position

    def get_individual_position_best(self) -> np.ndarray:
        return self.individual_position_best

    def get_individual_position_fitness(self) -> float:
        return self.fitness_fun(self.get_individual_position())

    def get_individual_position_best_fitness(self) -> float:
        return self.fitness_fun(self.get_individual_position_best())

    def get_informants_position_best(self, informants: List['Particle']):
        informants_best_position = [(p.get_individual_position_best(), p.get_individual_position_best_fitness()) for p
                                    in informants]
        informants_best_position += [(self.get_individual_position_best(), self.get_individual_position_best_fitness())]

        min_index = np.argmin([x[1] for x in informants_best_position])

        if min_index == len(informants_best_position) - 1:
            return self.get_individual_position_best()

        return informants[min_index].get_individual_position_best()

    def update_position_velocity(self, informants: List['Particle'], global_position_best: np.ndarray):

        informants_position_best = self.get_informants_position_best(informants)

        b = np.random.uniform(0.0, self.beta, size=self.dimension)
        c = np.random.uniform(0.0, self.gamma, size=self.dimension)
        d = np.random.uniform(0.0, self.delta, size=self.dimension)

        self.velocity = self.alpha*self.velocity + \
            b*(self.get_individual_position_best() - self.get_individual_position()) + \
            c*(informants_position_best - self.get_individual_position()) + \
            d*(global_position_best - self.get_individual_position())

        self.individual_position += self.epsilon*self.velocity

        if self.get_individual_position_fitness() < self.get_individual_position_best_fitness():
            self.individual_position_best = self.individual_position

