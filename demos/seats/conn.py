import numpy as np

def conn_mat(m,n):
    p = m*n
    C = np.zeros((p,p))

    for i in range(p):
        c1 = i % m  # column index in physical space
        c2 = i // m # row index in physical space
        #print(i, c1, c2)
        if c1 == m - 1 and c2 == n - 1: # bot right
            #print('br')
            C[i, i - 1] = 1
            C[i, i - 1 - m] = 1
            C[i, i - m]  = 1
        elif c1 == 0 and c2 == n - 1: # bot left
            #print('bl')
            C[i, i + 1]  = 1
            C[i, i - m]  = 1
            C[i, i - m + 1] = 1
        elif c1 == m - 1 and c2 == 0: # top right
            #print('tr')
            C[i, i - 1] = 1
            C[i, i + m] = 1
            C[i, i + m - 1] = 1
        elif c1 == 0 and c2 == 0: # top left
            #print('tl')
            C[i, i + 1] = 1
            C[i, i + m] = 1
            C[i, i + m + 1] = 1
        elif c1 > 0 and c2 == n - 1: # bot edge
            #print('be')
            C[i, i + 1] = 1
            C[i, i - m] = 1
            C[i, i - m + 1] = 1
            C[i, i - m - 1] = 1
            C[i, i - 1] = 1
        elif c1 > 0 and c2 == 0: # top edge
            #print('te')
            C[i, i + 1] += 1
            C[i, i + m] += 1
            C[i, i + m + 1] = 1
            C[i, i + m - 1] = 1
            C[i, i - 1] = 1
        elif c1 == m - 1 and c2 > 0:  # right edge
            #print('re')
            C[i, i + m] = 1
            C[i, i - m] = 1
            C[i, i - 1] = 1
            C[i, i + m - 1] = 1
            C[i, i - m - 1] = 1
        elif c1 == 0 and c2 > 0: # left edge
            #print('le')
            C[i, i + m] = 1
            C[i, i - m] = 1
            C[i, i + 1] = 1
            C[i, i + m + 1] = 1
            C[i, i - m + 1] = 1
        else: # interior
            #print('in')
            C[i, i + 1] = 1
            C[i, i - m + 1] = 1
            C[i, i - m] = 1
            C[i, i - m - 1] = 1
            C[i, i - 1] = 1
            C[i, i + m + 1] = 1
            C[i, i + m] = 1
            C[i, i + m - 1] = 1
    return C

class Seat:
    def __init__(self, number, sid = None):
        self.number = number
        if sid is None:
            self.sid = number
        else:
            self.sid = sid
        self.adjs = []
    def __eq__(self, other):
        return self.number == other.number

def construct_seats(m, n):
    """Return a list of Seat objects for the given rectangular geometry."""
    C = conn_mat(m, n)
    seats = [Seat(x) for x in range(C.shape[1])]
    for counter, row in enumerate(C):
        for counter2, value in enumerate(row):
            if value > 0:
                seats[counter].adjs.append(seats[counter2])
    return seats

energies = np.outer(range(10),range(10))
assert (energies == energies.transpose()).all()
def test_energy(i, j):
    return energies[i,j]

# evaluate energy
def eval_energy(seats, energy=test_energy):
    e = 0
    for s in seats:
        for a in s.adjs:
            e += energy(s.sid, a.sid)
    return e / 2

def eval_energy_diff(seats, i, j, energy=test_energy):
    """

    Evaluate energy difference of a hypothetical swap.  Applies in the
    case the two seats being swapped share neighbors, are neighbors, or
    are the same.

    """
    e1 = e2 = 0
    si = seats[i]
    sj = seats[j]
    for s in si.adjs:
        e1 += energy(s.sid, si.sid)
        if s == sj:
            e2 += energy(s.sid, si.sid)
        else:
            e2 += energy(s.sid, sj.sid)
    for s in sj.adjs:
        if s == si:
            e2 += energy(s.sid, sj.sid)
        else:
            e2 += energy(s.sid, si.sid)
        e1 += energy(s.sid, sj.sid)
    return e1 - e2

if __name__ == '__main__':
    C1 = conn_mat(3,3)
    C2 = conn_mat(3,4)
    C3 = conn_mat(4,3)
    print(C1, C2, C3, sep='\n')

    assert (C1 == C1.transpose()).all()
    assert (C2 == C2.transpose()).all()
    assert (C3 == C3.transpose()).all()

    seats = construct_seats(3, 3)

    # swap seats, test energy evaluation
    for i,j in (0,1), (0,5), (7,8), (3,4):
        e0 = eval_energy(seats)
        seats[i].sid, seats[j].sid = seats[j].sid, seats[i].sid
        e1 = eval_energy(seats)
        assert e1 - e0 == eval_energy_diff(seats, i, j)
        seats[i].sid, seats[j].sid = seats[j].sid, seats[i].sid
        e0again = eval_energy(seats)
        assert e0 == e0again
        assert e0 - e1 == eval_energy_diff(seats, i, j)
        seats[i].sid, seats[j].sid = seats[j].sid, seats[i].sid

#    from pandas import DataFrame
#    DataFrame(C1,dtype=int).to_latex('3-by-3.tex')
