from pyibex import Interval, IntervalVector, max, min, sqr, sign
from SIVIA import *
from vibes import vibes
from Disk import Disk

if __name__ == '__main__':
    # initiate the connection with the viewer
    vibes.beginDrawing()
    # create a new figure
    vibes.newFigure('TestCase0')
    vibes.setFigureProperties(dict(x=0, y=10, width=500, height=500))

    X0 = IntervalVector([[-2, 4], [-3, 5]])
    pdc = Disk(Interval(0, 1), Interval(0, 1), 2, 2)
    L_clear, L_dark, L_too_small =SIVIA(X0, pdc, 0.1)
    draw_SIVIA(L_clear, L_dark, L_too_small)
    vibes.drawBox(0, 1, 0, 1, '[k]')
    # vibes.setFigureProperties(dict(x=0, y=10, width=500, height=500))
    # L_clear, L_dark, L_too_small = SIVIA(X0, Disk(Interval(0, 1), Interval(0, 1), 2, 2, True), 0.1)
    # draw_SIVIA(L_clear, L_dark, L_too_small)
    # vibes.drawBox(0, 1, 0, 1, '[k]')
    vibes.saveImage("myImage.png", figure='TestCase0')
    vibes.endDrawing()



    # vibes.newFigure("myfig")
    # # Create a new group with specific format.
    # # Elements of this group are filled in cyan
    # vibes.newGroup("myGroup", format="r[cyan]")
    # vibes.drawCircle(0, 0, 3, group="myGroup")
    # vibes.drawBox(0, 4, -3, 3, group="myGroup")
    # vibes.drawPie((0, 0), (2, 4), [30, 60], group="myGroup")
