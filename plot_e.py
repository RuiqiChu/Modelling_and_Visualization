from hashlib import new
import matplotlib
from pyparsing import col

import sys
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns

f = 'p1_p2_var.dat'
with open(f, "r") as txt_file:
    input_data = [line.split() for line in txt_file]

p1s = np.linspace(0.1, 1, 10)
p2s = np.linspace(0.1, 1, 10)
avg = []
var = []
for i in range(len(input_data)):
    avg.append(float(input_data[i][2]))
    var.append(float(input_data[i][3]))


plot_avg = np.transpose(np.array(avg).reshape((10, 10)))
plot_var = np.transpose(np.array(var).reshape((10, 10)))
p1s = np.linspace(0.1, 1, 10)
p2s = np.linspace(0.1, 1, 10)
max_p2 = []
for j in range(len(plot_var)):
    max_p2_index = np.argmax((plot_var[j]))
    max_p2.append((max_p2_index+1)*0.1)
x,y = np.polyfit(p1s,max_p2,1)
max_p2s = (p1s*x+y)
X, Y = np.meshgrid(p1s, p2s)
plt.subplot(1,2,1)
plt.contourf(X, Y, plot_avg)
plt.colorbar()
plt.title('Average of the number of on sites\n vs different probabilities')
plt.xlabel('$p_1$')
plt.ylabel('$p_2$')

plt.subplot(1,2,2)
plt.contourf(X, Y, plot_var)
plt.colorbar()
plt.title('Variance of the number of on sites\n vs different probabilities')
plt.xlabel('$p_1$')
plt.ylabel('$p_2$')
plt.plot(p1s,max_p2s)
plt.xlim(0.1,1)
plt.ylim(0.1,1)
plt.savefig('p1_p2_var')

plt.show()
plt.close()