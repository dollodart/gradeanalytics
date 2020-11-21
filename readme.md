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

- `full_data_frame` is the data frame prior to removing all dates for which there are no entries, used for predicting future performance
- `points` contains the points for each assignment by each student, which is used to report newly made grades to students (since they should have an understanding for the weights of classes, and this is more information when different assesments in the same class have different numbers of points)
- `weighted_points` is the unnormalized contribution of each assesment for each student to their final grade.
- `grade_matrix` contains the percent of total points scored for each assignment by each student, which is valuable for analyzing performance on each assesment, but is generally unrelated to the final score
- `weighted_grades` contains the fraction earned in the weighted contribution. This valuable for calculating course performance and importance metrics where the point weighting should be taken into account. 
- `true_grades` uses the correct normalization factor of the sum of all points in the weighted key. This gives the fraction of all weighted points earned, and is used to directly calculate grades based on common fraction assignments (e.g., 85% of points is a B).

The `grades` is different from `weighted_grades` since different assessments have different numbers of points independent of their point weight. The `true_grades` gives the contribution normalized by the total number of weighted points, which gives a fraction of total (weighted) points often used for assigning grades in absolute scale when summed. However, for relative grading, the `weighted_points` frame can be directly used.

The purpose of having two ways to weight assignments, a per point weight and a number of points, rather than just one, is the following:

1. If only point totals are used to weigh assignments, graders have little freedom in defining point counts and often must use fractional points on homework assignments which are much longer (have more problems) and must be assigned fewer points not just for being less important, but more numerous than test questions.
2. If only assignment weights are used, e.g., the fractional score is weighted, then points have no intuitive meaning across assignments, unlike, e.g., a point in the final being worth some times more than a point in homework.

The added difficulty of calculating how important the assignment or any one of its problems is to the final grade is done by the program which of course can be shared with students. I have called this quantity the grade contribution, both for the total points so weighted (given the variable `weighted_key`) and for the student's score so weighted. The `weighted_points` may be called the `contribution` in light of this.

```
wk = full_data_frame['Grading Importance', 'Weight']*full_data_frame['Grading Importance', 'Total']
print('% contribution to final grade')
print((wk / wk.sum()*100).round(1))
print('compare')
r2 = full_data_frame['Grading Importance', 'Total'] / full_data_frame['Grading Importance', 'Total'].sum()
r3 = full_data_frame['Grading Importance', 'Weight'] / full_data_frame['Grading Importance', 'Weight'].sum()
print(r2); print(r3)
```
