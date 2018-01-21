import numpy as np
import  matplotlib.pyplot as plt
import os

file = open("./output/threshold", "r")
dist = []
for line in file:
    dist.append(float(line.split("\t")[2]))
import seaborn as sns

sns.set(color_codes=True)
sns.distplot(dist)
plt.show()
# plt.hist(dist)
# plt.show()