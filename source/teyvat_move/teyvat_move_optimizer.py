from source.util import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import splprep, splev

class ThreeDimensionOptimizer():
    def __init__(self, tlpp) -> None:
        self.bps = tlpp
        self.points = []
        last_i = [99999,99999]
        for i in tlpp['break_position']:
            if i == last_i:
                continue
            self.points.append([float(i[0]), float(i[1]), tlpp['break_position'].index(i)])
            last_i = i
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
    
    def predict_nearest_point(self, x, y, z):
        distances = (self.x_new - x)**2 + (self.y_new - y)**2
        # distances = distances*(self.z_new - z)*10
        
        for i in range(len(distances)):
            min_index = np.argmin(distances)
            if self.z_new[min_index] < z - 1:
                distances[min_index] = 99999
                print('pnp skip: <-1')
                continue
            elif self.z_new[min_index] > z + 5:
                distances[min_index] = 99999
                print('pnp skip: >5')
                continue
            else:
                break
            
        return self.x_new[min_index], self.y_new[min_index], self.z_new[min_index]

    def predict_gradient(self, x, y, z):
        dxdu, dydu, dzdu = splev(np.where(self.x_new == x)[0][0]/len(self.x_new), self.tck, der=1, ext=2)
        return dxdu, dydu, dzdu
    
if __name__ == '__main__':
    def get_path_file(path_file_name:str):
        return load_json(path_file_name+".json","assets\\TeyvatMovePath")
    # points = [(1, 1, 1), (2, 2, 2), (3, 3, 3), (4,4,4)]
    tlpp = get_path_file('Cecilia20230513195754i0') # GlazeLily20230513214422i0
    
    tdo = ThreeDimensionOptimizer(tlpp)
    # tdo.show_plt()
    x,y,z = tdo.predict_nearest_point(tlpp['start_position'][0],tlpp['start_position'][1],1)
    print(x,y,z)
    r = tdo.predict_gradient(x,y,z)
    print(r)