from support import optimize_circle_placement, optimize_rectangle_placement
import pandas as pd
import numpy as np
from gradeanalytics import weighted_grade_matrix as wgm

# wgm = wgm.loc['HW'] 
wgm = wgm.groupby(level=0).agg(np.mean)

z = wgm.corr()  # correlation among student performances on all assesments

def penalty(i,j):
    return z[i+1].loc[j+1]

nstudents = wgm.shape[1]
x = list(range(1, nstudents)) # student ids, initialize ordered
opt = optimize_circle_placement(x, penalty)
print(opt)

for i in range(len(opt) - 2):
    print(opt[i],opt[i +1], penalty(opt[i],opt[i+1])/z.mean().mean())
    print(opt[i+1],opt[i +2], penalty(opt[i+1],opt[i+2])/z.mean().mean())

orc = optimize_rectangle_placement(x, 4, 3, penalty)
print(orc)
