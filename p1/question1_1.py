import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib as mpl


map16 = [
    [0, -1, -1],
    [1, -1, 1],
    [2, -1, -3],
    [3, -1, 3],
    [4,  1, -1],
    [5,  1, 1],
    [6,  1, -3],
    [7,  1, 3],
    [8, -3, -1],
    [9, -3, 1],
    [10, -3, -3],
    [11, -3, 3],
    [12,  3, -1],
    [13,  3, 1],
    [14,  3, -3],
    [15,  3, 3],
]

map8 = [
    [0, -1, 1],
    [1,  1, 1],
    [2, -1, -1],
    [3,  1, -1],
    [4, -2.7, 0],
    [5,  0, 2.7],
    [6,  0, -2.7],
    [7,  2.7, 0],
]

map4 = [
    [0, -1, 1],
    [1,  1, 1],
    [2, -1, -1],
    [3,  1, -1],
]


def distance(b1, b2, a1, a2):
    # caculate the distance betwen the P1(a1,b1) and P2(a2,b2)
    return math.sqrt((b1-a1)**2 + (b2-a2)**2)


def coding(n, map):
    # coding process for channel information transmition
    # code value to I Q
    index = 0
    for i in range(len(n)):
        index += n[len(n)-i-1] * 2**i
    # index = index[0]
    return [map[index][1], map[index][2]]


def decoding(map, a1, a2, num):
    # decoding process for channel information transmition
    # I Q value to code such as 0,0,0,1
    dislist = []
    for i in range(len(map)):
        dislist.append(distance(map[i][1], map[i][2], a1, a2))

    out = dislist.index(min(dislist))
    outrecored = out
    outlist = []
    for i in range(num):
        outlist.append(out // (2 ** (num - i - 1)) % 2)
        if out // (2 ** (num - i - 1)) % 2 == 1:
            out = out - 2 ** (num - i - 1)

    return outlist


def getPn(map):
    # calculate the noise power Pn
    # assume that the code in map has the same occurrence probability

    A = 0
    for i in range(len(map)):
        A += map[i][1]**2 + map[i][2]**2

    return A / len(map)


def solute(num):
    # solute function 

    # choose the map matrix
    if num == 2:
        map = map4
    if num == 3:
        map = map8
    if num == 4:
        map = map16

    # set SNR
    SNR_DB = [x/10.0 for x in range(200)]
    SNR = [10 ** (x / 10) for x in SNR_DB]  # 信噪比，数字

    # get the Pn and Ps 
    size = len(SNR_DB)
    Ps = getPn(map)
    Pn = [Ps/x for x in SNR]

    # times of the experience 
    # N = 5000 # more time you use the line is more smooth 
    N = 50000
    BER = []
    for i in range(size):
        corrent = 0
        for j in range(N):
            # init the code n
            n = []
            for k in range(num):
                n.append(np.random.randint(0, high=2))

            # coding he n and get I Q
            b1, b2 = coding(n, map)

            # add noise and get output coding 
            o = decoding(map, np.random.normal(
                scale=math.sqrt(Pn[i])) + b1, np.random.normal(scale=math.sqrt(Pn[i]))+b2, num)

            # calculate the correct percent 
            for k in range(num):
                if o[k] == n[k]:
                    corrent += 1

        BER.append((N*num-corrent) / N/num)

    return SNR_DB, SNR, BER


def findnearest(BER2):
    # used in plot 
    minindex = 0
    mini = 100
    for i in range(len(BER2)):
        if abs(BER2[i]-0.02) < mini:
            mini = abs(BER2[i]-0.02)
            minindex = i
    return minindex


def main():
    # solute and plot 
    
    # that was a font file, may not useful in your computer
    # zhfont = mpl.font_manager.FontProperties(
    #     fname='/usr/share/fonts/Fonts/msyh.ttc')

    SNR_DB2, SNR2, BER2 = solute(2)
    print("finsh 2")
    SNR_DB3, SNR3, BER3 = solute(3)
    print("finsh 3")
    SNR_DB4, SNR4, BER4 = solute(4)
    print("finsh 4")

    # findnearest(BER2)

    plt.figure(1)
    plt.plot(SNR2[50:], BER2[50:], label="PQSK")
    plt.plot(SNR3[50:], BER3[50:], label="8QAM")
    plt.plot(SNR4[50:], BER4[50:], label="16QAM")
    plt.plot(SNR4[50:], [0.02] * len(SNR4[50:]), 'r')
    plt.plot(SNR2[findnearest(BER2)], 0.02, 'ko')
    plt.plot(SNR3[findnearest(BER3)], 0.02, 'ko')
    plt.plot(SNR4[findnearest(BER4)], 0.02, 'ko')
    plt.text(SNR2[findnearest(BER2)], 0.03, "[{}, {}]".format(
        '%.1f' % SNR2[findnearest(BER2)], str(0.02)))

    plt.text(SNR3[findnearest(BER3)], 0.03, "[{}, {}]".format(
        '%.1f' % SNR3[findnearest(BER3)], str(0.02)))

    plt.text(SNR4[findnearest(BER4)], 0.03, "[{}, {}]".format(
        '%.1f' % SNR4[findnearest(BER4)], str(0.02)))

    plt.xlabel("信噪比")
    plt.ylabel("误码率")
    plt.grid(True)

    plt.legend()
    plt.savefig("p1/BER-SNR-nodb.png", dpi=400)

    plt.figure(2)
    plt.plot(SNR_DB2[50:], BER2[50:], label="PQSK")
    plt.plot(SNR_DB3[50:], BER3[50:], label="8QAM")
    plt.plot(SNR_DB4[50:], BER4[50:], label="16QAM")
    plt.plot(SNR_DB4[50:], [0.02] * len(SNR_DB4[50:]), 'r')
    plt.plot(SNR_DB2[findnearest(BER2)], 0.02, 'ko')
    plt.plot(SNR_DB3[findnearest(BER3)], 0.02, 'ko')
    plt.plot(SNR_DB4[findnearest(BER4)], 0.02, 'ko')

    plt.text(SNR_DB2[findnearest(BER2)], 0.03, "[{},{}]".format(
        '%.1f' % SNR_DB2[findnearest(BER2)], str(0.02)))

    plt.text(SNR_DB3[findnearest(BER3)], 0.03, "[{},{}]".format(
        '%.1f' % SNR_DB3[findnearest(BER3)], str(0.02)))

    plt.text(SNR_DB4[findnearest(BER4)], 0.03, "[{},{}]".format(
        '%.1f' % SNR_DB4[findnearest(BER4)], str(0.02)))

    plt.xlabel("信噪比 / dB")
    plt.ylabel("误码率")
    plt.grid(True)

    plt.legend()
    plt.savefig("p1/BER-SNR-db.png", dpi=400)

    print(SNR_DB2)
    print(SNR_DB3)
    print(SNR_DB4)

    print(SNR2)
    print(SNR3)
    print(SNR4)

    print(BER2)
    print(BER3)
    print(BER4)


if __name__ == '__main__':
    main()
