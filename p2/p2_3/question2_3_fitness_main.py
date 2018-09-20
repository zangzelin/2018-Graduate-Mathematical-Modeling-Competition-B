import copy
import math
from math import asin, cos, radians, sin, sqrt

import matplotlib as mpl
import matplotlib.pyplot as plt
from gurobipy import *

import question2_3_deap
import numpy as np

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


def GetData(str):

    data_shi = [

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
    data_sheng = [
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
    if str == "shi":
        data = data_shi
    else:
        data = data_sheng

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

    return D, C, H, citycitys, data


def CreateLineAndMax(T):

    A = []
    S = [[0] * numberofcity for i in range(numberofcity)]
    len1 = len(T)// 8
    
    if len1 == 16:
        for i in range(len1):
            s = []
            a = T[i*8:i*8+4]
            b = T[i*8+4:i*8+8]
            na = a[0]*8+a[1]*4+a[2]*2 + a[3]
            nb = b[0]*8+b[1]*4+b[2]*2 + b[3]

            na = int(na/16 * 12)
            nb = int(nb/16 * 12)
            if na == nb:
                bad = 1

            x = max(na, nb)
            y = min(nb, na)

            s.append(x)
            s.append(y)
            S[na][nb] = 1
            S[nb][na] = 1
            A.append(s)

    else:
        for i in range(len1):
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
            
            if x == y :
                if y < 11:
                    y = y+1
                else:
                    y = y-1

    
            in1 = 0
            if [x,y] in A:
                if y == 11:
                    y = 0
                while 1:
                    y += 1
                    if [x,y] not in A and x != y:
                        
                        A.append([x,y])
                        break
                    if y > 10:
                        A.append([x,y])
                        break
            else:
                A.append([x,y])
            
            S[A[i][0]][A[i][1]] = 1
            S[A[i][1]][A[i][0]] = 1
    return A, S


def CreateLineAndMax2(T):

    A = [[1, 0], [2, 0], [3, 1], [4, 0], [4, 1], [4, 3], [6, 0], [6, 3],
         [7, 3], [7, 4], [7, 5], [7, 6], [8, 7], [9, 7], [10, 7], [11, 7]]
    S = [[0] * 12 for i in range(12)]
    for i in range(16):

        na = A[i][0]
        nb = A[i][1]
        if na == nb:
            bad = 1

        x = max(na, nb)
        y = min(nb, na)
        s = []
        s.append(x)
        s.append(y)
        S[na][nb] = 1
        S[nb][na] = 1
        # A.append(s)
    return A, S


def findusefulline(S, H):
    citys = range(numberofcity)
    goodtras3 = []
    for i in citys:
        for j in citys:
            for k in citys:
                ve = math.sqrt(H[i]*H[k])-math.sqrt(H[i] *
                                                    H[j])-math.sqrt(H[j] * H[k])
                # if ve > 0:
                # print(">0")
                if ve > 0 and i != k and S[i][j] == 1 and S[j][k] == 1 and i > k:
                    goodtras3.append([i, j, k, ve])

    goodtras4 = []
    for i in citys:
        for j in citys:
            for k in citys:
                for l in citys:
                    ve = math.sqrt(H[i]*H[l])-math.sqrt(H[i]*H[j]) - \
                        math.sqrt(H[j] * H[k])-math.sqrt(H[l] * H[k])
                    if ve > 0 and i != l and S[i][j] == 1 and S[j][k] == 1 and S[k][l] == 1 and i > l and j != k:
                        goodtras4.append([i, j, k, l, ve])

    return goodtras3, goodtras4


def AddTheScore(goodtras3, goodtras4, C):

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

    goodtras3.sort(key=lambda ele: ele[3], reverse=True)

    derta = 0
    s = ''

    for item in goodtras3:
        point1 = item[0]
        point2 = item[1]
        point3 = item[2]

        maxliuliang = min(C[point1][point2], C[point2][point3])
        if maxliuliang > 0:
            C[point1][point2] -= maxliuliang
            C[point2][point1] -= maxliuliang
            C[point2][point3] -= maxliuliang
            C[point3][point2] -= maxliuliang

            derta += item[3] * maxliuliang
            s += str(data[point1][0])+'->'+str(data[point2][0])+'->' + \
                str(data[point3][0]) + ':' + str(maxliuliang) + '\n'

    goodtras4.sort(key=lambda ele: ele[4], reverse=True)
    for item in goodtras4:
        point1 = item[0]
        point2 = item[1]
        point3 = item[2]
        point4 = item[3]

        maxliuliang = min(C[point1][point2], C[point2]
                          [point3], C[point3][point4])
        if maxliuliang > 0:

            C[point1][point2] -= maxliuliang
            C[point2][point1] -= maxliuliang
            C[point2][point3] -= maxliuliang
            C[point3][point2] -= maxliuliang
            C[point3][point4] -= maxliuliang
            C[point4][point3] -= maxliuliang

            derta += item[4] * maxliuliang
            s += str(data[point1][0])+'->'+str(data[point2][0])+'->'+str(data[point3]
                                                                         [0])+'->'+str(data[point4][0]) + ':' + str(maxliuliang) + '\n'

    return derta, s


def ploti(data, citys, filename, T):
    zhfont = mpl.font_manager.FontProperties(
        fname='/usr/share/fonts/Fonts/msyh.ttc')
    plt.figure()

    for i in citys:
        plt.plot(data[i][1], data[i][2], 'bo')
        # plt.text(data[i][1], data[i][2],data[i][0],fontproperties=zhfont)

    count = 0
    for i, j in citycitys:
        if i > j and T[i][j] == 1:
            count += 1
            plt.plot([data[i][1], data[j][1]], [data[i][2], data[j][2]], 'r-')

    plt.xlabel("经度 /°", fontproperties=zhfont)
    plt.ylabel("纬度 /°", fontproperties=zhfont)
    plt.savefig(filename+'.png', dpi=400)



def CheckTheBad(A):
    bad = 0
    for i in range(len(A)):
        for j in range(len(A)):
            if i != j and A[i][0] == A[j][0] and A[i][1] == A[j][1]:
                bad = 1
            if i != j and A[i][0] == A[j][1] and A[i][1] == A[j][0]:
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
    

    sum1 = 1
    A, S = CreateLineAndMax(T)
    goodtras3, goodtras4 = findusefulline(S, H)
    bad = CheckTheBad(A)

    lmbdaaaa1 = -110
    lmbdaaaa2 = -110
    lmbdaaaa3 = -110

    if bad != 1:
        sum1, s = AddTheScore(goodtras3, goodtras4, copy.deepcopy(C))
        for i in range(len(A)):
            x = A[i][0]
            y = A[i][1]
            a = max(x, y)
            b = min(x, y)
            x = a
            y = b
            sum1 += math.sqrt(H[x]*H[y]) * C[x][y] * lambda1[x][y]
        sum2 = sum([fenshujuzhen[i][j] * S[i][j] for i, j in citycitys])

        sum3 = np.var([sum([S[i][j] * C[i][j] for j in range(12)])
                    for i in range(12)])

        lmbdaaaa1 = (6000 + (200) - (6000- sum1))/200
        lmbdaaaa2 = (25 + 5 - (25-sum2))/200
        lmbdaaaa3 = (Max3 + 10 - sum3)/2
    
    
    return lmbdaaaa1+lmbdaaaa2/5+lmbdaaaa3/10,


def getfitwithplot(T, sumline, datastr,data):

    numberofcity = 12
    D, C, H, citycitys, data = GetData(datastr)
    lambda1 = [[1] * numberofcity for row in range(numberofcity)]

    A, S = CreateLineAndMax(T)
    goodtras3, goodtras4 = findusefulline(S, H)
    bad = CheckTheBad(A)

    if bad != 1:
        sum1,ssss = AddTheScore(goodtras3, goodtras4,copy.deepcopy(C) )
        for i in range(len(A)):
            x = A[i][0]
            y = A[i][1]
            a = max(x, y)
            b = min(x, y)
            x = a
            y = b
            sum1 += math.sqrt(H[x]*H[y]) * C[x][y] * lambda1[x][y]
        sum2 = sum([fenshujuzhen[i][j] * S[i][j] for i, j in citycitys])

        sum3 = np.var([sum([S[i][j] * C[i][j] for j in range(12)])
                    for i in range(12)])

        lmbdaaaa1 = (6000 + (200) - (6000- sum1))/200
        lmbdaaaa2 = (25 + 5 - (25-sum2))/200
        lmbdaaaa3 = (Max3 + 10 - sum3)/2

    filename = "p2/p2_3/23{}{}".format(datastr, sumline)
    f = open(filename+'.txt', 'w')
    f.write(ssss)
    f.close()

    for i in range(len(A)):
        print(data[A[i][0]][0], data[A[i][1]][0])

    ploti(data, range(12), filename, S)


numberofcity = 12
D, C, H, citycitys, data = GetData('shi')
lambda1 = [[1] * numberofcity for row in range(numberofcity)]
citys = range(numberofcity)
data = []

fenshu = [0.8849617254, 0.6026134106, 0.3589594829, 0.5663596092, 0.6551522425, 0.5564314226, 0.5155288626, 0.4757958043, 0.386196772, 0.298100972, 0.2701649654, 0.3031553566, 0.6026134106, 0.8923802528, 0.4800341665, 0.4465773333, 0.5618528396, 0.5906437506, 0.5039990068, 0.4804133599, 0.2700814308, 0.1968721703, 0.2531597227, 0.2768405271, 0.3589594829, 0.4800341665, 0.6995458799, 0.3565609107, 0.3183358376, 0.2480699871, 0.161366876, 0.130978076, 0.1886472066, 0.0896378082, 0.0324425116, 0.0708687044, 0.5663596092, 0.4465773333, 0.3565609107, 0.7963173832, 0.7835770857, 0.5455330548, 0.547622767, 0.4140915862, 0.3945937903, 0.3557063912, 0.1881893357, 0.2066036522, 0.6551522425, 0.5618528396, 0.3183358376, 0.7835770857, 0.8229182537, 0.9584204155, 0.5225305297, 0.3986283918, 0.407460232, 0.3570954304, 0.1589133288, 0.1550260977, 0.5564314226, 0.5906437506, 0.2480699871, 0.5455330548, 0.9584204155, 1, 0.7020337056, 0.6021487813, 0.4329384032, 0.4387576292, 0.4105804559, 0.3840849895,
            0.5155288626, 0.5039990068, 0.161366876, 0.547622767, 0.5225305297, 0.7020337056, 0.7503623282, 0.7214574897, 0.5355672553, 0.3191528791, 0.1409348266, 0.1466028041, 0.4757958043, 0.4804133599, 0.130978076, 0.4140915862, 0.3986283918, 0.6021487813, 0.7214574897, 0.7534366261, 0.7816884195, 0.4586948247, 0.2827194348, 0.1388279966, 0.386196772, 0.2700814308, 0.1886472066, 0.3945937903, 0.407460232, 0.4329384032, 0.5355672553, 0.7816884195, 0.7907003597, 0.7436446606, 0.327421392, 0.2026857618, 0.298100972, 0.1968721703, 0.0896378082, 0.3557063912, 0.3570954304, 0.4387576292, 0.3191528791, 0.4586948247, 0.7436446606, 0.7132095383, 0.2378011113, 0.100842946, 0.2701649654, 0.2531597227, 0.0324425116, 0.1881893357, 0.1589133288, 0.4105804559, 0.1409348266, 0.2827194348, 0.327421392, 0.2378011113, 0.6434361959, 0.1036221866, 0.3031553566, 0.2768405271, 0.0708687044, 0.2066036522, 0.1550260977, 0.3840849895, 0.1466028041, 0.1388279966, 0.2026857618, 0.100842946, 0.1036221866, 0.6781107247, ]
numberofcity = 12
Max1 = 5500
Max2 = 20
Max3 = 8
fenshujuzhen = []
for i in range(12):
    fenshujuzhen.append(fenshu[i*12:i*12+12])

def solute(sumline, datastr):
    D, C, H, citycitys, data = GetData(datastr)
    loop = 100
    best_ind = question2_3_deap.main(sumline, loop)
    getfitwithplot(best_ind, sumline, datastr,data)
    return best_ind


def main():

    solute(16,"shi")
    solute(16,"sheng")
    solute(33,"shi")
    solute(33,"sheng")


if __name__ == '__main__':
    main()
