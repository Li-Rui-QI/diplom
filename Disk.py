from pyibex import *
from SIVIA import *

# The thick set [[ Y ]] = [Y_subset, Y_supset]
# Y_subset -- disk with center (0, 0) and with radius r_subset = 1
# Y_supset -- disk with center (0, 0) and with radius r_supset = 2
# The thick function [f](x) = x - [v]
# [v] = [0.7, 1.3] x [-0.02, 0.02]
# Find approximation of [[ X ]] = [f]^(-1) ([[ Y ]]) using three types of intervals:
# 1. Classical intervals
# 2. The thick intervals with a subset-supset representation
# 3. The thick intervals defined by lower-upper interval bounds

class Disk:
    def __init__(self, mx, my, r_min=0, r_max=1, is_thin=False):
        self.m = IntervalVector([mx, my])
        self.Bp = Interval(0, r_max ** 2)
        self.Bm = Interval(0, r_min ** 2)
        self.is_thin = is_thin

    def test(self, X):
        m = self.m

        Xm = max(Interval(0), sign(
            (X[0] - m[0].ub()) * (X[0] - m[0].lb())
        )) * min(
            sqr(X[0] - m[0].lb()), sqr(X[0] - m[0].ub())
        ) + max(Interval(0), sign(
            (X[1] - m[1].ub()) * (X[1] - m[1].lb())
        ) * min(
            sqr(X[1] - m[1].lb()), sqr(X[1] - m[1].ub())
        ))

        Xp = max(
            sqr(X[0] - m[0].lb()), sqr(X[0] - m[0].ub())
        ) + max(
            sqr(X[1] - m[1].lb()), sqr(X[1] - m[1].ub())
        )

        Xub = Xm | Xp

        if self.Bp.is_disjoint(Xub):
            return IBOOL.OUT
        elif Xub.is_subset(self.Bm):
            return IBOOL.IN
        else:
            if self.is_thin:
                return IBOOL.UNK
            b1 = (Xm - self.Bp.ub()).is_subset(Interval(-1000, 0))
            b2 = (self.Bp.lb() - Xp).is_subset(Interval(-1000, 0))
            B1 = Xm - self.Bm.lb()
            B2 = self.Bm.ub() - Xp
            incl = (B1.ub() < 0 or B2.ub() < 0)
            if (b1 and b2) and incl:
                return IBOOL.MAYBE
            return IBOOL.UNK