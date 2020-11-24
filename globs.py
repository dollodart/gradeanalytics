import os
from datetime import date
from pandas import read_excel, Timestamp, concat

HOME = '/home/david/work/py-proj/gradeanalytics/'
letter_percentages = [0, 60, 63, 67, 70, 73, 77, 80, 83, 87, 90, 93, 97]
letter_grades = ['F','D-','D','D+','C-','C','C+','B-','B','B+','A-','A','A+']
filename = f'{HOME}./data.xlsx' 

full_data_frame = read_excel(filename,
                             sheet_name='scores',
                             index_col=[0, 1, 2, 3],
                             header=[0, 1])
full_data_frame = full_data_frame.ffill()

cutoff = Timestamp('2019-12-31')

time_bl = full_data_frame['Assessment Metadata','Date Assigned'] < cutoff
data_frame = full_data_frame[time_bl]
                                             
points = data_frame['Student ID']
weighted_points = points.multiply(data_frame['Grading Importance', 'Weight'], axis=0)
key = data_frame['Grading Importance', 'Total']
grades = points.divide(key,axis=0)
weighted_key = data_frame['Grading Importance', 'Total'] * data_frame['Grading Importance','Weight']
true_grades = weighted_points / weighted_key.sum()

student_frame = read_excel(filename,
                           sheet_name='students',
                           index_col='scoring ID')

if __name__ == '__main__':
    wk = weighted_key 
    r2 = full_data_frame['Grading Importance', 'Total'] / full_data_frame['Grading Importance', 'Total'].sum()
    r3 = full_data_frame['Grading Importance', 'Weight'] / full_data_frame['Grading Importance', 'Weight'].sum()
    n1 = (r2*100).round(1).rename('Point Fraction')
    n2 = (r3*100).round(1).rename('Weight Fraction')
    n3 = ((r2*r3*100)/(r2*r3).sum()).round(1).rename('Point-Weight Fraction')
    print(concat((n1,n2,n3),axis=1))
