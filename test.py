import numpy as np
import matplotlib.pyplot as plt

x = np.array([1,2])
y = np.array([4,5])

fig, (ax1, ax2) = plt.subplots(1,2)

ax1.scatter(1,3,color="r")
ax1.scatter(5,6,color="r")
ax2.scatter(9,10,color="b")
plt.show()
