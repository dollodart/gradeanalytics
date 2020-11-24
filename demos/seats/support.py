import numpy as np
from conn import conn_mat
from time import sleep

def optimize_rectangle_placement(x, nrows, ncols, penalty, temp, test = False):
    """                     

    The x vector has at index i the element j. The interaction energy
    due to the element j at index i with its neighbors at i-1, say a,
    and i+1, say b, must be given by penalty(j, a) and penalty(j, b).

    Assumes penalty returns 0 interaction if one or both of the inputs
    are 0, corresponding to empty seats.

    Because the number of students is generally small, a matrix
    containing all the interaction energies and a connectivity matrix
    can be calculated.

    This assumes all values in x are distinct or it doesn't
    matter. Insert student IDs and make the penalty function take
    student IDs as input rather than something associated with them if
    back-calculating is a concern.

    """

    nstudents = len(x) 
    nseats = nrows * ncols

    if ncols > nrows:
        nrows, ncols = ncols, nrows

    np.random.seed(20)
    ar = np.array(x + [0] * (nseats - nstudents))

    def calc(ar, penalty):
        I = np.zeros((nseats, nseats))
        for i in range(nseats):
            for j in range(nseats):
                I[i, j] = penalty(ar[i], ar[j])
            I[i, i] = 0
        return I

    if test:
        C = np.eye(nseats, nseats, -1) + np.eye(nseats, nseats, 1) # this is equivalent to a linear arrangement
        C[nseats - 1, 0] = 1
        C[0, nseats - 1] = 1
        min_energy = 338
        # periodic matrix (for circular arrangement)
        # this makes an idempotent matrix, C^2 = C
    else:
        C = conn_mat(nrows, ncols)
        min_energy = 592 # only for nrows = ncols = 3

    counter = 0

    I = calc(ar, penalty)

    while counter < nseats**2:
        p1 = np.random.randint(0, nseats)
        p2 = np.random.randint(0, nseats)
        while p1 == p2: 
            p2 = np.random.randint(0, nseats)

        e = (C * I).sum()
        ar[p1], ar[p2] = ar[p2], ar[p1]
        Io = I.copy()
        I = calc(ar, penalty)
        e2 = (C * I).sum()
        print(f'e={e2},e-emin={e2-min_energy}')
        arg = (e2 - e) / 2
        arg /= temp

#        print(np.exp(arg), counter); sleep(0.1)
        if np.exp(arg) > np.random.random_sample():
            counter += 1
        else:
            ar[p1], ar[p2] = ar[p2], ar[p1]
            I = Io

    seats = np.zeros((nrows,ncols))
    for counter, stu in enumerate(ar):
        x, y = counter % ncols, counter // ncols
        seats[y,x] = stu

    return seats


def optimize_circle_placement(r, penalty, temp = 1): 

    """

    The x vector has at index i the element j. The interaction energy
    due to the element j at index i with its neighbors at i-1, say a,
    and i+1, say b, must be given by penalty(j, a) and penalty(j, b).

    Convergence criterion is taken to be number of swaps equal to number of students.

    """

    n = len(r)
    counter = y = 0

    # initialization

    while counter < n**2:
        x = np.random.randint(0, n)
        while x == y:
            y = np.random.randint(0, n)

        p10 = penalty(r[x], r[(x + 1) % n])
        p20 = penalty(r[x - 1], r[x])
        p30 = penalty(r[y], r[(y + 1) % n])
        p40 = penalty(r[y - 1], r[y])
        e0 = p10 + p20 + p30 + p40

        p1 = penalty(r[x], r[(y + 1) % n])
        p2 = penalty(r[y - 1], r[x])
        p3 = penalty(r[y], r[(x + 1) % n])
        p4 = penalty(r[x - 1], r[y])
        e1 = p1 + p2 + p3 + p4

        arg = -(e1 - e0) / temp

        if np.exp(arg) > np.random.random_sample():
            r[x], r[y] = r[y], r[x]
            e0 = e1
            counter = 0
        else:
            counter +=1

    return r

if __name__ == '__main__':
    m = n = 3
    student_scores = list(range(1, m*n + 1)) # assume student scores are on a range
    penalty = lambda x, y: x*y 
    # for this penalty function, expect large numbers to be next to small numbers, medium numbers next to medium numbers

    # make a temperature based on the average interaction energy
    temp = 0
    for x in student_scores:
        for y in student_scores:
            temp += penalty(x,y)
    temp /= (m*n)**2
    temp /= 1 # in physical systems, the ambient thermal energy, e.g., at room temperature of 25 meV, 
    print(temp)
    # will be more than a factor of ten times less than, e.g., an adsorption energy

    # check energy calculation is the same between the two
    x = student_scores
    np.random.shuffle(x) 
    nseats = m*n
    nstudents = len(x)

    # compare energies calculated by two routines
#    egy = [penalty(i, j) for i, j in np.vstack((x, np.roll(x, -1))).transpose()]
#    egy = sum(egy)
#
#    ar = np.array(x + [0] * (nseats - nstudents))
    def calc(ar, penalty):
        I = np.zeros((nseats, nseats))
        for i in range(nseats):
            for j in range(nseats):
                I[i, j] = penalty(ar[i], ar[j])
            I[i, i] = 0
        return I
#
#    C = np.eye(nseats, nseats, -1) + \
#        np.eye(nseats, nseats, 1) # this is equivalent to a linear arrangement
#    C[0, -1] = 1
#    C[-1, 0] = 1
#    I = calc(ar, penalty)
#    egy2 = C*I
#    egy2 = egy2.sum()
#    print(egy, egy2/2)
#    assert egy == egy2 / 2

#    import itertools as it
#    e = []
#    C = conn_mat(m, n)
#    for ar in it.permutations(x):
#        I = calc(ar, penalty)
#        e.append( (ar,  (C*I).sum()) )


    # compare converged positions calculated by two routines
    ocp = optimize_circle_placement(student_scores, penalty, temp)
    print(ocp)
#    orp = optimize_rectangle_placement(student_scores, m, n, penalty, temp, test=True)
#    print(np.ravel(orp))
#
#    orp = optimize_rectangle_placement(student_scores, m, n, penalty, temp)
#    print(orp)
