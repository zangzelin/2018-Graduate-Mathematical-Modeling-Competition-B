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
    sumg = sum(gl)
    cho = []
    for i in range(16):
        for j in range(gl[i]):
            cho.append([i])
    a = np.random.randint(low=0, high=sumg)
    zzl = cho[a][0]

    num = 4

    n = []
    for i in range(num):
        n.append(zzl // (2 ** (num - i - 1)) % 2)
        if zzl // (2 ** (num - i - 1)) % 2 == 1:
            zzl = zzl - 2 ** (num - i - 1)

    return n


def solute(gen):
    # print(gen)
    zhfont = mpl.font_manager.FontProperties(
        fname='/usr/share/fonts/Fonts/msyh.ttc')

    num = 4
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

    for i in range(4,8):
        # new_i = i
        new_x = -map[i%4][1]
        new_y = map[i%4][2]
        map.append([i, new_x, new_y])
    
    for i in range(8,12):
        # new_i = i
        new_x = map[i%4][1]
        new_y = -map[i%4][2]
        map.append([i, new_x, new_y])

    for i in range(12,16):
        # new_i = i
        new_x = -map[i%4][1]
        new_y = -map[i%4][2]
        map.append([i, new_x, new_y])
    
    # plt.figure()
    # for i in range(16):
    #     plt.plot(map[i][1],map[i][2],'o')
    # plt.show()
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

    xxs = 0
    for i in range(16):
        xxs+= (gailv[i]/sum(gailv)) * math.log2(0.001+(gailv[i]/sum(gailv)))

    # print(xxs)
    if -xxs < 3:
        return -100,
    SNR_DB = 13.3
    SNR = 10 ** (SNR_DB / 10)    # 信噪比，数字

    size = 1
    Ps = getPn(map, gailv)
    Pn = Ps / SNR

    N = 10000

    corrent = 0
    for j in range(N):
        n = createsignal(gailv) # 生成信号

        b1, b2 = coding(n, map)

        o = decoding(map, np.random.normal(
            scale=math.sqrt(Pn)) + b1, np.random.normal(scale=math.sqrt(Pn))+b2, num)

        for k in range(num):
            if o[k] == n[k]:
                corrent += 1

    BER = (N*num-corrent) / N / num

    if BER < 0.005:
        print(1)
    return -BER,


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

    for i in range(4,8):
        # new_i = i
        new_x = -map[i%4][1]
        new_y = map[i%4][2]
        map.append([i, new_x, new_y])
    
    for i in range(8,12):
        # new_i = i
        new_x = map[i%4][1]
        new_y = -map[i%4][2]
        map.append([i, new_x, new_y])

    for i in range(12,16):
        # new_i = i
        new_x = -map[i%4][1]
        new_y = -map[i%4][2]
        map.append([i, new_x, new_y])
    
    # plt.figure()
    # for i in range(16):
    #     plt.plot(map[i][1],map[i][2],'o')
    # plt.show()
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
        plt.plot(map[i][1],map[i][2],'o')
        plt.text(map[i][1],map[i][2],'{} \n p {}'.format(i, '%0.3f'%(gailv[i]/sum(gailv))))
    
    xxs = 0
    for i in range(16):
        xxs+= (gailv[i]/sum(gailv)) * math.log2(0.001+(gailv[i]/sum(gailv)))

    print(xxs)
    plt.show()

def main():
    # ax = plt.figure()

    # solute(2)
    # print("finsh 2")
    # solute(3)
    # print("finsh 3")
    # a = solute([1]*160)
    # print(a)
    # plt.grid(True)
    # plt.legend()
    # plt.savefig("BER-SNR-nodb.png", dpi=400)
    gen =  [1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
    print(solute(gen))
    plot1(gen)

if __name__ == '__main__':
    main()
