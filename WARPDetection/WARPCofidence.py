import numpy as np
from fastdtw import fastdtw



def dist(x,y):
    return 1 if x!=y else 0

def myDTW(x,y):
    x = [ord(i) - ord('a') for i in x]
    y = [ord(i) - ord('a') for i in y]
    distance, path = fastdtw(x, y, dist=dist)
    return distance


# WARP计算周期
def warp(string,confidenceThreshold):
    stringLength = len(string)
    stringList = np.array([i for i in string])
    maxConfidence = 0
    maxP = 0
    candidateP=[i+1 for i in range(0,stringLength//2)]
    for p in candidateP:
        distance= myDTW(stringList[p:], stringList[:-p])
        confidence = (stringLength - p - distance)/(stringLength - p)
        if confidence > maxConfidence:
            maxConfidence = confidence
            maxP = p
    if maxConfidence >= confidenceThreshold:
        return maxConfidence,maxP
    else:
        return None,None

if __name__ == '__main__':
    print(warp('abbadcccccccccccbadccccccccccbabeccccccccccbadccccccccccbabf', 0.8))
    stringList= 'cdgggggggdcidcjgfabigggggggdcigbdchgbggggggdcigeggggdcigggggggbggggbggggdcidcigggggg'
    p = 1
    print(myDTW(stringList[p:], stringList[:-p]))