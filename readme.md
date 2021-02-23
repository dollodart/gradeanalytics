# Summary

This directory contains some analyses used for administering a course
as a graduate student. This directory contains scripts using packages
numpy, pandas, and matplotlib for analysis and visualization of
grades. Basic statistics and for the feature of assigning seats a toy
example of statistical mechanics are used in addition to the staple
of accounting. This is a demonstration of existing tools applied to a
common problem which may be borrowed for use.

Demos show one can:

  - Assign grades on absolute basis (percentage of points earned), by
  rank or coarsened rank on a relative basis, or so-called grading on a
  curve in which the mean performance of the group is adjusted but an
  absolute partition based on the normal distribution is made.

  - Make distributions and correlations among important and conveniently
  selected subsets of assignments. One may also group by problem
  number, to see if for all assesments the first question tends to
  be easier and/or have higher performance compared to the last. The
  split-apply-combine operations using pandas dataframes can be applied
  to any columns.

  - Make the data anonymous (omitting any ID), semianonymous (putting
  private IDs), or public (putting public ID) by substituting with
  dictionaries. One can use this to publish distribution charts and
  tables after exams to notify students of assesment performance.

  - Correlate student performance to assesment meta-data such as
  quantitative and qualitative problem classification, the instructor's
  perceived problem difficulty, or textbook chapter containing the
  material in the problem to inform changes in assessment, instruction,
  and curriculum.

  - Make time series plots using assignment date can be used to evaluate
  transient trends in students' group and individual performance and
  predict future performance and end-of course grades, valuable for
  intervention for at-risk and/or underrepresented students to improve
  retention.

  - Investigate possible demographic bias by comparing student
  performance by group to that expected from larger data set
  statistics. Student demographic data such as age, ethnicity, gender,
  income, and race can be found to have correlations to student
  performance. This can be compared to county, state, or national level
  performance differences to see if the demographic bias is better or
  worse than expected.

  - Investigate cheating by checking the correlation of students grades
  on assesments. Similarly good students will obtain similarly good
  scores and so it is required to find anomolously high correlation by
  subtracting the expected correlation. This would not be definitive
  since some students study or work together, as well. But it may be
  used for assigning seats for exams by pairing those with lowest
  correlated scores.

  - Include native python objects in the excel file by using the
  DataFrame method `apply` and python builtin `eval`, if not interpreted
  by the pandas excel parser directly. This is used to have a compact
  representation of fields, especially those with variable lengths, in
  the spreadsheet.


If gradebooks from several courses are available, then comparison
of student performance can be done by comparing these quantitative
measures. For example, it may be expected that summer quarter or summer
session has lower student performance due to shortened period and
demographics of the class, which can be found by comparing the average
grade in a summer quarter or session to a regular quarter or semester.

It should be noted that, while the number of applications listed is
large and could be made much larger, the method of analysis is the same
and of an elementary type: to calculate (statistically significant)
differences and distributions using probability and statistics.

# Data Spreadsheet

The grade data has inputs for both total number of points and weights
for each assignment. Each point can be assigned the same weight
everywhere, and more important assesments then be given more points. It
is also possible to allow the weight of a point to vary by class of
assignment. The motivation for this is that a sufficient integer
number is required, most rubrics assigning integer numbers to each
criterion, to grade something fairly, but assignment importance
might vary over significant scales to make equal point weighting, if
the lowest importance assignment is to have a signficant number of
points, non-ideal because the highest importance assignment then has
too many points. Though it is possible to assign different weights
to each assignment, that defeats the purpose of a point based system
(see assignment weighting for justification of different weights for
assignment classes).

Note the weights so defined do not give the contribution of the
assesment or its class to the final grade. It is possible to find the
weights required given some number of points for each assesment such
that the class of assesment contributes a given percentage to the final
grade, see `find-weights.py`.

The grade data is given hierarchial indexing in both columns and
rows to most emulate (what I understand to be) standard spreadsheet
format. Changing the hierarchial indexing will change the resulting
DataFrame and require editing the scripts.

A separate markup sheet which has some cells copied to the data sheet
can be used to allow comments and calculations in the spreadsheet while
keeping the data in a format which can be read into the DataFrame. The
`pandas.read_excel` function fills left-to-right and top-to-bottom for
implied repetition of the last preceding value when a cell is blank.

## Sample Data

The sample data is obtained by a normal distributions for fraction of
points earned, independent of any of the demographic/socioeconomic
factors also randomized. Meaningful trends must be obtained by actual
data, which I no longer have access to.

# Data Frame

The data frame contains all the information of the spreadsheet. Some
copies of the dataframe parts are made in the global space for
convenient access:

- `full_data_frame` is the data frame prior to removing all dates for
which there are no entries, used for predicting future performance.
- `points` contains the points for each assignment by each student,
which is used to report newly made grades to students (since they should
have an understanding for the weights of classes, and this is more
information when different assesments in the same class have different
numbers of points).
- `weighted_points` is the unnormalized contribution of each assesment
for each student to their final grade.
- `grades` contains the percent of total points scored for each
assignment by each student, which is valuable for analyzing performance
on each assesment, but is generally unrelated to the final score.
- `true_grades` uses the correct normalization factor of the sum of all
points in the weighted key. This gives the fraction of all weighted
points earned, and is used to directly calculate grades based on common
fraction assignments (e.g., 85% of points is a B) by summing.

The `true_grades` gives the contribution normalized by the total number
of weighted points, which gives a fraction of total (weighted) points
often used for assigning grades in absolute scale when summed. However,
for relative grading, the `weighted_points` frame can be directly
used. Note that `grades` is normalized by a Series (the key) using
broadcasting rules, while `true_grades` is normalized by a scalar for
total count of weighted points.

# Assignment Weighting

The purpose of having two ways to weight assignments, a per point weight
and a number of points, rather than just one, is the following:

1. If only point totals are used to weigh assignments, graders have
little freedom in defining point counts and often must use fractional
points on homework assignments which are much longer (have more
problems) and must be assigned fewer points not just for being less
important, but more numerous than test questions.
2. If only assignment weights are used, e.g., the fractional score is
weighted, then points have no intuitive meaning across assignments,
unlike, e.g., a point in the final being worth some times more than a
point in homework.

The added difficulty of calculating how important the assignment or any
one of its problems is to the final grade is done by the program which
of course can be shared with students. I have called this quantity the
grade contribution, both for the total points so weighted (given the
variable `weighted_key`) and for the student's score so weighted. The
`weighted_points` may be called the `contribution` in light of this.

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

Null, or not-a-number, values are omitted in calculating aggregates and
propogated in calculating element-wise binary operators by pandas. Zero
values, on the other hand, are effectively omitted except in cases
of division, for which they convert they result in an error-less
infinity. The question is what each one should represent. While it may
generally be desired to have arbitrary strings be used to designate why
an entry is missing, such as "not submitted" or "excused absence", those
cannot be supported in a native way and will throw type errors. The best
that can be done is to create a dictionary which maps those strings to
0 or NaN, and then to ensure the column data type is float (since with
mixed data it will be read in as object).

To elaborate on the "not submitted" and "excused absence" cases. For
some activities it is desired that the student, if missed for a valid
reason, has that assignment omitted from their total score, so that
all other assignments take over in importance. This is not trivial to
implement since the total is usually calculated independently of the
student score, and then broadcasted over all student scores. But it
could be implemented by using NaN to omit from aggregates regarding
that student. This is not yet done. Not submitted, on the other hand,
receives a score of 0, which should be distinct from any submitted
assignment score and allow one to, by testing for equality, determine
the number of assignments not submitted. This is, without any further
intervention, supported since student's scores are not used to divide
any quantity.
