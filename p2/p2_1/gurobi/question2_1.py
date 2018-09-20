from gurobipy import *
import math
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt
import matplotlib as mpl

'''
Gurobi solver is used in this code, 
and you can install this software in 

http://www.gurobi.com/documentation/

'''


def ploti(data, citys, citycitys, T,sumline,datatype):
    # plot function
    
    # zhfont = mpl.font_manager.FontProperties(
    #     fname='/usr/share/fonts/Fonts/msyh.ttc')
    
    plt.figure()

    for i in citys:
        plt.plot(data[i][1], data[i][2], 'bo')
        # plt.text(data[i][1], data[i][2],data[i][0],fontproperties=zhfont)

    count = 0
    for i, j in citycitys:
        if i > j and T[i][j] == 1:
            count += 1
            plt.plot([data[i][1], data[j][1]], [data[i][2], data[j][2]], 'r-')
    plt.xlabel("经度 /°")
    plt.ylabel("纬度 /°")
    plt.savefig('p2/p2_1/gurobi/21_optimal_{}{}.png'.format(datatype,sumline), dpi=400)
    # plt.show()


def haversine(lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r * 1000


def solute(sumline,datatype):

    datasheng = [

        ["北京", 116.41667, 39.91667, 21.729],
        ["上海", 121.43333, 31.23, 24.197],
        ["哈尔滨", 126.63333, 45.75, 37.88],
        ["郑州", 113.65, 34.76667, 95.59],
        ["武汉", 114.31667, 30.51667, 59.2],
        ["广州", 113.23333, 23.16667, 111.69],
        ["西安", 108.95, 34.26667, 38.3],
        ["重庆", 106.45, 29.56667, 30.48],
        ["成都", 104.06667, 30.66667, 83.02],
        ["昆明", 102.4, 25.02, 47.36],
        ["拉萨", 91, 29.6, 3.1],
        ["乌鲁木齐", 87.68333, 43.76667, 24.112559]
    ]

    datashi = [

        ["北京", 116.41667, 39.91667, 21.729],
        ["上海", 121.43333, 31.23, 24.197],
        ["哈尔滨", 126.63333, 45.75, 10.929],
        ["郑州", 113.65, 34.76667, 9.8807],
        ["武汉", 114.31667, 30.51667, 10.8929],
        ["广州", 113.23333, 23.16667, 14.4984],
        ["西安", 108.95, 34.26667, 12.55],
        ["重庆", 106.45, 29.56667, 30.4843],
        ["成都", 104.06667, 30.66667, 16.0447],
        ["昆明", 102.4, 25.02, 6.728],
        ["拉萨", 91, 29.6, 1],
        ["乌鲁木齐", 87.68333, 43.76667, 3.112559]
    ]

    if datatype == "shi":
        data = datashi
    else:
        data = datasheng

    numberofcity = 12
    # sumline = 16
    citys = range(numberofcity)
    lambda1 = [[1] * numberofcity for row in range(numberofcity)]

    D = []
    C = []
    H = []
    for i in citys:
        Di = []
        Ci = []
        for j in citys:

            Di.append(
                int(haversine(data[i][1], data[i][2], data[j][1], data[j][2]))//1000)
            if Di[j] <= 600:
                Ci.append(32)
            elif Di[j] <= 1200:
                Ci.append(16)
            else:
                Ci.append(8)
        D.append(Di)
        C.append(Ci)
        H.append(int(data[i][3]))


    citycitys = []
    for i in range(numberofcity):
        for j in range(numberofcity):
            citycitys.append([i, j])

    # ----------------------------------------

    m = Model("diet")

    # var

    T = []
    for i in citys:
        Ti = []
        for j in citys:
            Ti.append(
                m.addVar(vtype=GRB.BINARY)
            )
        T.append(Ti)
    # con

    # 对角线为0
    for i in citys:
        m.addConstr(T[i][i] == 0)

    # 连接条数为16
    m.addConstr(quicksum([T[i][j] for i, j in citycitys]) == sumline * 2)

    # 每个点被连接
    for i in citys:
        m.addConstr(quicksum([T[i][j] for j in citys]) >= 1)

    # 连接是对称的
    for i, j in citycitys:
        m.addConstr(T[i][j] == T[j][i])

    # 去除掉非全互联的情况
    for i, j in citycitys:
        m.addConstr(
            quicksum([T[i][k] for k in citys]) +
            quicksum([T[j][k] for k in citys]) >=
            T[i][i] + T[i][j] + T[j][i] + T[j][j] + 1
        )

    for i, j in citycitys:
        for o in citys:
            m.addConstr(
                quicksum([T[i][k] for k in citys]) +
                quicksum([T[j][k] for k in citys]) +
                quicksum([T[o][k] for k in citys]) >= 1 +
                T[i][i] + T[i][j] + T[i][o] +
                T[j][i] + T[j][j] + T[j][o] +
                T[o][i] + T[o][j] + T[o][o]
            )

    sum1 = quicksum(
        [
            math.sqrt(H[i]*H[j]) * C[i][j] * T[i][j] * lambda1[i][j]
            for i, j in citycitys
        ]
    )/2


    m.setObjective(sum1, GRB.MAXIMIZE)
    m.optimize()

    print('Obj: %g' % m.objVal)

    out = []
    for i, j in citycitys:
        print(int(T[i][j].x), end=' ')
        T[i][j] = T[i][j].x
        if j == numberofcity-1:
            print(" ")
        if int(T[i][j]) == 1 and i > j:
            out.append([i, j])

    print(out)
    ploti(data, citys, citycitys, T,sumline,datatype)

    for i in range(len(out)):
        print(data[out[i][0]][0], data[out[i][1]][0])

def main():
    solute(16,'shi')
    solute(16,'sheng')
    solute(33,'shi')
    solute(33,'sheng')

if __name__ == '__main__':
    main()