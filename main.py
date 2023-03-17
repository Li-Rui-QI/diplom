from pyibex import Interval, IntervalVector, max, min, sqr, sign
from SIVIA import *
from Disk import Disk

if __name__ == '__main__':
    # create a new figure
    X0 = IntervalVector([[-2, 4], [-3, 5]])
    pdc = Disk(Interval(0, 1), Interval(0, 1), 2, 2)
    L_clear, L_dark, L_too_small =SIVIA(X0, pdc, 0.1)
    draw_SIVIA(X0,L_clear, L_dark, L_too_small)
    plt.show()
