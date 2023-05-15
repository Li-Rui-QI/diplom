import numpy as np
from pyibex import Interval, IntervalVector, max, min
from SIVIA import *
from Disk import Disk
from Text import *
from Location import *
from Communication_area import test_1
from FindMatrixA import *
from InverseTor import *

if __name__ == '__main__':
    # create a new figure
    # X0 = IntervalVector(2, [-2, 2])
    # pdc = Disk(Interval(0, 0), Interval(0, 0), 1, 2,True)
    # L_clear, L_dark, L_too_small =SIVIA(X0, pdc, 0.1)
    # draw_SIVIA(X0,L_clear, L_dark, L_too_small)
    # plt.title('с помощью классических интервалов SIVIA')
    # plt.show()
    # test_1()
    # line_chart()
    # test_2()
    # I_1, probes_1, currents_1=generate(4, 4, True)
    # A = find_matrix_A(I_1, probes_1, currents_1)*1e7
    # Im = IntervalVector(len(A))
    # print(Im)
    # print(A)
    # case1()
    testcase_2()