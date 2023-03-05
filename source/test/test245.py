def f(x):
    return min(x**1.5/3, 130)

for i in [1,5,10,20,50,100]:
    print(f(i))