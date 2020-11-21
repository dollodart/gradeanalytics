import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from gradeanalytics import grades as gm,\
        true_grades as tgm,\
        student_frame as sf

from scipy.stats import ttest_ind
from statsmodels.stats.multicomp import pairwise_tukeyhsd

def democorr(field, ax=None):
    """

    Correlates student performance with various demographic fields,
    either continuous (in which case there is one covariance and two
    variances) or discrete (in which case there is only one variance).

    """

    if ax is None:
        fig, ax = plt.subplots(nrows=1,ncols=1)

    sm = tgm.sum() * 100.
    sf['grades'] = sm

    if isinstance(field, list):
        g = sf.groupby(field)
        g = g.agg(np.mean)
        g = g.sort_values(by='grades')
        if len(field) > 1:
            g.index = ['-'.join(x) for x in g.index]
        ax.plot(g['grades'], 'o')
        ax.set_title(f"Grades std dev with\n"
                     f"grouping by {'-'.join(field)} = "
                     f"{g['grades'].std():.2f}%")
    else:
        if sf.dtypes[field] == np.dtype('O'):
            g = sf.groupby(field)
            g = g.agg(np.mean)
            g = g.sort_values(by='grades')
            ax.plot(g['grades'], 'o')
            ax.set_title(f"Grades std dev with\n"
                         f"grouping by {field} = {g['grades'].std():.2f}%")
        else:
            # for fields with floats, like income, there is a correlation (which is
            # related to covariance)
            ax.plot(sf[field], sf['grades'], 'o')
            ax.set_title(f"Pearson correlation of grades"
                         f"with field {field} is {sf['grades'].corr(sf[field]):.2f}")

    ax.set_ylim((0, 100))  # absolute fractional scale
    return ax

def demogend(income_factors_func, ax=None):    

    """
    Performance by gender accounting for income.
    """

    if ax is None:
        fig, ax = plt.subplots(nrows=1, ncols=1)

    sm = tgm.sum()
    sf['dwgrades'] = sm*sf['income'].map(income_factors)
    g = sf.groupby('gender')
    y = g['dwgrades'].agg(np.mean)
    ax.bar(y.index, y.values)
    # plt.ylim((0,100)) #absolute fractional scale
    tt = ttest_ind(sf['dwgrades'][sf['gender'] == 'female'].values
            , sf['dwgrades'][sf['gender'] == 'male'].values)
    return tt, ax

def demorace(income_factors_func, ax=None):
    """

    After accounting for differences in socioeconomic background to
    the average, determine if there is a statistically significant
    difference in performance. Visually, this is seeing
    if the scores by race, after multiplying by the appropriate factors,
    lie on a horizontal line. Rigorously, the simultaneous Tukey t-test
    is done.

    To extend this to find atypical differences in races, the
    differences must be compared to known differences in races at a
    national level. For example, if there is some continuous function
    giving a correction not just as a function of income but also for
    demographic indicators such as race, then applying that handicap and
    some factor for each race would give the simultaneous t-test the
    ability to detect atypical differences (and hence possible racial
    bias in instruction or grading).

    """


    if ax is None:
        fig, ax = plt.subplots(nrows=1, ncols=1)

    # ideally this would be done by broadcasting using a series or dictionary,
    # since it is categorical and not a continuous function
    sm = tgm.sum()
    sf['dwgrades'] = sm / sf['income'].map(income_factors)
    tukt = pairwise_tukeyhsd(sf['dwgrades'], 
        sf['race'] + '-' + sf['ethnicity'])

    g = sf.groupby(['race','ethnicity'])
    y = g['dwgrades'].agg(np.mean)
    ax.plot(y.index.map('-'.join), y.values, 'o')
    # ax.set_ylim((0,100)) #absolute fractional scale
    return tukt, ax

if __name__ == '__main__':
    field = ['race', 'ethnicity']
    democorr(field)
    def income_factors(x): 
        return 1 + (x - 30000.) / 30000. if x < 30000. else 1
    tt, _ = demogend(income_factors)
    print(tt.pvalue)
    tt, _ = demorace(income_factors)
    print(tt.summary())

    plt.show()
