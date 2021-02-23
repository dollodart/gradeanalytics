This directory contains scripts using packages numpy, pandas, and matplotlib for analysis and visualization of grades. The theory used is limited to basic statistics and similar data transforms are made between analogous cases in which the most difference is in the name of the fields. This is a demonstration of existing tools applied to a common problem which may be borrowed for use.

Demos show that:
  - Distributions and correlations among important and conveniently selected subsets of assignments can be made.
    - Group by problem number, to see if for all assesments the first question tends to be easier and/or have higher performance compared to the last.
    - Student demographic data such as age, ethnicity, gender, income, and race can be found to have correlations to student performance.
  - The data can be anonymized (omitting any ID), semianonymized (putting private IDs), or publicized (putting public ID) with dictionaries.
    - Publish distribution charts and tables after exams to notify students of assesment performance.
  - Assesment meta-data such as quantitative and qualitative or relevant textbook chapter can be included and related to student performance.
  - Assignment date can be used to plot time-series to evaluate transient trends in students' group and individual performance.
  - Native python objects can be included in the excel file by using the DataFrame method `apply` and python builtin `eval`, if not interpreted by the parser directly.
    - This is used to have a compact representation of fields, especially those with variable lengths, in the spreadsheet.
    - While list objects can't be entered into a single cell of a spreadsheet program as a spreadsheet object, other objects such as dates can, and will be parsed to the appropriate Python object, in this case a date or datetime.
  - Possible demographic bias can be found by comparing student performance by group to that expected from larger data set statistics.
    - This can be compared to county, state, or national level performance differences to see if the demographic bias is better or worse than expected.
  - Possible cheating can be found by checking the correlation of students grades on assesments.
    - Similarly good students will obtain similarly good scores and so it is required to find anomolously high correlation by subtracting the expected correlation. This would not be definitive since some students study or work together, as well. But it may be used for assigning seats for exams by pairing those with lowest correlated scores. TODO: use a monte carlo simulation with energy weights for nearest neighbors based on correlation strength in an exam to determine the best seating arrangement.
  - Projections of grades for students can be made which are valuable for intervention for at-risk and/or underrepresented students and can be used to improve retention.
  - Correlations between instructor assigned problem difficulty and student performance can be made to see if the correlation is as expected
    - If not, the instruction may be improved in areas where performance relative to difficulty level is lower than expected.
  - Assigning grades relative to cohort performance for cases when absolute performance is outside expected ranges can be done
    - rank or coarsened rank 
    - so-called grading on a curve 

If gradebooks from several courses are available, then comparison of student performance can be done by comparing these quantitative measures. For example, it may be expected that summer quarter or summer session has lower student performance due to shortened period and demographics of the class, which can be found by comparing the average grade in a summer quarter or session to a regular quarter or semester.

It should be noted that, while the number of applications listed is large and could be made much larger, the fundamental method of analysis is the same and of an elementary type: to calculate (statistically significant) differences using statistics and statistical tests.

# Data Spreadsheet
The grade data has inputs for both total number of points and weights for each assignment. Each point can be assigned the same weight everywhere, and more important assesments then be given more points. It is also possible to allow the weight of a point to vary by class of assignment. The motivation for this is that a sufficient integer number is required, most rubrics assigning integer numbers to each criterion, to grade something fairly, but assignment importance might vary over significant scales to make equal point weighting, if the lowest importance assignment is to have a signficant number of points, non-ideal because the highest importance assignment then has too many points. Though it is possible to assign different weights to each assignment, that defeats the purpose of a point based system.

Note the weights so defined do not give the contribution of the assesment or its class to the final grade. It is possible to find the weights required given some number of points for each assesment such that the class of assesment contributes a given percentage to the final grade, see `find-weights.py`.

The grade data is given hierarchial indexing in both columns and rows to most emulate (what I understand to be) standard spreadsheet format. Changing the hierarchial indexing will change the resulting DataFrame and require editing the scripts.

A separate markup sheet which has some cells copied to the data sheet can be used to allow comments and calculations in the spreadsheet while keeping the data in a format which can be read into the DataFrame. The `pandas.read_excel` function fills left-to-right and top-to-bottom for implied repetition of the last preceding value when a cell is blank.

## Sample Data

The sample data is obtained by a normal distributions for fraction of points earned, independent of any of the demographic/socioeconomic factors also randomized. Meaningful trends must be obtained by actual data, which I no longer have access to.

# Data Frame
The data frame contains all the information of the data spreadsheet. Some copies of the dataframe parts are made in the global space for convenient access:

- `full_data_frame` is the data frame prior to removing all dates for which there are no entries, used for predicting future performance.
- `points` contains the points for each assignment by each student, which is used to report newly made grades to students (since they should have an understanding for the weights of classes, and this is more information when different assesments in the same class have different numbers of points).
- `weighted_points` is the unnormalized contribution of each assesment for each student to their final grade.
- `grades` contains the percent of total points scored for each assignment by each student, which is valuable for analyzing performance on each assesment, but is generally unrelated to the final score.
- `true_grades` uses the correct normalization factor of the sum of all points in the weighted key. This gives the fraction of all weighted points earned, and is used to directly calculate grades based on common fraction assignments (e.g., 85% of points is a B) by summing.

The `true_grades` gives the contribution normalized by the total number of weighted points, which gives a fraction of total (weighted) points often used for assigning grades in absolute scale when summed. However, for relative grading, the `weighted_points` frame can be directly used. Note that `grades` is normalized by a Series (the key) using broadcasting rules, while `true_grades` is normalized by a scalar for total count of weighted points.

The purpose of having two ways to weight assignments, a per point weight and a number of points, rather than just one, is the following:

1. If only point totals are used to weigh assignments, graders have little freedom in defining point counts and often must use fractional points on homework assignments which are much longer (have more problems) and must be assigned fewer points not just for being less important, but more numerous than test questions.
2. If only assignment weights are used, e.g., the fractional score is weighted, then points have no intuitive meaning across assignments, unlike, e.g., a point in the final being worth some times more than a point in homework.

The added difficulty of calculating how important the assignment or any one of its problems is to the final grade is done by the program which of course can be shared with students. I have called this quantity the grade contribution, both for the total points so weighted (given the variable `weighted_key`) and for the student's score so weighted. The `weighted_points` may be called the `contribution` in light of this.

```
wk = full_data_frame['Grading Importance', 'Weight']*full_data_frame['Grading Importance', 'Total']
r2 = full_data_frame['Grading Importance', 'Total'] / full_data_frame['Grading Importance', 'Total'].sum()
r3 = full_data_frame['Grading Importance', 'Weight'] / full_data_frame['Grading Importance', 'Weight'].sum()
n1 = (r2*100).round(1).rename('Point Fraction')
n2 = (r3*100).round(1).rename('Weight Fraction')
n3 = ((r2*r3*100)/(r2*r3).sum()).round(1).rename('Point-Weight Fraction')
print(concat((n1,n2,n3),axis=1))
```

## Null and Zero Values
Null, or not-a-number, values are omitted in calculating aggregates and propogated in calculating element-wise binary operators by pandas. Zero values, on the other hand, are effectively omitted except in cases of division, for which they convert they result in an error-less infinity. The question is what each one should represent. While it may generally be desired to have arbitrary strings be used to designate why an entry is missing, such as "not submitted" or "excused absence", those cannot be supported in a native way and will throw type errors. The best that can be done is to create a dictionary which maps those strings to 0 or NaN, and then to ensure the column data type is float (since with mixed data it will be read in as object). 

To elaborate on the "not submitted" and "excused absence" cases. For some activities it is desired that the student, if missed for a valid reason, has that assignment omitted from their total score, so that all other assignments take over in importance. This is not trivial to implement since the total is usually calculated independently of the student score, and then broadcasted over all student scores. But it could be implemented by using NaN to omit from aggregates regarding that student. Not submitted, on the other hand, receives a score of 0, which should be distinct from any submitted assignment score and allow one to, by testing for equality, determine the number of assignments not submitted.
