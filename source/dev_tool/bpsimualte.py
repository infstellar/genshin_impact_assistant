from source.util import *

def get_path_file(path_file_name:str):
    return load_json(path_file_name+".json","assets\\TeyvatMovePath")

import numpy as np
from scipy import interpolate

x = np.linspace(0, 10, 10)
y = np.sin(x)
z = np.cos(x)

tck, u = interpolate.splprep([x,y,z], s=0)
xi, yi, zi = interpolate.splev(u, tck)

print(xi)
print(yi)
print(zi)

x0 = 5.0
y0 = np.sin(x0)
z0 = np.cos(x0)

u0 = interpolate.splprep([x0,y0,z0], s=0)[1][0]
xi0, yi0, zi0 = interpolate.splev(u0, tck)

print(xi0)
print(yi0)
print(zi0)

dxdu, dydu, dzdu = interpolate.splev(u0, tck, der=1)

print(dxdu)
print(dydu)
print(dzdu)

