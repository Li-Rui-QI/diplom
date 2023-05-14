from pyibex import *
from SIVIA import *

SQR = Function("x1", "x2", "( max ( 0, sign(x1 * x2) * min(x1^2, x2^2) ), max(x1^2, x2^2) )")
# SQRT = Function("x1", "x2", "(min(x1^(1/2),x2^(1/2)), max(x1^(1/2), x2^(1/2)))")
MINUS = Function("x1", "x2", "y1", "y2", "(x1 - y2, x2 - y1)")
PLUS = Function("x1", "x2", "y1", "y2", "(x1 + y1, x2 + y2)")


class Location:
    def __init__(self, m):
        self.l_m = m
        self.Bp = IntervalVector(len(m), [0, 30 ** 2])

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


def test_2():
    eps = 0.5

    X0 = IntervalVector(2, [-50, 50])

    m = [
        [Interval(1).inflate(0.5), Interval(3).inflate(0.5)],
        [Interval(5).inflate(0.5), Interval(-3).inflate(0.5)],
        [Interval(-5).inflate(0.5), Interval(-6).inflate(0.5)],
        [Interval(-2).inflate(0.5), Interval(-5).inflate(0.5)],
        # [Interval(8, 12), Interval(-3, 1)],
        # [Interval(8, 12), Interval(4, 8)]
    ]

    L_clear, L_dark,L_too_small = SIVIA(X0, Location(m), eps)
    draw_SIVIA(X0,L_clear, L_dark, L_too_small)

    for item in m:
        ax = plt.gca()
        x0 = item[0][0]
        y0 = item[1][0]
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
    plt.show()

