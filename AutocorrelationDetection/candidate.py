import numpy as np

def shift(a,shiftv):
    #计算a和a移位shiftv之后的自相关值
    return np.dot(a,[a[(i-shiftv)%len(a)] for i in range(len(a))])

def generateCondidateP(a,minThreshold):
    #计算其移位1 --  len/2 的自相关值   将自相关值大于阀值的作为候选周期
    candidateP=[]
    for i in range(1,len(a)//2+1):
        value = shift(a,i)
        if value >= minThreshold*(len(a)//i):
            candidateP.append(i)
    return candidateP


###读入初始字符串  产生候选周期列表
def candidatePeriod(originString,minThreshold):
    #首先产生所有字母的二进制向量
    alphabet = set(originString)
    alphabet2VectorDict = {}
    for i in alphabet:
        alphabet2VectorDict[i] = []
    for i in originString:
        for key in list(alphabet2VectorDict.keys()):
            if i == key:
                alphabet2VectorDict[key].append(1)
            else:
                alphabet2VectorDict[key].append(0)

    #对于每一个二进制向量  计算其移位1 --  len/2 的自相关值   将自相关值大于阀值的作为候选周期
    candidateP = []
    for vector in list(alphabet2VectorDict.values()):
        candidateP.extend(generateCondidateP(vector,minThreshold))

    #将候选周期去重 即将重复周期组合为一个group
    return list(set(candidateP))
