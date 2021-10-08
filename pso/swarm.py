from typing import List, Callable

from tqdm import tqdm
import numpy as np

from pso.particle import Particle


class Swarm:
    """
    Class that implements the Swarm
    """
    def __init__(self,
                 alpha: float,
                 beta: float,
                 gamma: float,
                 delta: float,
                 epsilon: float,
                 lower_limit: float = 90.0,
                 upper_limit: float = 100.0,
                 dimension: int = 2):
        """
        :param lower_limit: The lower limit of the random selection
        interval of the starting position
        :param upper_limit: The upper limit of the random selection
        interval of the starting position
        :param fitness_fun: Fitness function
        :param dimension: Dimension of the problem
        """
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.delta = delta
        self.epsilon = epsilon
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.dimension = dimension

        self.global_position_best = None
        self.global_position_best_fitness = np.inf

        self.animation_particle_information = dict()

    def _calculate_global_position_best(self, particles: List[Particle]):
        fitness_arr = [p.get_individual_position_fitness() for p in particles]
        min_index = np.argmin(fitness_arr)

        if fitness_arr[min_index] < self.global_position_best_fitness:
            self.global_position_best_fitness = fitness_arr[min_index]
            self.global_position_best = particles[min_index].get_individual_position()

    @staticmethod
    def _get_informants(p_id: int, particles: List[Particle], n_informants: int) -> List[Particle]:
        particles_informants = particles[:]
        particles_informants.pop(p_id)
        informants = np.random.choice(particles, size=n_informants, replace=False)
        return informants

    def _create_animation_data_collector(self, particles: List[Particle]):
        for p_id, p in enumerate(particles):
            self.animation_particle_information[str(p_id)] = [[p.get_individual_position().copy(),
                                                               p.get_individual_position_fitness()]]

    def _add_animation_position(self, p_id: int, particle: Particle):
        self.animation_particle_information[str(p_id)].append([particle.get_individual_position().copy(),
                                                              particle.get_individual_position_fitness()])

    def get_animation_data_collector(self):
        return self.animation_particle_information

    def get_global_position_best(self):
        return self.global_position_best

    def run(self, max_iter: int, fitness_fun: Callable, n_particles: int, n_informants: int):

        data = {
            "fitness_fun": fitness_fun,
            "alpha": self.alpha,
            "beta": self.beta,
            "gamma": self.gamma,
            "delta": self.delta,
            "epsilon": self.epsilon,
            "lower_limit": self.lower_limit,
            "upper_limit": self.upper_limit,
            "dimension": self.dimension
        }

        particles = [Particle.from_dict(data) for _ in range(n_particles)]
        self._create_animation_data_collector(particles)

        for _ in tqdm(range(max_iter)):
            # 1. We assess the best position of the swarm
            self._calculate_global_position_best(particles)

            # 2. Iterate for each particle
            for p_id, p in enumerate(particles):

                # 2.2 We select informants for each particle
                informants = self._get_informants(p_id, particles, n_informants)

                # 2.2 Update particle position and velocity
                p.update_position_velocity(informants, self.get_global_position_best())

                # 2.1 Gather particle information for visualization
                self._add_animation_position(p_id, p)
