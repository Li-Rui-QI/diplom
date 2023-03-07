from enum import Enum
from pyibex import IntervalVector, LargestFirst
from collections import deque


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