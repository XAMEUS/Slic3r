import numpy as np
import matplotlib.pyplot as plt


N = 5
menMeans = (20, 35, 30, 35, 27)
womenMeans = (25, 11, 34, 20, 25)
ind = np.arange(N)    # the x locations for the groups
width = 0.2       # the width of the bars: can also be len(x) sequence

p1 = plt.bar(ind-width, menMeans, width, color='green')
p2 = plt.bar(ind, womenMeans, width, color='blue')
p3 = plt.bar(ind+width, womenMeans, width, color='red')

plt.ylabel('Temps')
plt.xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5'))
plt.legend((p1[0], p2[0], p3[0]), ('Alt', 'Bruteforce', 'Bo'))
plt.show()
