"""

This calculates the per point weighting for each class given a set of
assessments grouped in classes having given points such that the each
assessment class has a given contribution to the final grade.

The total contribution to the end grade of any given assessment is

f_i = N_i w_i/sum(N_i w_i,i,all)

To obtain

sum(f_i,i,class) = c

The following is required for a uniform weight w_class:

w_class = sum(N_i w_i, i, ~class)/sum(N_i,i,class) * c/(1-c)

If the weights of three classes are to be found so that the class
contribution of each is a desired value, then letting sum(N_i,i,A) = NA
be the total number of points in a class A,

wA*NA/(wA*NA+wB*NB+wC*NC) = c1
wB*NB/(wA*NA+wB*NB+wC*NC) = c2
wC*NC/(wA*NA+wB*NB+wC*NC) = c3

From which the linear system of equations,

(1-c1)NA*wA - c1 NB*wB - c1 NC*wC = 0
-c2 NA*wA + (1-c2)NB*wB - c2 NC*wC = 0
-c3 NA*wA - c3 NB*wB + (1-c3)NC*wC = 0

This is Ax=0, which will have non-trivial solutions only if A is not
full rank.

Note that c1+c2+c3=1. let NA*wA=xA be the variable, since they always
appear as a product, then

(1-c1)*xA - c1*xB - c1*xC = 0
-c2*xA + (1-c2)*xB - c2*xC = 0
-(1-c1-c2)*xA - (1-c1-c2)*xB + (c1+c2)*xC = 0

The third equation is the negative of the sum of the first two
equations, so that there is

(1-c1)*xA - c1*xB - c1*xC = 0
-c2*xA + (1-c2)*xB - c2*xC = 0

Let xC = 1, then

(1-c1)*xA - c1*xB = c1
-c2*xA + (1-c2)*xB = c2

Which may be solved for by standard methods.

"""

from gradeanalytics import data_frame as df
import numpy as np

N = df['Grading Importance', 'Total'].groupby(level=0).agg(sum)
i = N.index
N = N.values
c = np.array([3, 1, 2, 2])  # final, Hw, Midterm, Quiz (alphabetical order)
c = c / c.sum()
z = np.zeros((c.size, c.size))
z[:] = -c
z += np.eye(c.size)
z = z.transpose()
z = z[:c.size - 1]
xs = np.linalg.solve(z[:, :c.size - 1], -z[:, c.size - 1])
xs = np.append(xs, 1)
ws = xs / N
ws /= ws.min()

print("ass.\tcomp.\tweight\tnum. pts.".expandtabs(10))
for x in zip(i, c, ws, N):
    print("{}\t{:.2f}\t{:.2f}\t{:.2f}".format(*x).expandtabs(10))

# check
ccheck = ws * N / (ws * N).sum()
assert np.allclose(ccheck, c), "fails equality ws * N / sum(ws * N)"
