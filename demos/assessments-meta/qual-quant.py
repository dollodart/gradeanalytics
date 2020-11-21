from gradeanalytics import data_frame as df, weighted_key as wk, points as pm, key as k
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

bl = df['Assessment Metadata', 'Qual-Quant'] == 'Quant'
y1 = (wk[bl]).sum() / wk.sum()
y2 = 1 - y1
print('Grading Importance in Category')
print(f"Quantitative: {100*y1:.1f}%\n"
      f"Qualitative: {100*y2:.1f}%")

quant = pm[bl].sum()/k[bl].sum()
qual = pm[~bl].sum()/k[~bl].sum()
print()
print('Student Average Fraction Points in Category')
print(f"Quantitative: {100*quant.mean():.1f}%\n"
      f"Qualitative: {100*qual.mean():.1f}%")
