import math
from  math import e
import itertools

def reflect(T):

    s = []              # 存放T中出现的字母
    k = 0
    for  i in range(0,len(T)):
        for n in range(0,len(s)):
            if s[n] == T[i]:
                break;
            k = k+1
        if k == len(s):
            s.append(T[i])
        k = 0
    print(s)

    r = []              # 存放字母对应的二进制映射及Value
    for i in range(0,len(s)):
        imag = 2 * math.pi * i / len(s)
        if imag == 0.0:
            r.append(math.exp(0))
        else:
            r.append(e ** (complex(0, imag)))
    print(r)

    test= list(itertools.permutations(r,len(r)))
    print((test))
    for i in range(0,len(list(test))):
        print(list(test)[i])

T = 'abcabb'
reflect(T)