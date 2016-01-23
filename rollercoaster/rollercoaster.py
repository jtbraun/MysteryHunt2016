import numpy as np
import sys

def test_triangular_mesh():
    """An example of a cone, ie a non-regular mesh defined by its
        triangles.
    """
    n = 8
    t = numpy.linspace(-numpy.pi, numpy.pi, n)
    z = numpy.exp(1j * t)
    x = z.real.copy()
    y = z.imag.copy()
    z = numpy.zeros_like(x)

    triangles = [(0, i, i + 1) for i in range(1, n)]
    x = numpy.r_[0, x]
    y = numpy.r_[0, y]
    z = numpy.r_[1, z]
    t = numpy.r_[0, t]

    return triangular_mesh(x, y, z, triangles, scalars=t)


grid = np.array([
    [4,2,1,-3],
    [2,1,3,4],
    [3,4,2,1],
    [1,3,4,-2],
])


if True:
    grid = np.array([
        -5,	-7,	4,	3,	2,	-8,	-9,	-10,	-6,	-1,
        -9,	5,	1,	6,	3,	7,	8,	4,	2,	10,
        -8,	4,	10,	7,	6,	5,	1,	2,	3,	9,
        -7,	1,	2,	-10,	-8,	-9,	3,	6,	5,	4,
        -6,	-9,	5,	-4,	-10,	2,	7,	8,	-1,	3,
        2,	3,	6,	-8,	-9,	1,	-10,	7,	4,	5,
        3,	6,	7,	-9,	-1,	4,	2,	5,	-10,	-8,
        4,	2,	-9,	-1,	-5,	-10,	-6,	3,	-8,	-7,
        -10,	8,	3,	5,	7,	6,	4,	1,	-9,	-2,
        -1,	-10,	8,	2,	-4,	-3,	-5,	-9,	-7,	-6]).reshape((10,10))

P = []
T = []
C = []

def trans(p):
    return (-p[1], p[0], p[2])

def addpt(p, color):
    r = len(P)
    C.append(color)
    P.append(trans(p))
    return r

def addtri(a,b,c, color=0):
    t = (addpt(a,color), addpt(b,color), addpt(c,color))
    T.append(t)

def addquad(a, b, h):
    d = (a[0], a[1], h)
    c = (b[0], b[1], h)
    addtri(a, b, c, color=0.5)
    addtri(c, d, a, color=0.5)

def addsq(x, y, z):
    base = [(x, y, 0),
            (x+1, y, 0),
            (x+1, y+1, 0),
            (x, y+1, 0),]
    draw_quad = True

    h = -z if draw_quad else 0
    top = [(x, y, h),
            (x+1, y, h),
            (x+1, y+1, h),
            (x, y+1, h),]

    tip = (x+0.5, y+0.5, z)
    if (z >= 0):
        addtri(base[0], base[1], tip)
        addtri(base[1], base[2], tip)
        addtri(base[2], base[3], tip)
        addtri(base[3], base[0], tip)
    else:
        addquad(base[0], base[1], h)
        addquad(base[1], base[2], h)
        addquad(base[2], base[3], h)
        addquad(base[3], base[0], h)
        addtri(top[0], top[1], top[2], color=0.5)
        addtri(top[2], top[3], top[0], color=0.5)

for rowi, row in enumerate(grid):
    for coli, val in enumerate(row):
        addsq(rowi, coli, val)




x = np.array([1,0])
y = np.array([0,1])
paths = [
    [(0,0), 2*x, y, x, y, -x, y,
     -2*x, -y, x, -y, -x, -y]
]
path = [
    (2, 0),
     1, 1, 4, 2, -2, 2, 1, 2, 1, -3, 2, 2, -1, 2, -3, -1, -2, 1, 1, 1, -2, -1, -1, -2, 1, -3, -1, 1, -1, -2, 1, -1, 1, -1
]


from mayavi.mlab import *

points = []
p = np.array(path[0])
for i, length in enumerate(path[1:]):
    direction = x if 0 == i % 2 else y

    direction  = direction * np.sign(length)
    length = np.abs(length)

    print "GOING", length * direction, "STARTING AT", p
    for i in xrange(length):
        z = grid[-1-p[1]][p[0]]
        points.append( (p[0], -p[1], z) )
        p += direction
z = grid[-1-p[1]][p[0]]
points.append( (p[0], -p[1], z) )

points = np.array(points)
x = points[:, 0] + 0.5
y = points[:, 1] + 0.5 + 9.
z = points[:, 2]
plot3d(-x, y, np.abs(z), color=(0., 1., 0.))

if True:
    points = np.array(P)
    x = points[:,0]
    y = points[:,1]
    z = points[:,2]
    triangular_mesh(x,y,z, T, scalars=C)

show()
