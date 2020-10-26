import numpy as np
from conn import conn_mat

def optimize_rectangle_placement(x, nrows, ncols, penalty, temp):
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

#    rpd = rectangle_pairs(nrows, ncols)
#    C = conn_mat(rpd, nrows, ncols)
    C = np.eye(nseats, nseats, -1) + np.eye(nseats, nseats, 1) # this is equivalent to a linear arrangement
    # periodic matrix (for circular arrangement)
    C[nseats - 1, 0] = 1
    C[0, nseats - 1] = 1
    # this makes an idempotent matrix, C^2 = C

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
        arg = (e2 - e) / 2
        arg /= temp

        if np.exp(arg) < 0.5:
            counter = 0
        else:
            ar[p1], ar[p2] = ar[p2], ar[p1]
            I = Io
            counter += 1

    seats = np.zeros((nrows,ncols))
    for counter, stu in enumerate(ar):
        x, y = counter % ncols, counter // ncols
        seats[y,x] = stu

    return seats


def optimize_circle_placement(x, penalty, temp = 1): 

    """

    The x vector has at index i the element j. The interaction energy
    due to the element j at index i with its neighbors at i-1, say a,
    and i+1, say b, must be given by penalty(j, a) and penalty(j, b).

    """

    num = len(x)
    egy = [penalty(i, j) for i, j in np.vstack((x, np.roll(x, -1))).transpose()]
    sm = sum(egy)
    mxm = np.argmax(egy)
    mnm = np.argmin(egy)
    counter = 0

    while True:
        mxm = np.random.randint(0, num)
        mnm = np.random.randint(0, num)

        sm0 = sm
        sm -= egy[mxm] + egy[mxm - 1] + egy[mnm] + egy[mnm - 1]
        x[mxm], x[mnm] = x[mnm], x[mxm]

        p1 = penalty(x[mxm], x[(mxm + 1) % num])
        p2 = penalty(x[mxm - 1], x[mxm])
        p3 = penalty(x[mnm], x[(mnm + 1) % num])
        p4 = penalty(x[mnm - 1], x[mnm])

        arg = (sm + p1 + p2 + p3 + p4 - sm0) / temp
        if np.exp( arg ) < 0.5:
            egy[mxm] = p1
            egy[mxm - 1] = p2
            egy[mnm] = p3
            egy[mnm - 1] = p4
            counter = 0
        else:
            x[mnm], x[mxm] = x[mxm], x[mnm]
            counter += 1

        sm += egy[mxm] + egy[mxm - 1] + egy[mnm] + egy[mnm - 1]
        if counter > num**2:
            break

    return x

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
    temp /= 10 # in physical systems, the ambient thermal energy, e.g., at room temperature of 25 meV, 
    # will be more than a factor of ten times less than, e.g., an adsorption energy

    # check energy calculation is the same between the two
    x = student_scores
    np.random.shuffle(x) 
    nseats = m*n
    nstudents = len(x)

    egy = [penalty(i, j) for i, j in np.vstack((x, np.roll(x, -1))).transpose()]
    egy = sum(egy)

    ar = np.array(x + [0] * (nseats - nstudents))
    def calc(ar, penalty):
        I = np.zeros((nseats, nseats))
        for i in range(nseats):
            for j in range(nseats):
                I[i, j] = penalty(ar[i], ar[j])
            I[i, i] = 0
        return I

    C = np.eye(nseats, nseats, -1) + \
        np.eye(nseats, nseats, 1) # this is equivalent to a linear arrangement
    C[0, -1] = 1
    C[-1, 0] = 1
    I = calc(ar, penalty)
    egy2 = C*I
    egy2 = egy2.sum()
    print(egy, egy2/2)
    assert egy == egy2 / 2


    ocp = optimize_circle_placement(student_scores, penalty, temp)
    print(ocp)
    orp = optimize_rectangle_placement(student_scores, m, n, penalty, temp)
    print(np.ravel(orp))
    #orp = optimize_rectangle_placement(student_scores, m + 1, n, penalty, temp)
    #print(np.ravel(orp))
