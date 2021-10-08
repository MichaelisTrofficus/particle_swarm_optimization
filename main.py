import plotly.graph_objects as go

from utils.functions import paraboloid
from pso.swarm import Swarm

from utils.functions import paraboloid_plot
from utils.animation import get_frames

ALPHA = 0.7
BETA = 0.6
GAMMA = 0.9
DELTA = 0.0
EPSILON = 1.0
MAX_ITER = 200
N_PARTICLES = 75
N_INFORMANTS = 30
DIMENSION = 2

s = Swarm(alpha=ALPHA, beta=BETA, gamma=GAMMA, delta=DELTA, epsilon=EPSILON, dimension=DIMENSION, upper_limit=7.5,
          lower_limit=5.5)
s.run(max_iter=MAX_ITER, fitness_fun=paraboloid, n_particles=N_PARTICLES, n_informants=N_INFORMANTS)

animation_data_collector = s.get_animation_data_collector()

if DIMENSION == 2:

    xyz = paraboloid_plot(100)

    color_grey = "grey"

    fig = go.Figure(
        data=[go.Surface(
            x=xyz[0],
            y=xyz[1],
            z=xyz[2],
            colorscale=[[0, color_grey], [1, color_grey]],
            opacity=0.5,
            showscale=False)] * (N_PARTICLES + 1)
    )

    frames = get_frames(animation_data_collector)

    fig.update(frames=frames)
    fig.update_layout(
        updatemenus=[dict(type='buttons',
                          buttons=[dict(label='Play',
                                        method='animate',
                                        args=[None,
                                              dict(frame=dict(redraw=True,
                                                              fromcurrent=True,
                                                              mode="inmediate",
                                                              duration=300))])],
                          ),
                     ]
    )

    fig.show()
