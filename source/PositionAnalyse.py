from unit_old import *

hwnd=getWindowsInfo("trinityWindow","星战前夜：晨曦 - luboil")#星战前夜：晨曦
print("load over")
while(1):
    a=input().split(',')
    a=list(map(int,a))
    b=hwnd.winpos
    #   b=[58,83]
    a[0]-=b[0]
    a[1]-=b[1]
    print(a)