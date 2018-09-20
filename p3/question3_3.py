import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib as mpl


def distance(b1, b2, a1, a2):
    return math.sqrt((b1-a1)**2 + (b2-a2)**2)


def decoding(map, a1, a2, num):

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


def coding(n, map):
    index = 0
    for i in range(len(n)):
        index += n[len(n)-i-1] * 2**i
    # index = index[0]
    return [map[index][1], map[index][2]]


def getPn(map, gailv):
    A = 0
    for i in range(len(map)):
        A += (map[i][1]**2 + map[i][2]**2)*gailv[i]

    return A / sum(gailv)


def createsignal(gl):

    num = int(math.log2(len(gl)))
    sumg = sum(gl)
    cho = []
    for i in range(len(gl)):
        for j in range(gl[i]):
            cho.append([i])
    a = np.random.randint(low=0, high=sumg)
    zzl = cho[a][0]

    n = []
    for i in range(num):
        n.append(zzl // (2 ** (num - i - 1)) % 2)
        if zzl // (2 ** (num - i - 1)) % 2 == 1:
            zzl = zzl - 2 ** (num - i - 1)

    return n


def solute(map, gailv):
    # print(gen)
    zhfont = mpl.font_manager.FontProperties(
        fname='/usr/share/fonts/Fonts/msyh.ttc')

    num = int(math.log2(len(map)))

    # SNR_DB = 13.3
    SNR_DB = [x/10.0 for x in range(200)]
    SNR = [10 ** (x / 10) for x in SNR_DB]  # 信噪比，数字

    # SNR = 10 ** (SNR_DB / 10)    # 信噪比，数字

    size = len(SNR_DB)
    Ps = getPn(map, gailv)
    Pn = [Ps/x for x in SNR]

    N = 50000
    BER = []
    for i in range(size):

        if i % (size//10) == 0:
            print('*', end='')

        corrent = 0
        for j in range(N):
            n = createsignal(gailv)  # 生成信号

            b1, b2 = coding(n, map)

            o = decoding(map, np.random.normal(
                scale=math.sqrt(Pn[i])) + b1, np.random.normal(scale=math.sqrt(Pn[i]))+b2, num)

            for k in range(num):
                if o[k] == n[k]:
                    corrent += 1

        BER.append((N*num-corrent) / N/num)

    return SNR_DB, SNR, BER


def evalOneMax(individual):

    return sum(individual),


def plot1(gen):
    place = gen[:40]
    map = []
    for i in range(4):
        genx = place[i*10:i*10+5]
        geny = place[i*10+5:i*10+10]

        x = 16 * genx[0] + 8*genx[1] + 4*genx[2]+2*genx[3]+genx[4]
        y = 16 * geny[0] + 8*geny[1] + 4*geny[2]+2*geny[3]+geny[4]
        x = x/31
        y = y/31

        map.append([i, x, y])

    for i in range(4, 8):
        # new_i = i
        new_x = -map[i % 4][1]
        new_y = map[i % 4][2]
        map.append([i, new_x, new_y])

    for i in range(8, 12):
        # new_i = i
        new_x = map[i % 4][1]
        new_y = -map[i % 4][2]
        map.append([i, new_x, new_y])

    for i in range(12, 16):
        # new_i = i
        new_x = -map[i % 4][1]
        new_y = -map[i % 4][2]
        map.append([i, new_x, new_y])

    gal = gen[40:]

    gl1 = gal[0:5]
    gl2 = gal[5:10]
    gl3 = gal[10:15]
    gl4 = gal[15:20]

    x1 = 16 * gl1[0] + 8*gl1[1] + 4*gl1[2]+2*gl1[3]+gl1[4]
    x2 = 16 * gl2[0] + 8*gl2[1] + 4*gl2[2]+2*gl2[3]+gl2[4]
    x3 = 16 * gl3[0] + 8*gl3[1] + 4*gl3[2]+2*gl3[3]+gl3[4]
    x4 = 16 * gl4[0] + 8*gl4[1] + 4*gl4[2]+2*gl4[3]+gl4[4]

    gailv = []
    for i in range(4):
        gailv.append(x1)
        gailv.append(x2)
        gailv.append(x3)
        gailv.append(x4)

    plt.figure()
    for i in range(16):
        plt.plot(map[i][1], map[i][2], 'o')
        plt.text(map[i][1], map[i][2], '{} \n p {}'.format(
            i, '%0.2f' % (gailv[i]/sum(gailv))))

    xxs = 0
    for i in range(16):
        xxs += (gailv[i]/sum(gailv)) * math.log2(0.001+(gailv[i]/sum(gailv)))

    print(xxs)
    plt.show()


def findnearest(BER2):
    minindex = 0
    mini = 100
    for i in range(len(BER2)):
        if abs(BER2[i]-0.02) < mini:
            mini = abs(BER2[i]-0.02)
            minindex = i
    return minindex


def main():
    zhfont = mpl.font_manager.FontProperties(
        fname='/usr/share/fonts/Fonts/msyh.ttc')
    # ax = plt.figure()
    pointnew = [[0, 0.2903225806451613, 0.9032258064516129], [1, 0.7419354838709677, 0.6129032258064516], [2, 0.9032258064516129, 0.22580645161290322], [3, 0.22580645161290322, 0.22580645161290322], [4, -0.2903225806451613, 0.9032258064516129], [5, -0.7419354838709677, 0.6129032258064516], [6, -0.9032258064516129, 0.22580645161290322], [7, -0.22580645161290322, 0.22580645161290322],
                [8, 0.2903225806451613, -0.9032258064516129], [9, 0.7419354838709677, -0.6129032258064516], [10, 0.9032258064516129, -0.22580645161290322], [11, 0.22580645161290322, -0.22580645161290322], [12, -0.2903225806451613, -0.9032258064516129], [13, -0.7419354838709677, -0.6129032258064516], [14, -0.9032258064516129, -0.22580645161290322], [15, -0.22580645161290322, -0.22580645161290322]]
    gailvnew = [3, 3, 2, 31, 3, 3, 2, 31, 3, 3, 2, 31, 3, 3, 2, 31]
    pointnew1 = [[0, 0.6774193548387096, 0.22580645161290322], [1, 0.22580645161290322, 0.25806451612903225], [2, 0.7096774193548387, 0.9032258064516129], [3, 0.1935483870967742, 0.8709677419354839], [4, -0.6774193548387096, 0.22580645161290322], [5, -0.22580645161290322, 0.25806451612903225], [6, -0.7096774193548387, 0.9032258064516129], [7, -0.1935483870967742, 0.8709677419354839], [8, 0.6774193548387096, -0.22580645161290322], [9, 0.22580645161290322, -0.25806451612903225], [10, 0.7096774193548387, -0.9032258064516129], [11, 0.1935483870967742, -0.8709677419354839], [12, -0.6774193548387096, -0.22580645161290322], [13, -0.22580645161290322, -0.25806451612903225], [14, -0.7096774193548387, -0.9032258064516129], [15, -0.1935483870967742, -0.8709677419354839]]
    gailvnew1 = [8, 27, 0, 2, 8, 27, 0, 2, 8, 27, 0, 2, 8, 27, 0, 2]

    point4 = [
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
    gailv4 = [1] * 16

    point3 = [
        [0, -1, 1],
        [1,  1, 1],
        [2, -1, -1],
        [3,  1, -1],
        [4, -2.7, 0],
        [5,  0, 2.7],
        [6,  0, -2.7],
        [7,  2.7, 0],
    ]
    gailv3 = [1] * 8

    point2 = [
        [0, -1, 1],
        [1,  1, 1],
        [2, -1, -1],
        [3,  1, -1],
    ]
    gailv2 = [1] * 4

    SNR_DB4, SNR4, BER4 = solute(point4, gailv4)
    print('*')
    SNR_DB3, SNR3, BER3 = solute(point3, gailv3)
    print('*')
    SNR_DB2, SNR2, BER2 = solute(point2, gailv2)
    print('*')
    SNR_DBn, SNRn, BERn = solute(pointnew1, gailvnew1)
    print('*')

    plt.figure(1)
    plt.plot(SNR2[50:], BER2[50:], label="PQSK")
    plt.plot(SNR3[50:], BER3[50:], label="8QAM")
    plt.plot(SNR4[50:], BER4[50:], label="16QAM")
    plt.plot(SNRn[50:], BERn[50:], label="new-16QAM")
    plt.plot(SNR4[50:], [0.02] * len(SNR4[50:]), 'r')
    plt.plot(SNR2[findnearest(BER2)], 0.02, 'ko')
    plt.plot(SNR3[findnearest(BER3)], 0.02, 'ko')
    plt.plot(SNR4[findnearest(BER4)], 0.02, 'ko')
    plt.plot(SNRn[findnearest(BERn)], 0.02, 'ko')
    plt.text(SNR2[findnearest(BER2)], 0.03, "[{}, {}]".format(
        '%.1f' % SNR2[findnearest(BER2)], str(0.02)), fontproperties=zhfont)

    plt.text(SNR3[findnearest(BER3)], 0.04, "[{}, {}]".format(
        '%.1f' % SNR3[findnearest(BER3)], str(0.02)), fontproperties=zhfont)

    plt.text(SNR4[findnearest(BER4)], 0.03, "[{}, {}]".format('%.1f' % SNR4[findnearest(BER4)], str(0.02)), fontproperties=zhfont)
    plt.text(SNRn[findnearest(BERn)], 0.01, "[{}, {}]".format('%.1f' % SNRn[findnearest(BERn)], str(0.02)), fontproperties=zhfont)

    plt.xlabel("信噪比", fontproperties=zhfont)
    plt.ylabel("误码率", fontproperties=zhfont)
    plt.grid(True)
    plt.legend()
    plt.savefig("p3/3_4_nodb.png", dpi=400)

    plt.figure(2)
    plt.plot(SNR_DB2[50:], BER2[50:], label="PQSK")
    plt.plot(SNR_DB3[50:], BER3[50:], label="8QAM")
    plt.plot(SNR_DB4[50:], BER4[50:], label="16QAM")
    plt.plot(SNR_DBn[50:], BERn[50:], label="new-16QAM")
    plt.plot(SNR_DB4[50:], [0.02] * len(SNR4[50:]), 'r')
    plt.plot(SNR_DB2[findnearest(BER2)], 0.02, 'ko')
    plt.plot(SNR_DB3[findnearest(BER3)], 0.02, 'ko')
    plt.plot(SNR_DB4[findnearest(BER4)], 0.02, 'ko')
    plt.plot(SNR_DBn[findnearest(BERn)], 0.02, 'ko')
    plt.text(SNR_DB2[findnearest(BER2)], 0.03, "[{}, {}]".format(
        '%.1f' % SNR_DB2[findnearest(BER2)], str(0.02)), fontproperties=zhfont)

    plt.text(SNR_DB3[findnearest(BER3)], 0.04, "[{}, {}]".format(
        '%.1f' % SNR_DB3[findnearest(BER3)], str(0.02)), fontproperties=zhfont)

    plt.text(SNR_DB4[findnearest(BER4)], 0.03, "[{}, {}]".format('%.1f' % SNR_DB4[findnearest(BER4)], str(0.02)), fontproperties=zhfont)
    plt.text(SNR_DBn[findnearest(BERn)], 0.03, "[{}, {}]".format('%.1f' % SNR_DB4[findnearest(BERn)], str(0.02)), fontproperties=zhfont)

    plt.xlabel("信噪比 /dB", fontproperties=zhfont)
    plt.ylabel("误码率", fontproperties=zhfont)
    plt.grid(True)
    plt.legend()
    plt.savefig("p3/3_4_db.png", dpi=400)



if __name__ == '__main__':
    main()
