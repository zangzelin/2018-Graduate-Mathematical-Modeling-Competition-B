from gurobipy import *
import math
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt


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

def ploti(data,citys,citycitys,T):
    plt.figure()

    for i in citys:
        plt.plot(data[i][1],data[i][2],'ro',)

    count = 0
    for i,j in citycitys:
        if i>j and T[i][j] == 1:
            count += 1
            plt.plot([data[i][1],data[j][1]],[data[i][2],data[j][2]],'r-')

    plt.show()
    # print(count)

def getdata():
    data = [

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
    numberofcity = 12

    citys = range(numberofcity)

    D = []  # 距离
    C = []  # 容量
    H = []  # 人口
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

    for i in citys:
        for j in citys:
            for k in citys:
                if math.sqrt(H[j]) <= \
                        (math.sqrt(H[i])*math.sqrt(H[k]))/(math.sqrt(H[i])+math.sqrt(H[k])):
                    # print(i,j,k)
                    pass
    return D, C, H, citycitys


def CreateLineAndMax(T):

    A = []
    S = [[0] * 12 for i in range(12)]
    for i in range(16):
        s = []
        a = T[i*8:i*8+4]
        b = T[i*8+4:i*8+8]
        na = a[0]*8+a[1]*4+a[2]*2 + a[3]
        nb = b[0]*8+b[1]*4+b[2]*2 + b[3]

        na = int(na/16 * 12)
        nb = int(nb/16 * 12)
        if na == nb:
            bad = 1

        x = max(na,nb)
        y = min(nb,na)

        s.append(x)
        s.append(y)
        S[na][nb] = 1
        S[nb][na] = 1
        A.append(s)
    return A, S


def CheckTheBad(A):
    bad = 0
    for i in range(len(A)):
        for j in range(len(A)):
            if i != j and A[i][0] == A[j][0] and A[i][1] == A[j][1]:
                bad = 1
        if A[i][0] == A[i][1]:
            bad = 1

    set1 = set()
    for i in range(len(A)):
        set1.add(A[i][0])
        set1.add(A[i][1])

    if len(set1) < 12:
        bad = 1

    return bad


def getfit(T):

    data = [

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

    numberofcity = 12
    D,C,H,citycitys= getdata()
    lambda1 = [[1] * numberofcity for row in range(numberofcity)]

    A, S = CreateLineAndMax(T)
    # goodtras3, goodtras4 = findusefulline(S,H)
    bad = CheckTheBad(A)



    sum1 = 0
    if bad != 1:
        for i in range(16):
            x = A[i][0]
            y = A[i][1]
            a = max(x,y)
            b = min(x,y)
            x = a
            y = b
            sum1 += math.sqrt(H[x]*H[y]) * C[x][y] * lambda1[x][y]
    
    # ploti(data,range(12),citycitys,S)

    return int(sum1),


def evalOneMax(individual):
    a = sum(individual)
    return a,


def main():
    numberofcity = 12
    sumline = 16
    citys = range(numberofcity)
    lambda1 = [[1] * numberofcity for row in range(numberofcity)]
    D, C, H, citycitys = getdata()

    # s = getfit(T)
    # print(s)


if __name__ == '__main__':
    main()

