"""
The Ramer-Douglas-Peucker algorithm roughly ported from the pseudo-code provided
by http://en.wikipedia.org/wiki/Ramer-Douglas-Peucker_algorithm
copy from https://github.com/sebleier/RDP/blob/master/__init__.py
"""

from math import sqrt


def distance(a, b):
    return  sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def point_line_distance(point, start, end):
    if (start == end):
        return distance(point, start)
    else:
        n = abs(
            (end[0] - start[0]) * (start[1] - point[1]) -
            (start[0] - point[0]) * (end[1] - start[1])
        )
        d = sqrt(
            (end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2
        )
        return n / d


def rdp(points, epsilon):
    """Reduces a series of points to a simplified version that loses detail, but
    maintains the general shape of the series.
    """
    dmax = 0.0
    index = 0
    for i in range(1, len(points) - 1):
        d = point_line_distance(points[i], points[0], points[-1])
        if d > dmax:
            index = i
            dmax = d

    if dmax >= epsilon:
        results = rdp(points[:index+1], epsilon)[:-1] + rdp(points[index:], epsilon)
    else:
        results = [points[0], points[-1]]

    return results

# Demo. copy from https://stackoverflow.com/questions/14631776/calculate-turning-points-pivot-points-in-trajectory-path

import matplotlib.pyplot as plt
import numpy as np
import os

def angle(dir):
    """
    Returns the angles between vectors.

    Parameters:
    dir is a 2D-array of shape (N,M) representing N vectors in M-dimensional space.

    The return value is a 1D-array of values of shape (N-1,), with each value
    between 0 and pi.

    0 implies the vectors point in the same direction
    pi/2 implies the vectors are orthogonal
    pi implies the vectors point in opposite directions
    """
    dir2 = dir[1:]
    dir1 = dir[:-1]
    return np.arccos((dir1*dir2).sum(axis=1)/(
        np.sqrt((dir1**2).sum(axis=1)*(dir2**2).sum(axis=1))))
if __name__ == '__main__':
    tolerance = 1
    min_angle = np.pi*0.005
    from source.util import load_json
    # points = load_json(all_path=filename)['position_list']
    # points = [i['position'] for i in points]
    S = [[-1004.39, -2406.393], [-1002.3100000000001, -2406.122], [-983.422, -2468.528], [-980.354, -2473.13], [-918.219, -2512.508], [-912.338, -2513.787], [-907.479, -2510.207], [-901.087, -2508.673], [-895.206, -2506.627], [-890.347, -2503.047], [-872.448, -2480.546], [-862.732, -2477.989], [-845.6, -2478.5], [-803.921, -2489.24], [-796.506, -2493.075], [-788.834, -2497.422], [-766.077, -2498.445], [-709.056, -2518.389], [-701.385, -2521.713], [-681.696, -2532.197], [-674.025, -2551.119], [-668.656, -2556.744], [-662.774, -2557.0], [-654.848, -2557.767], [-613.936, -2565.182], [-606.265, -2567.739], [-599.872, -2569.529], [-592.201, -2568.762], [-577.115, -2554.443], [-571.745, -2554.699], [-565.097, -2558.278], [-553.335, -2566.461], [-550.011, -2571.319], [-539.016, -2576.178], [-530.578, -2576.945], [-524.696, -2576.178], [-506.286, -2572.086]]
    points = [[2621.692, -4826.849], [2619.391, -4833.497], [2617.09, -4838.611], [2610.953, -4849.095], [2604.816, -4860.09], [2597.401, -4872.363], [2594.332, -4876.71], [2590.497, -4882.08], [2582.314, -4895.121], [2575.155, -4902.28], [2565.182, -4910.718], [2561.603, -4914.554], [2558.023, -4918.901], [2555.722, -4923.759], [2555.21, -4929.64], [2555.466, -4936.8], [2556.489, -4943.192], [2557.511, -4954.443], [2557.767, -4962.114], [2557.511, -4968.251], [2560.5, -4996.5], [2557.0, -5001.492], [2558.023, -5007.117], [2563.392, -5006.606], [2565.182, -5000.469], [2566.5, -4994.25], [2570.808, -5001.492], [2578.99, -5002.259], [2586.661, -4998.679], [2592.031, -4998.168], [2598.935, -5000.981], [2605.072, -5006.095], [2611.976, -5011.209], [2617.601, -5014.277], [2624.505, -5018.112], [2631.92, -5021.692], [2637.545, -5024.249], [2645.728, -5027.318], [2653.655, -5030.13], [2666.25, -5030.25], [2662.348, -5033.966], [2669.508, -5033.71], [2674.5, -5034.0], [2678.202, -5039.336], [2682.804, -5044.194], [2687.151, -5053.655], [2690.22, -5059.28], [2693.8, -5063.627], [2699.681, -5070.02], [2701.47, -5075.901], [2701.982, -5083.572], [2701.726, -5090.22], [2707.5, -5097.75], [2707.5, -5102.25], [2705.05, -5107.352]]
    points = S
    points = np.array(points)
    import random
    random.randint
    print(len(points))
    x, y = points.T

    # Use the Ramer-Douglas-Peucker algorithm to simplify the path
    # http://en.wikipedia.org/wiki/Ramer-Douglas-Peucker_algorithm
    # Python implementation: https://github.com/sebleier/RDP/
    simplified = np.array(rdp(points.tolist(), tolerance))

    print(len(simplified))
    sx, sy = simplified.T

    # compute the direction vectors on the simplified curve
    directions = np.diff(simplified, axis=0)
    theta = angle(directions)
    # Select the index of the points with the greatest theta
    # Large theta is associated with greatest change in direction.
    idx = np.where(theta>min_angle)[0]+1

    fig = plt.figure()
    ax =fig.add_subplot(111)

    ax.plot(x, y, 'b-', label='original path')
    ax.plot(sx, sy, 'g--', label='simplified path')
    ax.plot(sx[idx], sy[idx], 'ro', markersize = 10, label='turning points')
    ax.invert_yaxis()
    plt.legend(loc='best')
    plt.show()
    print()