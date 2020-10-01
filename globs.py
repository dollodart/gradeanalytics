# globals
import os
from pandas import Timestamp
from datetime import date
from pandas import read_excel

letter_percentages = [0, 60, 63, 67, 70, 73, 77, 80, 83, 87, 90, 93, 97]
letter_grades = ['F','D-','D','D+','C-','C','C+','B-','B','B+','A-','A','A+']
filename = '/home/david/work/py-proj/gradeanalytics/data.xlsx' 

full_data_frame = read_excel(filename,
                             sheet_name='scores',
                             index_col=[0, 1, 2, 3],
                             header=[0, 1])
full_data_frame = full_data_frame.ffill()

# cutoff=Timestamp(date.today())
cutoff = Timestamp('2019-12-31')

time_bl = full_data_frame['Assessment Metadata','Date Assigned'] < cutoff
data_frame = full_data_frame[time_bl]
                                             
point_matrix = data_frame['Student ID']
weighted_point_matrix = point_matrix.multiply(
    data_frame['Grading Importance', 'Weight'], axis=0)
grade_matrix = point_matrix.divide(
    data_frame['Grading Importance', 'Total'], axis=0)
weighted_grade_matrix = weighted_point_matrix.divide(
    data_frame['Grading Importance', 'Total'] * 
    data_frame['Grading Importance', 'Weight'],axis=0)

student_frame = read_excel(filename,
                           sheet_name='students',
                           index_col='scoring ID')

if __name__ == '__main__':
    r1 = full_data_frame['Grading Importance', 'Weight']*full_data_frame['Grading Importance', 'Total']
    print('% contribution to final grade')
    print((r1 / r1.sum()*100).round(1))
    print('compare')
    r2 = full_data_frame['Grading Importance', 'Total'] / full_data_frame['Grading Importance', 'Total'].sum()
    r3 = full_data_frame['Grading Importance', 'Weight'] / full_data_frame['Grading Importance', 'Weight'].sum()
    print((r2*100).round(1)); print((r3*100).round(1)); print((r2*r3*100/(r2*r3).sum()).round(1))
