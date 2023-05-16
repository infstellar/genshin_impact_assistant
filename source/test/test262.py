from source.util import *

def get_path_file(path_file_name:str):
    return load_json(path_file_name+".json","assets\\TeyvatMovePath")

import numpy as np
from scipy.interpolate import splprep, splev

def fit_curve(points):
    points = np.array(points)
    tck, u = splprep(points.T, u=None, s=0.0)
    u_new = np.linspace(u.min(), u.max(), 1000)
    x_new, y_new, z_new = splev(u_new, tck)
    return x_new, y_new, z_new, tck

# points = [(1, 1, 1), (2, 2, 2), (3, 3, 3), (4,4,4)]
points = []
bps = get_path_file('GlazeLily20230513214422i0')
for i in bps['break_position']:
    points.append([i[0], -i[1], bps['break_position'].index(i)])
x_new, y_new, z_new, tck = fit_curve(points)
print()

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x_new, y_new, z_new)
plt.show()

print()

def nearest_point(x, y, z, x_new, y_new, z_new):
    distances = (x_new - x)**2 + (y_new - y)**2 + (z_new - z)**2
    min_index = np.argmin(distances)
    return x_new[min_index], y_new[min_index], z_new[min_index]

x, y, z = 1.2, 1.2, 1.2
nearest_x, nearest_y, nearest_z = nearest_point(x, y, z, x_new, y_new, z_new)

dxdu, dydu, dzdu = splev(0.5, tck, der=1)

print()
