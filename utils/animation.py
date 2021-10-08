from typing import Dict

import plotly.graph_objects as go


def get_frames(animation_data_collector: Dict):

    number_iterations = len(animation_data_collector["0"])
    frames = []

    for n in range(number_iterations):
        data = []
        for _, position_fitness_arr in animation_data_collector.items():
            position_fitness = position_fitness_arr[n]
            position, fitness = position_fitness[0], position_fitness[1]
            x, y, z = [position[0]], [position[1]], [fitness]

            data.append(
                go.Scatter3d(
                    x=x,
                    y=y,
                    z=z,
                    mode="markers",
                    marker=dict(color="red", size=2, opacity=1)
                )
            )

        # data.append(
        #     go.Scatter3d(
        #         x=[3],
        #         y=[0.5],
        #         z=[0.0],
        #         mode="markers",
        #         marker=dict(color="black", size=10, opacity=1, symbol="cross")
        #     )
        # )

        frames.append(go.Frame(
            data=data
        ))

    return frames
