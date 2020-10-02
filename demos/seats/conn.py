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
    #from pandas import DataFrame
    #DataFrame(I).to_latex('3-by-3.tex')
    return C