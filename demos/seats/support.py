from conn import Seat, construct_seats, eval_energy_diff, eval_energy
import numpy as np
import numpy.random as r

def simulate(seats, energy_func, known_minimum = None, kbt = 1):
    e0 = eval_energy(seats, energy_func)
    n = len(seats)
    y = 0
    unsuccesful_iters = 0
    if known_minimum is None:
        ehist = []
        def evaluator(e):
            ehist.append(e)
            if len(ehist) > n:
                diff = sum(abs(ehist[-(i+1)] - ehist[-i]) for i in range(n))
                if 0 < diff < 1e-2*n*kbt:
                    return False
            return True
    else:
        evaluator = lambda e: e > known_minimum

    maxiters = n**4
    while evaluator(e0): # known minimum
        x = r.randint(0,n)
        while x == y:
            y = r.randint(0, n)

        de = eval_energy_diff(seats, y, x, energy_func=energy_func)
        if de > 0 and np.exp(-de/kbt) > r.random():
            seats[x].sid, seats[y].sid = seats[y].sid, seats[x].sid
            e0 -= de
            unsuccesful_iters = 0
        else:
            unsuccesful_iters += 1
            if unsuccesful_iters % (maxiters // 10) == 0:
                kbt *= 0.9 # simulated annealing
            elif unsuccesful_iters > maxiters:
                if known_minimum is not None:
                    print(f'couldn\'t find minimum {known_minimum}\n'
                            f'found {e0} which is {(known_minimum - e0)/known_minimum*100:.1f}% close')
                else:
                    print(f'{n**4} iterations without transition\n'
                          f'quitting')
                return seats
        
    return seats


if __name__ == '__main__':
    exe_func = lambda x, y: x*y

    seats = construct_seats(3,3)
    for s in seats:
        s.sid += 1
    seats = simulate(seats, exe_func, known_minimum = 296, kbt=100)
    for s in seats:
        print(s.number, s.sid, [(x.number, x.sid) for x in s.adjs])

    seats = [Seat(i, i + 1) for i in range(9)]
    for s in seats:
        s.adjs.extend([seats[(s.number + 1) % 9], seats[(s.number - 1) % 9]])
    print()
    seats = simulate(seats, exe_func, kbt=40)
    #seats = simulate(seats, exe_func, known_minimum=169, kbt=40)
    for s in seats:
        print(s.number, s.sid, [(x.number, x.sid) for x in s.adjs])
