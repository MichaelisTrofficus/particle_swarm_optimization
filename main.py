from utils.functions import paraboloid
from pso.swarm import Swarm


s = Swarm(alpha=0.5, beta=0.7, gamma=0.5, delta=0, epsilon=1)

s.run(max_iter=100, fitness_fun=paraboloid, n_particles=20, n_informants=4)
