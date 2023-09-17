from sklearn.ensemble import IsolationForest
import numpy as np
data = np.array([10,11,15,99,11,25]).reshape(-1, 1)
predictions = IsolationForest().fit(data).predict(data)
data2 = data[predictions==1]
print (data2.reshape(1, -1)[0])