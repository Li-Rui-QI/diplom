from matplotlib.patches import Circle
from pyibex import *
from SIVIA import *


class CommArea:
    def __init__(self, m,is_thin=False):
        self.l_m = m
        self.Bp = IntervalVector(len(m), [0, 20 ** 2])
        self.Bm = IntervalVector(len(m), [0, 10 ** 2])
        self.is_thin = is_thin

    def test(self, X):
        Xm = IntervalVector(len(self.l_m))
        Xp = IntervalVector(len(self.l_m))

        for i, m in enumerate(self.l_m):
            Xm[i] = max(
                Interval(0),
                sign((X[0] - m[0].ub()) * (X[0] - m[0].lb()))
            ) * min(
                sqr(X[0] - m[0].lb()), sqr(X[0] - m[0].ub())
            ) + max(
                Interval(0),
                sign((X[1] - m[1].ub()) * (X[1] - m[1].lb()))
            ) * min(
                sqr(X[1] - m[1].lb()), sqr(X[1] - m[1].ub())
            )

            Xp[i] = max(
                sqr(X[0] - m[0].lb()), sqr(X[0] - m[0].ub())
            ) + max(
                sqr(X[1] - m[1].lb()), sqr(X[1] - m[1].ub())
            )

        Xub = Xm | Xp

        if self.Bp.is_disjoint(Xub):
            return IBOOL.OUT
        elif Xub.is_subset(self.Bm):
            return IBOOL.IN
        elif self.is_thin:
            return IBOOL.UNK


def add_patch(cir1):
    pass


def test_1():

    eps = 0.5
    X0 = IntervalVector(2, [-20, 20])

    m = [
        [Interval(1).inflate(0.5), Interval(3).inflate(0.5)],
        [Interval(5).inflate(0.5), Interval(-3).inflate(0.5)],
        [Interval(5).inflate(0.5), Interval(6).inflate(0.5)],
        [Interval(-2).inflate(0.5), Interval(-5).inflate(0.5)]
    ]

    L_clear, L_dark, L_too_small = SIVIA(X0, CommArea(m,True), eps)
    draw_SIVIA(X0,L_clear, L_dark,L_too_small)
    plt.title('CommArea с помощью классических интервалов SIVIA')

    for item in m:

        cir1 = Circle(xy=(item[0].mid(), item[1].mid()), radius=0.2, alpha=0.5)
        add_patch(cir1)

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
