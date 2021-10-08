import numpy as np


def paraboloid(point: np.ndarray) -> float:
    return float(np.sum(point**2))


def paraboloid_plot(n: int):
    x1 = np.linspace(-10, 10, n)
    x2 = x1.copy()
    x3 = np.zeros(shape=(x1.shape[0], x2.shape[0]))

    for i, a1 in enumerate(x1):
        for j, a2 in enumerate(x2):
            params = np.array([a2, a1])
            x3[i, j] = paraboloid(params)

    return x1, x2, x3

