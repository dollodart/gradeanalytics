from gradeanalytics import letter_percentages, letter_grades, weighted_grade_matrix as wgm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from scipy.stats import normaltest

def abcdf(file=None):
    """

    Bin the students total grades into the classical ABCDF system.

    """

    sm = wgm.sum()
    grades = pd.cut(100.* sm, 
            letter_percentages, 
            labels=letter_grades[:-1])

    # sum collapses to the student IDs
    # index is "problem subnumber" from previous index
    grades.name = 'Letter Grade'
    grades.index.name = 'Scoring ID'

    if file is None:
        file = open('final_grades_table.tex', 'w')
    grades.to_latex(file)
    file.close()

    return None

def abcdf_vis(axs=None):
    sm = wgm.sum().sort_values(axis=0) * 100.
    sorted_student_numbers = sm.index.values

    if axs is None:
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax2 = ax1.twiny()
        ax3 = ax1.twinx()

    ax1.bar(sorted_student_numbers, sm, width=0.1)
    ax1.set_ylim([0, 100])
    ax1.set_xticks(np.arange(1, max(sorted_student_numbers) + 1))
    ax1.set_ylabel('percentage of total points')
    ax1.set_xlabel('student ID')

    ax2.set_xlim(ax1.get_xlim())
    ax2.set_xticks(ax1.get_xticks())
    ax2.set_xticklabels(sorted_student_numbers)
    ax2.set_xlabel('class rank')

    # ax3.set_ylim([0,100])
    ax3.set_ylim(ax1.get_ylim())
    ax3.set_yticks(letter_percentages)
    ax3.set_yticklabels(letter_grades)
    ax3.set_ylabel('conventional letter grade')

    return ax1, ax2, ax3

def rank():
    """

    Returns the class ranks for each student.

    """

    sm = wgm.sum().sort_values(axis=0) * 100.
    nstudents = wgm.shape[1]
    return ["{} {}".format(*x) for x in zip(sm.index,reversed(range(nstudents)))]

def coarse_rank():
    """
    
    Assign the same number of each grade type.
    This is just a coarse version of class rank.

    """
    sm = wgm.sum().sort_values(axis=0) * 100.
    nstudents = wgm.shape[1]
    ngrades = len(letter_grades)
    nstudents_per_grade = nstudents // ngrades

    l = []
    c = 0
    i = 0
    letter_grades[::-1] = letter_grades
    for _ in range(wgm.shape[1]):
        if c > nstudents_per_grade:
            c = 0
            i += 1
        l.append(letter_grades[i])
        c += 1
    l[::-1] = l

    return ["{} {}".format(*x) for x in zip(sm.index,l)]


def bell_curve(): 
    """                                                   

    If the student grade distribution is unimodal it may be desired to give
    more grades of the mean value than of the extreme values. A linear space
    in the grade assigned will result in a small fraction of extreme grades
    in most cases. For a gaussian curve, the population in both extremes is
    approximately 1/3 the total.

    For example, assign the mean grade to be B and let the spacing for
    letter grades be such that C+ lies one negative std. dev., A- one
    positive std. dev.

         -s     m    +s
    .-----.-----.-----.-----.
       |     |     |     |
    C+    B-    B     B+    A-

    In list form,

    labels=['C+','B-','B','B+','A-']
    bins=[m-2.5*s,m-1.5*s,m-0.5*s,m+0.5*s,m+1.5*s,m+2.5*s]

    The cut method returns

    C+ in (m-2.5*s,m-1.5*s]
    B- in (m-1.5*s,m-0.5*s]
    B  in (m-0.5*s,m+0.5*s]
    B+ in (m+0.5*s,m+1.5*s]
    A- in (m+1.5*s,m+2.5*s]

    Note the C grade is the average grade between F and A in the
    conventional ABCDF system.

    """

    sm = wgm.sum().sort_values(axis=0) * 100.
    mean = sm.mean()
    std = sm.std()
    peaks, _ = find_peaks(np.histogram(sm)[0])

    if len(peaks) > 1:
        #raise Warning("Multimodal distribution")
        print(f'multimodal distribution with {len(peaks)} peaks')

    res = normaltest(sm)

    if res.pvalue < 0.05:
        #raise Warning("grade distribution fails D'Agostino Pearson normality test")
        print("grade distribution fails D'Agostino Pearson normality test with p = {res.pvalue} < 0.05")

    n = len(letter_grades)
    if n % 2 == 0:
        r1 = range(n // 2)  # unchecked
        r2 = range(2, n // 2 + 1)
    else:
        r1 = range(n // 2 + 2)
        r2 = range(2, n // 2 + 2)

    spacing = std * 2 / 3
    bins = [mean - spacing * (i - 1 / 2) for i in r1][::-1] \
        + [mean + spacing * (i - 1 / 2) for i in r2]
    high = (sm > mean + spacing * 0.5).sum()
    low = (sm < mean - spacing * 0.5).sum()
    med = sm.size - (high + low)
    scs = [low, med, high]
    print("student distribution: {}% low, {}% medium, {}% high".format(
    *[100 * x / sum(scs) for x in scs]))
    res = pd.cut(sm, bins, labels=letter_grades[::-1])
    return res

if __name__ == '__main__':
#    abcdf()
#    abcdf_vis()
#    plt.show()
#    for i in rank():
#        print(i)
#    for i in coarse_rank():
#        print(i)
    print(bell_curve())
