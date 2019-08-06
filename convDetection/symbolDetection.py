import numpy as np
import itertools
'''

def product(S):
    temp = ""
    result = []
    for i in range(1,len(S)):
        for j in range(0,i-1):
            if S[i][j] == "*":
                temp[j] = "*"
                continue
            else:
                for k in range(0,len(S[i][j])):
'''



def FFT(X,Y,W):
    result = 0
    for i in range(0,len(X)):
        result = result + 2**(len(X)-i-1) *int(X[i])*int(Y[i])
        if int(X[i])*int(Y[i])!=0:
            W.append(len(X) - i - 1)
    return  result

def symbolDetection(T,conf):   #T为待检测字符串，conf为阈值
    single_result = {}         #存放单个字母结果的字典
    result = {}                #最后结果存放的字典

    s = []              #存放T中出现的字母
    r = []              #存放字母对应的二进制映射及Value
    k = 0
    temp0 =''
    for  i in range(0,len(T)):
        for j in range(0,len(s)):
            if s[j] == T[i]:
                break;
            k = k+1
        if k == len(s):
            s.append(T[i])
        k = 0
    for i in range(0,len(s)):
        for j in range(0,len(s)):
            if i == len(s)-j-1 :
                temp0 = temp0 +'1'
            else :
                temp0 = temp0 + '0'
        r.append(temp0)
        temp0 = ''
    print(r)
    print(s)

    #生成T'=T1序列,是被换成二进制后的序列
    T1 = ''
    for i in range(0,len(T)):
        for j in range(0,len(s)):
            if s[j] == T[i]:
                T1 = T1 + r[j]

    print(T1)

    """
    print(int(T1,2))
    print(T1[:-3])
    print(int(T1[:-3],2))
    print(bin(int(T1,2)>>3)[2:])
    print(bin(int(T1[:-3],2))[2:])
    """

    # 计算C(T1)
    CT = []
    temp = []
    W1 = []  #存放T1 与T2序列相重合的二进制位数
    T2 = '' #是移位后的序列
    for i in range(0,int(len(T)/2)):
        for j in range(0,len(s)*(i+1)):
            T2 = T2 + '0'
        T2 = T2 + T1[:(-1 * len(s)*(i+1))]
        CT.append(FFT(T1,T2,temp))
        W1.append(temp)

        temp = []
        T2 = ''
    print(W1)

    #计算Wp,k和Wp,k,l
    W2 ={}
    for p in range(0,len(W1)):
        p=p+1
        for j in range(0,len(W1[p-1])):
            k = W1[p-1][j] % len(s)
            str_temp = str(p)+"_"+str(k)
            if str_temp in W2 :
                W2[str_temp].append(W1[p-1][j])
            else:
                W2[str_temp] = []
                W2[str_temp].append(W1[p-1][j])
    print(W2)

    W3 = {}
    F = {}
    for pk in W2.keys():
        for j in range(0,len(W2[pk])):
            temp = pk.split("_",1)
            p = temp[0]
            k = temp[1]
            l = (len(T) - int(p) - 1 - int(W2[pk][j]/len(s)) )%int(p)
            str_temp = pk+ "_" +str(l)
            if str_temp in W3 :
                W3[str_temp].append(W2[pk][j])
            else:
                W3[str_temp] = []
                W3[str_temp].append(W2[pk][j])
            str_tempF = s[int(k)] + "_"+str(p)+"_"+str(l)
            if str_tempF in F:
                F[str_tempF] = F[str_tempF]+1
            else:
                F[str_tempF] = 1
    print(W3)
    print(F)

    S = [[]for i in range(0,int(len(T)/2)+1)]              #存放根据定义3生成的pattern
    for i in range(0,len(S)):
            S[i]=[""for j in range(1,i+1)]

    for i in F.keys():
        p = int(i.split("_",2)[1])
        l = int(i.split("_",2)[2])
        if ((len(T)-l)%p) == 0:
            t = F[i]/((len(T)-l)/p-1)
        else:
            t = F[i]/((len(T)-l)/p)
        temp = i.split("_",2)[0] + "_" + str(p)+"_"+str(l)
        if t>=conf :
            if temp in single_result:
                if single_result[temp]<t:
                    single_result[temp] = t
                    S[p][l] = S[p][l] + i.split("_", 2)[0]

                    pattern = ""
                    for k in range(0, p):
                        if k == l:
                            pattern = pattern + i.split("_", 2)[0]
                        else:
                            pattern = pattern + "*"
            else :
                single_result[temp] = t

                pattern = ""
                for k in range(0, p):
                    if k == l:
                        pattern = pattern + i.split("_", 2)[0]
                    else:
                        pattern = pattern + "*"
                result[pattern] = t
                if S[p][l] != "":
                    S[p][l] = i.split("_", 2)[0]
                else :
                    S[p][l] = S[p][l] + i.split("_", 2)[0]
    print(single_result)
    print(result)
    return  result


    '''
    for i in range(1,len(S)):
        for j in range(0,len(S[i])):
            S[i][j]=S[i][j]+"*"
    print(S)


    #生成候选周期标识pattern
    flag=0
    temp = []
    for i in range(1,len(S)):
            for pro in itertools.product(S[i],S[i]):
                print(pro)
'''


path = "E:\dns_detection\intervalToStr.txt"
for line in open(path,"r"):
    dns = line.split(" ")
    periodResult = symbolDetection(dns[2], 0.6)
    if periodResult == {}:
        continue
    result = dns[0] + " "+dns[1] + " "+dns[2]+" "
    for i in periodResult.keys():
        result = result +i + ":"+ str(periodResult[i])+" "
    result = result+"\n"
    print(result)
    f = open("E:\dns_detection\conv_symbolDetection.txt","a")
    f.write(result)


'''
W=[]
print(FFT("001100100100001010010","000001100100100001010",W))
print(W)



T = 'abcabbabcb'
symbolDetection(T,0.333333)

'''