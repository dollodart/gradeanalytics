from numpy.random import random

n = 20 # sample size
nn = 20 # number samples
m = 5
avg = 0
p = 0.5
for j in range(nn):
    correct = 0
    for i in range(n):
        p1 = random()
        if p1 < p: # know answer
            correct += 1
        else:
            p2 = random()
            if p2 < 1/m:
                correct += 1
    print(correct/n)
    avg += correct/n

print()
print(avg/nn)
print(p + (1-p)/m)

