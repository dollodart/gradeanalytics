"""

Takes the column of book chapter as lists, and calculates the average
contribution to final grade of problems citing that chapter.  Or,
calculates the fraction contribution, assuming an equa split of problem
citation to all chapters cited.

"""


from gradeanalytics import data_frame as df
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
y = df['Assessment Metadata', 'Book Chapters'].apply(eval)
df['Assessment Metadata', 'Book Chapters'] = y
df = df.explode(('Assessment Metadata', 'Book Chapters'))
wt = df['Grading Importance', 'Weight'] * df['Grading Importance', 'Total']
wt = wt / wt.sum() * 100.
df['Grading Importance', 'Frac Cont'] = wt

#r = df.groupby(('Assessment Metadata', 'Book Chapters')).agg('mean')['Grading Importance', 'Frac Cont']
g = df.groupby(('Assessment Metadata', 'Book Chapters'))
r = (g.agg('sum')/g.agg('nunique'))['Grading Importance', 'Frac Cont'] 
plt.bar(r.index, r.values)
plt.xlabel('Book Chapter')
plt.ylabel('Average % Contribution of Problem Citing Chapter') 
plt.show()
