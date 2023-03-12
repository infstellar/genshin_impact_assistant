import numpy as np
import matplotlib.pyplot as plt
import pwlf, sympy
from source.util import *
def get_breaks_points(posi_list):
    
    # 生成一些随机数据
    # x = np.linspace(0, 10, 100)
    # y = np.piecewise(x, [x < 3, x < 6, x >= 6], [lambda x: x + np.random.randn(len(x)), lambda x: -x + 9 + np.random.randn(len(x)), lambda x: x - 6 + np.random.randn(len(x))])
    posi_dict=load_json("qingxin167859238574.json","assets\\TeyvatMovePath")
    all_posi = []
    for i in posi_dict["position_list"]:
        all_posi.append(i["position"])
    start_point = np.array(posi_dict["start_position"])
    end_point = np.array(posi_dict["end_position"])
    x=np.array(all_posi)[:,0]#-start_point[0]
    y=np.array(all_posi)[:,1]#-start_point[1]
    # 创建一个pwlf对象，并传入自变量和因变量
    my_pwlf = pwlf.PiecewiseLinFit(x,y)

    # 使用fit方法进行自动分段选择和拟合，指定最大分段数为5
    t1 = time.time()
    print(my_pwlf.fit(4))
    print(time.time()-t1)

    # 获取最优分段数和对应的R_squared值
    n_segments = my_pwlf.n_segments
    # r_squared = my_pwlf.R_squared()
    my_pwlf.break_n
    # 打印结果
    print('The optimal number of segments is', n_segments)
    # print(my_pwlf._get_breaks())
    # print('The R-squared value is', r_squared)

    # 获取预测值
    xd = np.linspace(start_point[0],end_point[0])
    yd = my_pwlf.predict(xd)

    # 绘制散点图和拟合曲线
    plt.subplot(2,1,1)
    plt.scatter(x,y)
    plt.plot(xd,yd,'r')
    plt.title('Data and fit')

    # 计算并绘制残差图
    residuals = y - my_pwlf.predict(x)
    plt.subplot(2,1,2)
    plt.scatter(x,residuals)
    plt.hlines(0,x.min(),x.max())
    plt.title('Residuals')
    plt.show()

get_breaks_points(1)