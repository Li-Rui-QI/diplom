from enum import Enum

from matplotlib import patches

from pyibex import IntervalVector, LargestFirst
from collections import deque
import matplotlib.pyplot as plt



class IBOOL(Enum):
    IN = 0
    OUT = 1
    MAYBE = 2
    UNK = 3
    EMPTY = 4

def SIVIA(X0, test, eps):
    stack = deque([IntervalVector(X0)])
    L_clear = deque()
    L_dark = deque()
    L_too_small = deque()
    lf = LargestFirst(eps / 2.0)
    i = 0
    while len(stack) > 0:
        i = i + 1
        X = stack.popleft()
        t = test.test(X)

        if t == IBOOL.IN:
            L_clear.append(X)
        elif t == IBOOL.OUT:
            L_dark.append(X)
        else:
            if X.max_diam() > eps:
                (X1, X2) = lf.bisect(X)
                stack.append(X1)
                stack.append(X2)
            else:
                L_too_small.append(X)
    print("Number of tests : %d" % i)
    return L_clear, L_dark, L_too_small

def draw_SIVIA(L_clear: deque, L_dark: deque,  L_too_small: deque):
    ax = plt.gca()
    while len(L_clear) > 0: # red
        X = L_clear.popleft()
        x0 = X[0][0]
        y0 = X[1][0]
        width = X[0][1] - X[0][0]
        height = X[1][1] - X[1][0]
        ax.add_patch(patches.Rectangle(
            (x0, y0),  # (x,y)
            width,  # width
            height,
            edgecolor='black',
            facecolor='red',
            fill=True
        )
        )
    while len(L_dark) > 0: # blue
        X = L_dark.popleft()
        x1 = X[0][0]
        y1 = X[1][0]
        width = X[0][1] - X[0][0]
        height = X[1][1] - X[1][0]
        ax.add_patch(patches.Rectangle(
            (x1, y1),  # (x,y)
            width,  # width
            height,
            edgecolor= 'black',
            facecolor = 'blue',
            fill=True)
        )
    while len(L_too_small) > 0: # yellow
        X = L_too_small.popleft()
        x2 = X[0][0]
        y2 = X[1][0]
        width = X[0][1] - X[0][0]
        height = X[1][1] - X[1][0]
        ax.add_patch(patches.Rectangle(
            (x2, y2),  # (x,y)
            width,  # width
            height,
            edgecolor='black',
            facecolor = 'yellow',
            fill=True
        )
        )
    ax.set_xlim([-2, 4])
    ax.set_ylim([-3, 5])
    plt.show()