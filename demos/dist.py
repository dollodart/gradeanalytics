import pandas as pd
import numpy as np
from gradeanalytics import point_matrix as pm,\
        student_frame as sf, data_frame as df,\
        grade_matrix as gm
import matplotlib.pyplot as plt

def dist1(assessment,ax=None,file=None):
    """

    Plot the point distribution for a given assignment and print a table
    sorted by the student ID, for reporting new results to students.

    """
    y = pm.loc[assessment].sum()

    if ax is None:
        fig, ax = plt.subplots(nrows=1, ncols=1)

    if file is not None:
        sf['scores'] = y
        sf = sf.sort_values(by='ID')
        sf.to_latex(file, index=False,
                columns=['ID','scores'])

    #x, y = np.histogram(y.values,10)
    #ax.plot(y[:-1], x)

    #ax.hist(y.values) 

    y = y.sort_values()
    ax.set_yticks([])
    ax.plot(y.values, range(len(y)))

    return ax

def distn(assessment,ax=None):
    """

    Get the mean and standard deviation for all problems for a given
    subset of assessments.

    """

    means = gm.loc[assessment].mean(axis=1)
    stds = gm.loc[assessment].std(axis=1)

    x = ['-'.join([str(y) for y in x]) for x in means.index]

    if ax is None:
        fig, ax = plt.subplots(nrows=1, ncols=1)

    ax.errorbar(x=x, 
            y=means * 100, 
            xerr=None, 
            yerr=stds * 100, 
            fmt='ko')
    plt.xticks(rotation=90)
    return ax

def distaggn(assessment, ax = None):
    """

    Get the mean and standard deviation for a set of aggregated assessments
    (such as HW for all HW problems).

    The points matrix is used since summing points and then dividing by the
    total number of points in each class, since each class has the same
    weights, gives the fraction earned in that class

    """

    means = pm.loc[assessment].groupby(level=0).agg(np.sum).mean(axis=1)
    stds = pm.loc[assessment].groupby(level=0).agg(np.sum).std(axis=1)
    ref = df.loc[assessment]['Grading Importance', 'Total'].groupby(level=0).agg(np.sum)
    means = means / ref
    stds = stds / ref
    if ax is None:
        fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.errorbar(
        x=means.index,
        y=means * 100,
        xerr=None,
        yerr=stds * 100,
        fmt='ko')
    ax.set_xlabel('Assesment')
    ax.set_ylabel('% of that Assesment Scored')
    return ax

if __name__ == '__main__':
    assessment = 'HW', 1
    dist1(assessment)
    #distn(assessment)
    #distaggn(assessment)
    plt.show()
