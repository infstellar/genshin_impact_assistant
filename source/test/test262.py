from source.util import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import splprep, splev

def get_path_file(path_file_name:str):
    return load_json(path_file_name+".json","assets\\TeyvatMovePath")



# points = [(1, 1, 1), (2, 2, 2), (3, 3, 3), (4,4,4)]
tlpp = get_path_file('GlazeLily20230513214422i0')

class ThreeDimensionOptimizer():
    def __init__(self, tlpp) -> None:
        self.bps = tlpp
        self.points = []
        for i in tlpp['break_position']:
            self.points.append([i[0], -i[1], tlpp['break_position'].index(i)])
        self.x_new, self.y_new, self.z_new, self.tck = self._fit_curve(self.points)
        

    def _fit_curve(self, points):
        points = np.array(points)
        tck, u = splprep(points.T, u=None, s=0.0)
        u_new = np.linspace(u.min(), u.max(), 1000)
        x_new, y_new, z_new = splev(u_new, tck)
        return x_new, y_new, z_new, tck
    
    def show_plt(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(self.x_new, self.y_new, self.z_new)
        plt.show()    
    
    def predict_nearest_point(self, x, y, z=0):
        if z==0:
            distances = (self.x_new - x)**2 + (self.y_new - y)**2
            min_index = np.argmin(distances)
        else:
            distances = (self.x_new - x)**2 + (self.y_new - y)**2 + (self.z_new - z)**2
            min_index = np.argmin(distances)
        return self.x_new[min_index], self.y_new[min_index], self.z_new[min_index]

    def predict_gradient(self, x, y, z):
        dxdu, dydu, dzdu = splev(z/len(self.z_new), self.tck, der=1)
        return dxdu, dydu, dzdu


