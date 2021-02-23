from conn import Seat, construct_seats, eval_energy_diff, eval_energy
import numpy as np
import numpy.random as r

energy = lambda x, y: x*y

def until_minimum(seats, known_minimum, kbt):
    e0 = eval_energy(seats, energy)
    n = len(seats)
    y = 0
    unsuccesful_iters = 0
    while e0 > known_minimum: # known minimum
        x = r.randint(0,n)
        while x == y:
            y = r.randint(0, n)

        de = eval_energy_diff(seats, y, x, energy=energy)
        if de > 0 and np.exp(-de/kbt) < r.random():
            seats[x].sid, seats[y].sid = seats[y].sid, seats[x].sid
            #assert de == e0 - eval_energy(seats,energy=energy)
            e0 -= de
            print(e0)
        else:
            unsuccesful_iters += 1
            if unsuccesful_iters % 100 == 0:
                kbt *= 0.9 # simulated annealing
            elif unsuccesful_iters > 1000:
                print(f'couldn\' find minimum {known_minimum}\n'
                        f'found {e0} which is {(known_minimum - e0)/known_minimum*100:.1f}% close')
                return seats
        
    return seats

seats = construct_seats(3,3)
for s in seats:
    s.sid += 1
seats = until_minimum(seats, 296, kbt=100)
for s in seats:
    print(s.number, s.sid, [(x.number, x.sid) for x in s.adjs])

seats = [Seat(i, i + 1) for i in range(9)]
for s in seats:
    s.adjs.extend([seats[(s.number + 1) % 9], seats[(s.number - 1) % 9]])
print()
seats = until_minimum(seats, 169, kbt=40)
for s in seats:
    print(s.number, s.sid, [(x.number, x.sid) for x in s.adjs])
