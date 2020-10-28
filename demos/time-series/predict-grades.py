import matplotlib.pyplot as plt
from datetime import date, datetime, timedelta
from gradeanalytics import full_data_frame as fdf, weighted_point_matrix as wpm
import pandas as pd
pd.plotting.register_matplotlib_converters()

def fraction_determined(from_date = None):
    if from_date is None:
        from_date = datetime.now()
    # calculate
    bl = fdf['Assessment Metadata', 'Date Assigned'] > cd
    fut = fdf[bl]
    past = fdf[~bl]
    cfut = (fut['Grading Importance', 'Weight'] *
             fut['Grading Importance', 'Total']).sum()
    cpast = (past['Grading Importance', 'Weight'] *
           past['Grading Importance', 'Total']).sum()
    frac = cpast / (cfut + cpast)
    return "Fraction of total grade thus far determined {:.2f}%".format(frac * 100)


def projected_scores(df,mode='project@date'):
    """

    Input: the data frame containing desired rows, over all time

    Output: projected scores at each time assuming equal fractional 

    """

    df = df.sort_values(by=('Assessment Metadata', 'Date Assigned'))
    x = df['Assessment Metadata', 'Date Assigned'].values
    scale = (df['Grading Importance', 'Weight'] *
             df['Grading Importance', 'Total']).cumsum(axis=0)

    if mode != 'project@date':
        scale = scale.max()
        ax.set_ylabel('Percent of Perfect End of Course Score')
    y = wpm.reindex(df.index).cumsum(axis=0)
    y = y.divide(scale, axis=0).values
    return x, y


def projected_scores_vis(df = fdf, ax = None, mode='project@date', absolute_scale = False): 
    """

    Predict end of course score assuming equal cumulative performance
    from time from_date to course end.  This is equivalent to taking the
    contribution (weights and points) at from_date and dividing it by
    the fraction of total contribution earned at from_date.

    """

    if ax is None:
        fig, ax = plt.subplots(nrows=1,ncols=1)

    x, y = projected_scores(df = df, mode = mode) 

    if mode != 'project@date':
        ax.set_ylabel('Percent of Perfect End of Course Score')
    else:
        ax.set_ylabel('Projected End of Course Score @ Date')

    ax.set_xlabel('Date')
    ax.plot(x, y * 100)
    ax.legend(wpm.columns)  # student ids
    if absolute_scale:
        ax.set_ylim((0, 100))
    plt.xticks(rotation=90)
    plt.tight_layout()
    return ax

def projected_scores_by_category(index_level, df = fdf):
    """

    Students may show consistently higher performance in some categories
    over others, e.g., quantitative or qualitative problems, or exams
    versus homeworks. Predict by category predicts the student grades by
    assuming equal fractional performance in each category.

    """

    xy = []
    for cd in df['Assessment Metadata','Date Assigned'].drop_duplicates().sort_values(): 
        sfdf = df[df['Assessment Metadata', 'Date Assigned'] < cd].sort_values(by=('Assessment Metadata', 'Date Assigned'))
        tot = tot_poss = 0
        for n, gr in sfdf.groupby(level=index_level):
            gr = gr.sort_values(by=('Assessment Metadata', 'Date Assigned'))
            x = gr['Assessment Metadata', 'Date Assigned']
            wt = (gr['Grading Importance', 'Weight'] *
                 gr['Grading Importance', 'Total'])
            scale = wt.cumsum(axis=0)
            y = wpm.reindex(gr.index).cumsum(axis=0)
            tot += y.max(axis=0)
            tot_poss += scale.max()
        try:
            xy.append( (cd, tot / tot_poss ) )
        except ZeroDivisionError:
            pass
    x, y = zip(*xy)
    y = pd.concat(y, axis=1)
    return x, y.transpose()

if __name__ == '__main__':
    cd = pd.Timestamp(date(year=2019,month=11,day=1))
    print(fraction_determined(cd))
    projected_scores_vis()
    x, y = projected_scores_by_category(0)
    plt.figure()
    for j in y.columns:
        plt.plot(x, y[j],label=j)
    plt.show()
