"""

Problem from intro statistics textbook by Ross (section 3.3 example
3c).  As an extension, predict the variability in scores introduced
provided a student has a fixed probability of knowing the answer to
every question, for a fixed number of options per questions and a fixed
number of questions.  

The first extension is solved for the mean statistic, in the long limit
(large number of problems), as p + (1-p)/m since the probabily p is the
fraction of problems one knows the answer to and will answer correctly,
1-p is the fraction of problems which will be guessed, assuming the
student is incapable of excluding some answers and randomly guesses this
has 1/m probability of being correct. 

The standard deviation of the binomial distribution as applied to
problems for which the answer is not known is sqrt(n*1/m*(1-1/m)), maybe
sqrt((1-p)*n*1/m*(1-1/m)) where n is the total number of trials since
only 1-p of them will be guesses. The variance is a non-linear operator
so it isn't as simple to calculate. If the standard deviation is scaling
as sqrt(n), then note the fractional standard deviation is scaling as
1/sqrt(n), and vanishes with increasing n, hence longer tests have less
inaccuracy due to random cause variance.

"""


import matplotlib.pyplot as plt
from numpy import sqrt

def pkbc(m, p):
    return m * p / (1 + (m - 1) * p)

x = 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100
print(f'm,p,prob')
fig, axs = plt.subplots(nrows=3)
for m in 2, 3, 4, 5, 6, 10, 20:
    l = []
    ll = []
    lll = []
    for p in range(0, 11):
        p /= 10
        pp = pkbc(m, p)
        print(f'{m},{p*100:.1f},{pp*100:.1f}')
        l.append(100*pp)
        ll.append(100*(p + (1-p)/m))
        lll.append(100*sqrt((1-p)/m*(1-1/m)))
    axs[0].plot(x, l, label=m)
    axs[1].plot(x, ll, label=m)
    axs[2].plot(x, lll, label=m)

axs[2].set_xlabel('Probability Know Answer')
axs[0].set_ylabel('Probability Knew Answer\nProvided Correct')
axs[1].set_ylabel('Expected Score $X$')
axs[2].set_ylabel('Expected $\sigma / \sqrt{n}$\n $=\\varepsilon \sqrt{n}$')
axs[0].set_title('Legend Number Options')
axs[0].plot([0, 100], [100, 100], 'k-', label='ideal')
axs[0].legend()#; axs[1].legend(); axs[2].legend()
axs[1].plot([0,100], [0,100], 'k-', label='ideal')
axs[2].plot([0,100], [0,0], 'k-', label='ideal')
plt.show()
