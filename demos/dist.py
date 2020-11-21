import pandas as pd
import numpy as np
from gradeanalytics import points as pm,\
        full_data_frame as fdf,\
        grades as gm
import matplotlib.pyplot as plt

def dist1(assessment,df=pm):
    """

    Return a table for the points earned in a given assessment.

    """
    y = df.loc[assessment].sum()
    y = y.sort_values()
    return y


def dist1_vis(assessment,df=pm,ax=None):
    """

    Plot the point distribution for a given assessment.

    """

    y = dist1(assessment, df)

    if ax is None:
        fig, ax = plt.subplots(nrows=1, ncols=1)

#    ax.set_yticks([])
#    ax.plot(range(len(y)), y.cumsum())
    
    ax.hist(y,bins=y.max() - y.min())

    return ax

def distn_vis(assessment,df=gm,ax=None):
    """

    Get the mean and standard deviation for all problems for a given
    subset of assessments.

    """

    means = df.loc[assessment].mean(axis=1)
    stds = df.loc[assessment].std(axis=1)

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

def distaggn_vis(assessment, df=pm, ax = None):
    """

    Get the mean and standard deviation for a set of aggregated assessments
    (such as HW for all HW problems).

    The points matrix is used since summing points and then dividing by the
    total number of points in each class, since each class has the same
    weights, gives the fraction earned in that class.

    """

    means = df.loc[assessment].groupby(level=0).agg(np.sum).mean(axis=1)
    stds = df.loc[assessment].groupby(level=0).agg(np.sum).std(axis=1)
    ref = fdf.loc[assessment]['Grading Importance', 'Total'].groupby(level=0).agg(np.sum)
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
    ax.set_xlabel('Assessment')
    ax.set_ylabel('% of Assessment Points Scored')
    return ax

if __name__ == '__main__':
    assessment = 'HW', 1
    #x = dist1(assessment)
    #with open('assessment-scores.tex', 'w') as _:
    #    x.to_latex(_, index=False,
    #        columns=['ID','scores'])

    
    dist1_vis(assessment)
    distn_vis(assessment)
    distaggn_vis(assessment)
    plt.show()
