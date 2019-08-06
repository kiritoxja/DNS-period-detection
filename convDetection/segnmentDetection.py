import math
from math import e
import itertools

def segmentDetection(T,conf):
    result = {}
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
        imag = float(2 * math.pi * i / len(s))
        if imag == 0.0:
            r.append(math.exp(0))
        else:
            r.append(e ** (complex(0, imag)))

    print(r)

    # W = list(itertools.permutations(r,len(r)))                  # 存放映射对应的w值
    W =r

    C = [[]for i in range(0,len(W))]                  # 存放结果
    for i in range(0,len(C)):
        C[i]  = [0 for j in range(1, int(len(T)/2)+2)]


    # 计算卷积
    for l in range(0,len(W)):
        '''
        
        # 重新建立s与w之间的映射关系
        if l == 0:
            W = r
        else:
            temp = W[0]
            for j in range(1,len(W)):
                W[j-1] = W[j]
            W[len(W)-1] = temp
        '''

        # 生成C（Tl）
        Tl = []     # 根据映射生成新的序列
        for i in range(0,len(T)):
            # 生成新序列Tl
            for j in range(0,len(s)):
                if T[i] == s[j]:
                    Tl.append(W[j])
        print(Tl)

        for p in range(1, int(len(T)/2)+1):
            for i in range(0,len(T)):
                if(i+p)> len(T)-1:
                    break
                else:
                    if Tl[i]==Tl[i+p]:
                        C[l][p] = C[l][p] + 1.0
                    else :
                        C[l][p] = C[l][p] + 0
                        # Tl[i]
    print(C)

    # 计算平均值并根据阈值筛选候选周期
    CT = [0  for i in range(1,int(len(T)/2)+2)]
    for i in range(1,len(CT)):
        for l in range(0,len(C)):
            CT[i] = CT[i] + C[l][i]
        CT[i] = CT[i]/len(W)

    print(CT)

    for p in range(1,len(CT)):
        if int(CT[p].real)/(len(T)-p)>=conf:
            result[p] = int(CT[p].real)/(len(T)-p)

    print(result)
    return  result





path = "E:\dns_detection\intervalToStr.txt"
for line in open(path,"r"):
    dns = line.split(" ")
    periodResult = segmentDetection(dns[2], 0.6)
    if periodResult == {}:
        continue
    result = dns[0] + " "+dns[1] + " "+dns[2]+" "
    for i in periodResult.keys():
        result = result + str(i) + ":"+ str(periodResult[i])+" "
    result = result+"\n"
    print(result)
    f = open("E:\dns_detection\conv_segmentDetection.txt","a")
    f.write(result)

    '''
        # 开始进行位移,计算ci(Tl)
        for p in range(1,int(len(T)/2)):


T = 'abcabbabcb'
segmentDetection(T,0.333333)

'''




