from gradeanalytics import data_frame as df
import pandas as pd
import matplotlib.pyplot as plt

y = df['Grading Importance', 'Total'] * df['Grading Importance', 'Weight']
df['Grading Importance', 'Frac Cont'] = y / y.sum()

r = (df.loc['HW'].groupby(('Assessment Metadata', 'Difficulty')).agg('sum')
    ['Grading Importance', 'Frac Cont'])

plt.plot(r.index, r.values*100, 'o')
plt.ylim((-1, r.max()*110))
plt.xlabel('Difficulty')
plt.ylabel('Percent Contribution to Final Grade')
plt.title('Homeworks Contribution to Final Grade by Difficulty')
plt.show()
