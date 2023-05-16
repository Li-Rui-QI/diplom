from pyibex import *
from SIVIA import *
import numpy as np
from FindMatrixA import *

# Tolerable-United solution sets
#  /                 \    /  \     /       \
# | [2, 4]    [-2, 0] |  | x1 | = | [-1, 1] |
# | [-1, 1]    [2, 4] |  | x2 |   | [0, 2]  |
#  \                 /    \  /     \       /


class TolUnSolSets:
    def __init__(self, B,A):
        self.B = B
        self.A = A
#
    def test(self, I):
        Im = IntervalVector(len(self.A))
        Ip = IntervalVector(len(self.A))
        for i in range(0, len(self.A)):
            Im[i] = min(self.A[i][0] * I[0], self.A[i][1] * I[0]) + min(self.A[i][2] * I[1], self.A[i][3]*I[1])
            Ip[i] = max(self.A[i][0] * I[0], self.A[i][1] * I[0]) + max(self.A[i][2] * I[1], self.A[i][3]*I[1])

        # Im = IntervalVector([
        #     (min(self.A[0][0] * I[0], self.A[0][1] * I[0]) + min(self.A[0][2] * I[1], self.A[0][3]*I[1])),
        #     (min(self.A[3][0] * I[0], self.A[3][1] * I[0]) + min(self.A[3][2] * I[1], self.A[3][3]*I[1]))
        # ])
        #
        # Ip = IntervalVector([
        #     (max(self.A[0][0] * I[0], self.A[0][1] * I[0]) + max(self.A[0][2] * I[1], self.A[0][3] * I[1])),
        #     (max(self.A[3][0] * I[0], self.A[3][1] * I[0]) + max(self.A[3][2] * I[1], self.A[3][3] * I[1]))
        #
        #
        # ])

        Xub = Im | Ip

        if self.B.is_disjoint(Xub):
            return IBOOL.OUT
        elif self.B.is_superset(Xub):
            return IBOOL.IN
        else:
            b1 = (Im - self.B.ub()).is_subset(IntervalVector(2, Interval(-1000, 0)))
            b2 = (self.B.lb() - Ip).is_subset(IntervalVector(2, Interval(-1000, 0)))
            B1 = Im - self.B.lb()
            B2 = self.B.ub() - Ip
            incl = False
            for i in range(0, self.B.size()):
                if B1[i].ub() < 0 or B2[i].ub() < 0:
                    incl = True
                    break
            if (b1 and b2) and incl:
                return IBOOL.MAYBE
            return IBOOL.UNK


def testcase_2():

    eps = 0.1
    I_1, probes_1, currents_1 = generate(4, 4, True)
    A = find_matrix_A(I_1, probes_1, currents_1) * 1e7
    I0 = IntervalVector([[-10, 15], [-8, 10]])
    # b = IntervalVector([[-5.7, 5],  [-7, 7]])
    b = IntervalVector([[-5.7 ,5], [-4.7, 6],[-2,3],[-7,7]])
    L_clear, L_dark, L_too_small = SIVIA(I0, TolUnSolSets(b,A), eps)
    draw_SIVIA(I0,L_clear, L_dark,L_too_small)
    plt.show()



