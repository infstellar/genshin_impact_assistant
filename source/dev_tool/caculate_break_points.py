import numpy as np
import matplotlib.pyplot as plt
import pwlf
from source.util import *
def get_breaks_points(dict_name, show_res = True):
    posi_dict=load_json(dict_name,"assets\\TeyvatMovePath")
    all_posi = []
    for i in posi_dict["position_list"]:
        all_posi.append(i["position"])
    start_point = np.array(posi_dict["start_position"])
    end_point = np.array(posi_dict["end_position"])
    x=np.array(all_posi)[:,0]
    y=np.array(all_posi)[:,1]

    for i in range(1,20):
        my_pwlf = pwlf.PiecewiseLinFit(x,y)
        print(f"calculating: {i}")
        t1 = time.time()
        my_pwlf.fit(i)
        t2 = time.time()-t1
        print(f"cost {t2}")
        n_segments = my_pwlf.n_segments
        # 打印结果
        print('The optimal number of segments is', n_segments)
        print(my_pwlf.fit_breaks)
        if t2 >= 10: # max sec
            break

    if show_res:
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
    res = my_pwlf.predict(my_pwlf.fit_breaks)
    res = list(zip(list(res), list(my_pwlf.fit_breaks)))
    print(res)
    return res

json_list = []
for root, dirs, files in os.walk(os.path.join(ROOT_PATH,"assets\\TeyvatMovePath")):
    for file in files:
        if '.' in file:
            if file[file.index('.'):]==".json":
                json_list.append(file)
print(json_list)
for jn in json_list:
    j = load_json(jn,os.path.join(ROOT_PATH,"assets\\TeyvatMovePath"))
    if "break_position" not in j:
        j["break_position"] = get_breaks_points(jn)
        save_json(j,jn,os.path.join(ROOT_PATH,"assets\\TeyvatMovePath"))