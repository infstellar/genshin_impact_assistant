from typing import Any

from source.util import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import splprep, splev
from source.common.timer_module import *

class B_SplineCurve_GuidingHead_Optimizer():
    """

    B样条曲线-引导头优化器。

    该优化器使用B样条曲线拟合TLPP文件中的BPs，以BP的index作为z轴坐标，

    通过predict_nearest_point函数获得当前BP index，通过predict_guiding_head_position预测引导头位置。

    将移动目标从BP坐标优化为引导头坐标，保证了TMF的连续性。由此避免了走过头导致的BP检测失败，和调试offset这一不可控的magic number。


    """
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

        self.curr_length = 0 # 0~1

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

    # @timer
    def predict_nearest_point(self, x, y, z):
        distances = (self.x_new - x)**2 + (self.y_new - y)**2
        # distances = distances*(self.z_new - z)*10
        min_index = 0
        for i in range(len(distances)):
            min_index = np.argmin(distances)
            if self.z_new[min_index] < z - 1:
                distances[min_index] = 99999
                if DEBUG_MODE:
                    print('pnp skip: <-1')
                continue
            elif self.z_new[min_index] > z + 4:
                distances[min_index] = 99999
                if DEBUG_MODE:
                    print('pnp skip: >1')
                continue
            else:
                break

        return self.x_new[min_index], self.y_new[min_index], self.z_new[min_index]

    # @timer
    def predict_guiding_head_position(self,z):
        dxdu, dydu, dzdu = self.predict_gradient(z)
        rate = 0.5-(dzdu-120)*0.005
        print(f"dzdu: {dzdu}, rate: {rate}")
        # if dzdu<=30:
        #     rate = 1
        # else:
        #     rate = maxmin(rate, 1.5, 0.5)
        rate = 1
        # print(f"final rate: {rate}")
        guiding_head_z = z + rate
        distances = abs(self.z_new - guiding_head_z)
        guiding_head_index = np.argmin(distances)
        print(round(min(distances),2), guiding_head_index)
        return [self.x_new[guiding_head_index], self.y_new[guiding_head_index]]

    def predict_gradient(self, z):
        if z == 0:
            z = self.z_new[0]
        dxdu, dydu, dzdu = splev(np.where(self.z_new == z)[0][0]/len(self.z_new), self.tck, der=1, ext=2)
        return dxdu, dydu, dzdu

if __name__ == '__main__':
    def get_path_file(path_file_name:str):
        return load_json(path_file_name+".json","assets\\TeyvatMovePath")
    # points = [(1, 1, 1), (2, 2, 2), (3, 3, 3), (4,4,4)]
    tlpp = get_path_file('Cecilia20230513195754i0') # GlazeLily20230513214422i0

    tdo = B_SplineCurve_GuidingHead_Optimizer(tlpp)
    tdo.show_plt()
    x,y,z = tdo.predict_nearest_point(tlpp['start_position'][0],tlpp['start_position'][1],1)
    print(x,y,z)
    r = tdo.predict_gradient(z)
    print(r)