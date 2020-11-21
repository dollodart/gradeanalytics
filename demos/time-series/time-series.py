import matplotlib.pyplot as plt
from gradeanalytics import grades as gm, data_frame as df
import pandas as pd
pd.plotting.register_matplotlib_converters()

df = df.loc['HW']
gm = gm.loc['HW']

plt.figure()
plt.xlabel('Date of Assesment')
plt.xticks(rotation=90)

# average grade (fractional in assignment, not contribution) with time
plt.plot(df['Assessment Metadata', 'Date Assigned'], 100 * gm.mean(axis=1), 'o')
plt.ylabel('Average Percentage Points In Assessment')
plt.title('Homeworks Time Series')

# number of missing assignments
#plt.plot(df['Assesment Metadata','Date Assigned'], (wgm == 0).sum(axis=1), 'o')
#plt.ylabel('Number of Missing Assignments')

plt.show()
