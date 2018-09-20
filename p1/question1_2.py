
import math

pi = 3.14
h = 6.62e-34
f = 1.93e14
B = 5e10
NF = 4

xzb = 3.3

def getout(K,F,n):

    d1 = (0.5) ** ((80/15) * n) * K * F

    u1 = sum([ F ** (x+1) for x in range(n)]) + \
         0.66 * K * (
             F ** n * 
             sum( [ 0.5 ** ( (80/15) * x) for x in range(n)]) + \
             F ** (n-1+0.001)
         )
    u2 = 2 * pi * h * f * B *\
        (
            NF + 1/(10 * math.log10(F))
        )
    # print(d1/u1/u2 )
    va = d1/u1/u2
    if va >= 3.3:
        # print(d1/u1/u2)
        return 1,va
    else: 
        return 0,va


def main():
    # K = 100
    maxn = 0

    for K in range(1000):
        for F in range(101,1000):
            for n in range(1,10):
                inF = F/100.0
                out,va = getout(K,inF,n)
                if out == 1 and maxn <= n:
                    maxn = n
                    # print(K,inF,n,va)
    print("find the max n is {}".format(maxn))

    # pass
if __name__ == '__main__':
    main()
