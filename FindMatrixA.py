import numpy as np
from pyibex import Interval, IntervalVector
from pyibex.pyibex import IntervalMatrix
import math
from scipy import special

# найти матрица А
# Br - радиальная компонента магнитного поля
#  Bz - аксиальная компонента магнитного поля
# 矩阵的同行元素之间用空格（或”,”）隔开；
# 矩阵的行与行之间用”;”（或回车符）隔开；

def find_matrix_B(r, z, a, I):
    c = 299792458
    eps = 1e-7

    sign = 1
    if r < 0:
        sign = -1

    r = np.abs(r)

    k_sqr = 4 * a * r / ((a + r) ** 2 + z ** 2)
    # k = 1.75
    k = np.sqrt(k_sqr)


    K = special.ellipk(k)
    E = special.ellipe(k)
    if r < eps:
        Br = 0
        Bz = 2 * np.pi * a ** 2 * I / (c * (a ** 2 + z ** 2) ** (3/2))
    else:
        Br = (I / c) * 2 * z / (r * np.sqrt((a + r) ** 2 + z ** 2)) * (
                    -K + E * (a ** 2 + r ** 2 + z ** 2) / ((a - r) ** 2 + z ** 2))
        if np.abs(r-a) < eps:
            r = a - eps
        Bz = (I / c) * 2 / (np.sqrt((a + r) ** 2 + z ** 2)) * (K + E * (a ** 2 - r ** 2 - z ** 2) / ((a - r) ** 2 + z ** 2))

    B = math.sqrt(Br**2+Bz**2)
    Br = sign * Br

    return Br, Bz, B

def find_matrix_A(I, probes, currents):
    n = len(probes)
    m = len(currents)
    Ar = np.zeros((n, m))
    Az = np.zeros((n, m))
    A = np.zeros((n, m))
    for i in range(n):
        for j in range(m):
            r = probes[i][0]
            z = probes[i][1]

            a = currents[j][0]  # 电荷球的半径
            h = currents[j][1]  # 电荷球的高度

            Br_1,Bz_1,B_1=find_matrix_B(r, z-h, a, I[j])

            Ar[i][j] = Br_1 / I[j]
            Az[i][j] = Bz_1 / I[j]
            A[i][j] = math.sqrt(Ar[i][j] ** 2 + Az[i][j] ** 2)
    return A


def rdnumpy(txtname):
    f = open(txtname,"r")
    line = f.readlines()
    lines = len(line)  # 行数
    columns = 0
    for l in line:
        le = l.strip('\n').split('\t')
        columns = len(le)  # 列

    A = np.zeros((lines, columns), dtype=float)
    A_row = 0
    for lin in line:
        list = lin.strip('\n').split('\t')
        A[A_row:] = list[0:columns]
        A_row += 1
    return A


def generate(n, m, real_data=False):
    I_vector = np.zeros((m, 1))
    for i in range (m):
        I_vector[i] = 1 + abs(np.random.rand()) * 5
    I = 1e6 * I_vector

    currents = []

    r_in = 0.125
    x_min = 0.1
    a,b = 0.15,0.3
    ellipse1 = lambda y : a + x_min + a * math.sqrt(1 - y * y / (b * b)) + r_in
    ellipse2 = lambda y : a + x_min - a * math.sqrt(1 - y * y / (b * b)) + r_in

    path = "./data/matrix_b.txt"
    limiter = rdnumpy(path)/100

    probes = []

    if real_data==True:
        probes = rdnumpy("./data/lim.txt")/10000

    r = 0.9
    if m % 2 == 0:
        step_current = 2 * (2 * b * r) / (m - 1)
    else:
        step_current = 2 * (2 * b * r) / (m - 2)
        currents.append([ellipse1(b), b])

    x1,x2=0,0
    for y in np.arange(-b*r,b*r,step_current) :
        x1 = ellipse1(y)
        x2 = ellipse2(y)
        new_current1 = [x1,y]
        new_current2 = [x2,y]
        currents.append(new_current1)
        currents.append(new_current2)


    return I, probes, currents





