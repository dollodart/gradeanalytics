import numpy as np

#def circle_pairs(m):
#    dct = {}
#    for i in range(m):
#        dct[i] = [i - 1, (i + 1) // m]

def rectangle_pairs(m, p):
    """One can use modular arithmetic and store this as a lexicographical single array. """
    dct = {}
    for i in range(m):
        w = i > 0
        e = i < m - 1
        for j in range(p):
            n = j < p - 1
            s = j > 0
            nw = n & w
            ne = n & e
            sw = s & w
            se = s & e

            nn = []
            if w:
                nn.append((i - 1, j))
            if e:
                nn.append((i + 1, j))
            if n:
                nn.append((i, j + 1))
            if s:
                nn.append((i, j - 1))
            if nw:
                nn.append((i - 1, j + 1))
            if ne:
                nn.append((i + 1, j + 1))
            if sw:
                nn.append((i - 1, j - 1))
            if se:
                nn.append((i + 1, j - 1))
            dct[(i, j)] = nn
    return dct


def conn_mat(rpairs, nrows, ncols):
    mat = np.zeros((ncols * nrows, ncols * nrows))
    for p in rpairs.keys():
        ps = p[0] + ncols * p[1]
        for pp in rpairs[p]:
            pps = pp[0] + ncols * pp[1]
            mat[ps, pps] += 1
    return np.triu(mat)


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

    num_students = len(x) 

    if ncols > nrows:
        nrows, ncols = ncols,nrows

    np.random.seed(20)
    ar = np.array(x + [0] * (nrows * ncols - num_students))

    I = np.zeros((nrows * ncols, nrows * ncols))

    for i in range(nrows):
        for j in range(ncols):
            I[i, j] = penalty(ar[i], ar[j])
        I[i, i] = 0
    I = np.triu(I) # do not double count interactions

    rpd = rectangle_pairs(nrows, ncols)
    C = conn_mat(rpd, nrows, ncols)

    counter = 0

    while counter < (nrows * ncols)**2:
        p1 = np.random.randint(0, nrows * ncols)
        p2 = np.random.randint(0, nrows * ncols)
        # swap both the row and columns of the connectivity matrix to effectively swap positions
        # the final result of swap order is independent of the order of swapping
        # only two two columns and two rows need to be evaluated
        # since there are only nearest neighbor interactions

        arg = (C[p2]*I[p1] + C[p1]*I[p2] + C[:,p2]*I[:,p1] + C[:,p1]*I[:,p2]) \
        - (C[p1]*I[p1] + C[p2]*I[p2] + C[:,p1]*I[:,p1] + C[:,p2]*I[:,p2])
        arg = arg.sum()
        arg /= temp

        if np.exp(arg) < 0.5:
            C[p1], C[p2] = C[p2], C[p1]
            C[:, p1], C[:, p2] = C[:, p2], C[:, p1]
            counter = 0
            ar[p1], ar[p2] = ar[p2], ar[p1]
        else:
            counter += 1

    seats = np.zeros((nrows,ncols))
    for counter, stu in enumerate(ar):
        x, y = counter % nrows, counter // nrows
        seats[x,y] = stu

    return seats


def optimize_circle_placement(x, penalty, temp = 1): 

    """

    The x vector has at index i the element j. The interaction energy
    due to the element j at index i with its neighbors at i-1, say a,
    and i+1, say b, must be given by penalty(j, a) and penalty(j, b).

    """

    num = len(x)
    print(num)
    print()
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
            # p = int(e^x, -inf, y) = e^y
            # y = ln(p)
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

    ocp = optimize_circle_placement(student_scores, penalty, temp)
    print(ocp)
    orp = optimize_rectangle_placement(student_scores, m, n, penalty, temp)
    print(orp)
