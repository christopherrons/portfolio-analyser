import numpy as np
from scipy import optimize


class QuadraticSolver:

    @staticmethod
    def solve(H: np.array, c: np.array, c0: np.array, x0: np.array, constraints: [{}], bounds: [], options: {} = {},
              sign: float = 1.0):
        loss: (np.array, float) = lambda x: sign * (np.dot(x.T, np.dot(H, x)) + np.dot(c, x) + c0.dot(np.ones(len(c0)).T))
        jacobian: (np.array, float) = lambda x: sign * (np.dot(x.T, H) + c.dot(np.ones(len(c)).T))
        result = optimize.minimize(loss, jac=jacobian, constraints=constraints, bounds=bounds,
                                   method='SLSQP', options=options, x0=x0)
        return result
