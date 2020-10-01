from gradeanalytics import data_frame as df, weighted_grade_matrix as wgm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

bl = df['Assessment Metadata', 'Qual-Quant'] == 'Quant'
wt = df['Grading Importance', 'Weight'] * df['Grading Importance', 'Total']
y1 = (wt * bl).sum() / wt.sum()
y2 = 1 - y1
print('Grading Importance in Category')
print(f"Quantitative: {100*y1:.1f}%\n"
      f"Qualitative: {100*y2:.1f}%")

r1 = df['Student ID'].multiply(df['Grading Importance', 'Weight'],axis=0).mean(axis=1)
print()
print('Average Grade in Category')
print(f"Quantitative: {100*(r1[bl]/wt[bl]).mean():.1f}%\n"
      f"Qualitative: {100*(r1[~bl]/wt[~bl]).mean():.1f}%")
