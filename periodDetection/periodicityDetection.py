
from  coreClass.util import Edge
from  coreClass.util import Period
from  coreClass.util import Tree

'''
 trees : 待进行周期检测的后缀树，list 类型
 lens : 总的字符串长度
 towin : 容忍的时间差
 minConfidence : 最低置信度
'''


def periodicityDetection(trees, lens, towin, minConfidence):
    all_period = {}
    for tree in trees:                  #遍历树
        periodCollection = {}
        for edge in tree.edges:         #遍历边
            if len(edge.pattern) > (lens/2) :
                continue
            else:
                current = edge.current  # initialize current with the starting node of the edge

                for i in range(len(edge.current)- 1):   # i 是出现向量的索引
                    # print(i)
                    diffValue = current[i+1] - current[i]
                    # ignore this occurrence if period < length of pattern  OR period > 33 % of series  length  OR period
                    # starting position > half of series length
                    '''                
                    print((diffValue < edge.value))
                    print((diffValue == 1))
                    print(('%d , %d')%(diffValue , (1 / 3 * lens )))
                    print(diffValue >(1 / 3 * lens ))
                    print( (current[i] > 0.5 * lens))
                    '''
                    if (diffValue < edge.value)|(diffValue == 1)| (diffValue >1 / 3 * lens )| (current[i] > 0.5 * lens) :
                        continue

                    # 初始化候选周期p相关信息
                    p = Period()
                    p.pattern = edge.pattern
                    p.val = diffValue
                    p.stops = current[i]
                    p.length = edge.value
                    if ('%s_%d')%(p.pattern,p.val)in periodCollection.keys() :
                        continue
                    p.foundPosCount = 0

                    # 初始化A B C preSubCurValue
                    sumPerVal = 0
                    preSubCurValue = 0           # 前一个pattern出现的位置
                    currStPos = p.stops           # 当前pattern出现的位置
                    subCurrent = current[i]

                    j = i
                    while (j<len(edge.current)):  # j 是出现向量的索引
                        A = subCurrent - currStPos
                        B = int(A / p.val)
                        C = A - (B * p.val)
                        if -1 * towin <C <towin: # C在容忍的误差内
                            if (preSubCurValue - currStPos) != B:
                                p.foundPosCount = p.foundPosCount + 1
                                preSubCurValue = subCurrent
                                currStPos = subCurrent
                                sumPerVal = sumPerVal + (p.val + C)
                        if j<len(edge.current)-1:
                            subCurrent = current[j+1]
                        j =j+1

                    y = 0
                    if (lens - p.stops) % p.val >= edge.value:
                        y = 1
                    else:
                        y = 0
                    p.conf = p.foundPosCount / (int((lens - p.stops)/p.val) + y)        #。。。。？
                    if p.conf >= minConfidence:
                        p.avgVal = int((sumPerVal - p.val) / (p.foundPosCount - 1))
                        periodCollection[('%s_%d')%(p.pattern,p.val)] = p
        all_period[('%s_%s')%(tree.host,tree.domain)] = periodCollection

    for p in all_period.keys():                         # 打印信息
        for pattern in all_period[p].keys():
                print(all_period[p][pattern].pattern)
                print(all_period[p][pattern].val)
                print(all_period[p][pattern].foundPosCount)
                print(all_period[p][pattern].avgVal)
                print(all_period[p][pattern].conf)
    return all_period


'''

edge1 = Edge()
edge1.pattern = 'ab'
edge1.value = 2
edge1.current = [0,3,6]
edge1.len = 3

edge2= Edge()
edge2.pattern = 'a'
edge2.value = 1
edge2.current = [2,7,12,17,18,22]
#edge2.current = [2,7, 12, 16 ,17]

edges = []
edges.append(edge2)
#edges.append(edge1)
tree = Tree()
tree.edges = edges
tree.host = 'IP地址'
tree.domain = '域名'

trees = []
trees.append(tree)
period = periodicityDetection(trees,33,1,0.3)
for p in period.keys():
    for pattern in period[p].keys():
        print(period[p][pattern].pattern)
        print(period[p][pattern].val)
        print(period[p][pattern].foundPosCount)
        print(period[p][pattern].avgVal)
        print(period[p][pattern].conf)

'''








