import numpy
import numpy as np
points = "15,15,15,15,19,20,20,20,15,20,17,16,20"\
         ",16,15,18,15,17,55,65,62,57,65,206,210"
points = np.array([float(x) for x in points.split(',')])
r1 = np.random.random(size=(len(points),30))
v = points[:,np.newaxis]*np.exp(-r1**2)
assert (v < points[:,np.newaxis]).all()
v = np.floor(v)
np.savetxt('rdata.csv',v,delimiter=',')
