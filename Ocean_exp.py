from ipyleaflet import Map, basemaps, basemap_to_tiles, Rectangle, Polyline, LayersControl
from matplotlib import cm
import matplotlib.pylab as plt
from mpl_toolkits import mplot3d

import pandas as pd
import numpy as np
import pathlib as pl
import datetime

import csv
import math
import random

from pyibex import *
from SIVIA import *

SQR = Function("x1", "x2", "( max ( 0, sign(x1 * x2) * min(x1^2, x2^2) ), max(x1^2, x2^2) )")
# SQRT = Function("x1", "x2", "(min(x1^(1/2),x2^(1/2)), max(x1^(1/2), x2^(1/2)))")
MINUS = Function("x1", "x2", "y1", "y2", "(x1 - y2, x2 - y1)")
PLUS = Function("x1", "x2", "y1", "y2", "(x1 + y1, x2 + y2)")


class Ocean_exp:
    def __init__(self, m):
        self.l_m = m
        self.Bp = IntervalVector(len(m), [0, 100])

    def test(self, X):
        Xm = IntervalVector(len(self.l_m))
        Xp = IntervalVector(len(self.l_m))

        for i, m in enumerate(self.l_m):
            dX0 = MINUS.eval_vector(IntervalVector([
                [X[0].lb(), X[0].ub()],
                [X[0].lb(), X[0].ub()],
                [m[0].lb(), m[0].lb()],
                [m[0].ub(), m[0].ub()]
            ]))
            # print("dX0", dX0)
            dX1 = MINUS.eval_vector(IntervalVector([
                [X[1].lb(), X[1].ub()],
                [X[1].lb(), X[1].ub()],
                [m[1].lb(), m[1].lb()],
                [m[1].ub(), m[1].ub()]
            ]))
            # print("dX1", dX1)
            S0 = SQR.eval_vector(IntervalVector([
                [dX0[0].lb(), dX0[0].ub()],
                [dX0[1].lb(), dX0[1].ub()]
            ]))
            # print("S0", S0)
            S1 = SQR.eval_vector(IntervalVector([
                [dX1[0].lb(), dX1[0].ub()],
                [dX1[1].lb(), dX1[1].ub()]
            ]))
            # print("S1", S1)
            N2 = PLUS.eval_vector(IntervalVector([
                [S0[0].lb(), S0[0].ub()],
                [S0[1].lb(), S0[1].ub()],
                [S1[0].lb(), S1[0].ub()],
                [S1[1].lb(), S1[1].ub()]
            ]))
            # print("N2",N2)
            # K = SQRT.eval_vector(IntervalVector([
            #     [N2[0].lb(), N2[0].ub()],
            #     [N2[1].lb(), N2[1].ub()]
            # ]))
            Xm[i], Xp[i] = N2[0], N2[1]
            # Xm[i], Xp[i] = K[0], K[1]
            # print("K", K)
        Xub = Xm | Xp
        # print("Xub", Xub)

        if self.Bp.is_disjoint(Xub):
            return IBOOL.OUT
        elif Xub.is_subset(self.Bp):
            return IBOOL.IN
        else:
            return IBOOL.UNK

def ocean():

    sss_df = pd.read_csv('./data/side-scan-sonar-index.csv', sep=';', low_memory=False)
    # print(sss_df.head())
    sss_latitude = sss_df['Latitude'].to_numpy(dtype=np.float32)
    sss_longitude = sss_df['Longitude'].to_numpy(dtype=np.float32)
    m = []
    new_latitude =[]
    new_longitude = []
    for i in range(len(sss_latitude)):
        new_latitude.append(sss_latitude[i]+ 0.1 * i)
        new_longitude.append(sss_longitude[i] + 0.05 * i)
    for i in range(len(sss_latitude)):
        m.append([Interval(new_latitude[i]).inflate(0.1), Interval(new_longitude[i]).inflate(0.1)])
    fig, ax = plt.subplots(nrows=1, ncols=1)
    plt.plot(new_longitude, new_latitude, color='k')
    plt.plot(new_longitude[0], new_latitude[0], color='g', marker='.', markersize=20)
    plt.plot(new_longitude[-2], new_latitude[-2], color='r', marker='.', markersize=20)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.axis('equal')
    plt.figure()
    X0 = IntervalVector([[30,80], [-20, 10]])
    eps = 0.5
    L_clear, L_dark,L_too_small = SIVIA(X0, Ocean_exp(m), eps)
    draw_SIVIA(X0,L_clear, L_dark, L_too_small)
    x_set = []
    y_set = []
    for item in m:
        ax = plt.gca()
        x0 = item[0][0]
        y0 = item[1][0]
        x_set.append(x0)
        y_set.append(y0)
        width = item[0][1] - item[0][0]
        height = item[1][1] - item[1][0]
        ax.add_patch(patches.Rectangle(
            (x0, y0),  # (x,y)
            width,  # width
            height,
            edgecolor='black',
            facecolor='black',
            fill=True)
        )
    plt.plot(x_set, y_set, '-', linewidth=0.1)
    plt.show()