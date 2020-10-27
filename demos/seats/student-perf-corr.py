"""
Returns correlations among assessments and among students in correlation matrix.
"""

from scipy.stats import linregress
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from gradeanalytics import weighted_grade_matrix as wgm

# choose coarser resolution by aggregation to some level
wgm = wgm.groupby(level=0).agg(np.mean)
# wgm = wgm.loc['HW'] # choose subset of highest resolution
z = wgm.corr()
fig = plt.figure()
ax = fig.add_subplot(111)
cset = ax.imshow(np.tril(z))
ax.set_xticks(range(len(z.index)))
ax.set_yticks(range(len(z.columns)))
ax.set_xticklabels(z.index, rotation=90)
ax.set_yticklabels(z.columns)
fig.colorbar(cset)
plt.show()
