"""
Returns correlations among assessments and among students in correlation matrix.
"""

from scipy.stats import linregress
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from gradeanalytics import grades as gm

# choose coarser resolution by aggregation to some level
gm = gm.groupby(level=0).agg(np.mean)
# gm = gm.loc['HW'] # choose subset of highest resolution
z = gm.corr()
fig = plt.figure()
ax = fig.add_subplot(111)
cset = ax.imshow(np.tril(z))
ax.set_xticks(range(len(z.index)))
ax.set_yticks(range(len(z.columns)))
ax.set_xticklabels(z.index, rotation=90)
ax.set_yticklabels(z.columns)
fig.colorbar(cset)
plt.show()
