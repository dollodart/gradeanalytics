import pandas as pd
import numpy as np
from gradeanalytics import grades as gm
from conn import Seat, construct_seats
from support import simulate
from conn import eval_energy

# gm = gm.loc['HW'] 
gm = gm.groupby(level=0).agg(np.mean)

z = gm.corr().abs()  
# correlation among student performances on all assesments

def penalty_func(i,j):
    if i > nstudents - 1 or j > nstudents - 1:
        return 0 # this is minimum correlation coefficient, empty seats
    return z[i].loc[j]

nstudents = gm.shape[1]

# make a temperature based on the differences in average energies
es = np.ravel(z.values)
diff_acc = 0
for x in es:
    for y in es:
        diff_acc += abs(x - y)
temp = diff_acc / len(es)**2
print(f'temperature is {temp:.4f}')

# assign student ids (circular arrangement)
#seats = [Seat(i, i + 1) for i in range(nstudents)]
#for s in seats:
#    s.adjs.extend([seats[(s.number + 1) % nstudents], seats[(s.number - 1) % nstudents]])
#
#seats = simulate(seats, penalty_func, kbt = temp)
#for s in seats:
#    print(s.number, s.sid, tuple((x.number, x.sid) for x in s.adjs))

# assign student ids (rectangular arrangement)
seats = construct_seats(6,6)
for s in seats:
    s.sid += 1

print(f'sids {",".join(f"{x}" for x in range(nstudents+1, 3*4 + 1))} are empty')
sseats = simulate(seats, penalty_func, kbt=temp)
for s in sseats:
    print(s.number, s.sid, [(x.number, x.sid) for x in s.adjs])

opt = eval_energy(sseats, penalty_func)
x = np.array(range(36))
x += 1
for _ in range(1000):
    np.random.shuffle(x)
    for c, s in enumerate(seats):
        s.sid = x[c]
    e = eval_energy(seats, penalty_func)
    de = e - opt
    if de < 0:
        print('found better solution in 1000 random samples'
              '\nfix the temperature or other simulation parameters')
