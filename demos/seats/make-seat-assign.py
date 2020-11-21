from support import optimize_circle_placement, optimize_rectangle_placement
import pandas as pd
import numpy as np
from gradeanalytics import weighted_grades as wgm

# wgm = wgm.loc['HW'] 
wgm = wgm.groupby(level=0).agg(np.mean)

z = wgm.corr()  # correlation among student performances on all assesments

def penalty(i,j):
    if i == 0 or j == 0:
        return -1 # this is the minimum correlation coefficient
    return z[i].loc[j]

nstudents = wgm.shape[1]
x = list(range(1, nstudents)) # student ids, initialize ordered

# make a temperature based on the average interaction energy
# this is correlation coefficient excluding self-correlation
temp = 0
for i in x:
    for j in range(1, i):
        temp += penalty(i, j)
temp /= nstudents**2 / 2
temp /= 10
opt = optimize_circle_placement(x, penalty, temp=0.05)
print(opt)

for i in range(len(opt) - 2):
    for j in 1, 2:
        s1, s2, e = opt[i + j - 1],opt[i + j], penalty(opt[i + j - 1],opt[i+j])/z.mean().mean()
        print(f'{s1:n} {s2:n} {e:.1f}')

orc = optimize_rectangle_placement(x, 4, 3, penalty, temp=0.05)
print(orc)
