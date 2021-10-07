from typing import Tuple, List, Callable

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
                 lower_limit: float = 0.0,
                 upper_limit: float = 0.5,
                 dimension: int = 3):
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

    def _select_informants(self, p: Particle, n_informants: int) -> List[Particle]:
        pass

    def run(self, fitness_fun: Callable, n_particles: int, n_informants: int):

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



