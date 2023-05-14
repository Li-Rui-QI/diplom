import matplotlib.pyplot as plt

def line_chart():
#折线图
    x = [1,2,3,4,5,6]#点的横坐标
    k1 = [260.7,170.7,87.5,58.7,58.5,46.4]#线1的纵坐标
    k2 = [260.7,87.5,22.9,14.1,14.1,0]#线2的纵坐标
    plt.plot(x,k1,'s-',color = 'r',label="distance 5m")#s-:方形
    plt.plot(x,k2,'o-',color = 'g',label="distance 10m")#o-:圆形
    plt.xlabel("Number of tags")#横坐标名字
    plt.ylabel("area")#纵坐标名字
    plt.legend(loc = "best")#图例
    plt.show()
