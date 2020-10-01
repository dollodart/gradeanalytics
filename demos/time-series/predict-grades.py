import matplotlib.pyplot as plt
from datetime import date, datetime, timedelta
from gradeanalytics import full_data_frame as fdf, weighted_point_matrix as wpm
import pandas as pd
pd.plotting.register_matplotlib_converters()

def predict(from_date = None, ax = None): 
    """

    Predict end of course score assuming equal cumulative performance
    from time from_date to course end.  This is equivalent to taking the
    contribution (weights and points) at from_date and dividing it by
    the fraction of total contribution earned at from_date.

    """

    if from_date is None:
        from_date = datetime.datetime.now()
    if ax is None:
        fig, ax = plt.subplots(nrows=1,ncols=1)

    bl = fdf['Assessment Metadata', 'Date Assigned'] > cd
    
    # calculate
    fut = fdf[bl]
    past = fdf[~bl]
    cfut = (fut['Grading Importance', 'Weight'] *
             fut['Grading Importance', 'Total']).sum()
    cpast = (past['Grading Importance', 'Weight'] *
           past['Grading Importance', 'Total']).sum()
    frac = cpast / (cfut + cpast)
    print("Fraction of total grade thus far determined {:.2f}%".format(frac * 100))

    # find what the projected value was at each time 
    sfdf = fdf.sort_values(by=('Assessment Metadata', 'Date Assigned'))
    x = sfdf['Assessment Metadata', 'Date Assigned'].values
    scale = (sfdf['Grading Importance', 'Weight'] *
             sfdf['Grading Importance', 'Total']).cumsum(axis=0)
    scale = scale 
    scale = 1
    y = wpm.reindex(sfdf.index).cumsum(axis=0)
    y = y.divide(scale, axis=0).values

    ax.set_xlabel('Date')
    #ax.set_ylabel('Projected End of Course Score @ Date')
    ax.set_ylabel('Percent of Perfect End of Course Score')
    ax.plot(x, y * 100)
    ax.legend(wpm.columns)  # student ids
    #ax.set_ylim((0, 100))
    plt.xticks(rotation=90)
    plt.tight_layout()
    return ax

if __name__ == '__main__':
    cd = pd.Timestamp(date(year=2019,month=11,day=1))
    predict(from_date = cd)
    plt.show()
