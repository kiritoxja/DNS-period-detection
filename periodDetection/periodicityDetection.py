
from  coreClass.util import Edge
from  coreClass.util import Period
from  coreClass.util import Tree
import pickle as pk
'''
 trees : 待进行周期检测的后缀树，list 类型
 lens : 总的字符串长度
 towin : 容忍的时间差
 minConfidence : 最低置信度
'''


def periodicityDetection(trees, towin, minConfidence):
    for tree in trees:                  #遍历树
        periodCollection = {}
        for edge in tree.edges:         #遍历边
            if len(edge.pattern) > (tree.lens/2) :
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
                    if (diffValue < edge.value)|(diffValue == 1)| (diffValue >1 / 3 * tree.lens )| (current[i] > 0.5 * tree.lens) :
                        continue

                    # 初始化候选周期p相关信息
                    p = Period(edge.pattern, diffValue, current[i], len(edge.pattern))
                    if ('%s_%d')%(p.pattern,p.val)in periodCollection.keys() :
                        continue
                    p.foundPosCount = 0

                    # 初始化A B C preSubCurValue
                    sumPerVal = 0
                    preSubCurValue = -5           # 前一个pattern出现的位置
                    currStPos = p.stops           # 当前pattern出现的位置
                    subCurrent = current[i]

                    j = i
                    while (j<len(edge.current)):  # j 是出现向量的索引
                        A = subCurrent - currStPos
                        if 0 <= (p.val - A%p.val) <=towin :
                            if j<len(edge.current)-1:
                                if current[j+1] - currStPos > p.val:
                                     B = int(A / p.val)+1
                                else:
                                    B = int(A / p.val)
                            else :
                                B = int(A / p.val)
                        else:
                            B = int(A / p.val)
                        C = A - (B * p.val)
                        if -1 * towin <=C <=towin: # C在容忍的误差内
                            if (preSubCurValue - currStPos) != B:
                                p.foundPosCount = p.foundPosCount + 1
                                preSubCurValue = subCurrent
                                currStPos = subCurrent
                                sumPerVal = sumPerVal + (p.val + C)
                        if j<len(edge.current)-1:
                            subCurrent = current[j+1]
                        j =j+1

                    y = 0
                    if (tree.lens - p.stops) % p.val >= edge.value:
                        y = 1
                    else:
                        y = 0
                    p.conf = p.foundPosCount / (int((tree.lens - p.stops)/p.val) + y)        #。。。。？
                    if p.conf > 1:
                        f = open("E:\\dns_detection\\error.txt","a")
                        str0 = ""
                        for c in edge.current:
                            str0 = str0 +  " " + str(c)
                        f.write(('%s_%s %s %d %d %d %d   %s \n') % (tree.host, tree.domain, p.pattern, p.val,p.foundPosCount, (int((tree.lens - p.stops)/p.val) + y),tree.lens,str0))
                        f.close()
                    if p.conf >= minConfidence:
                        p.avgVal = int((sumPerVal - p.val) / (p.foundPosCount - 1))
                        pattern_period = 0
                        for char in list(p.pattern):
                            pattern_period = pattern_period + float(tree.time2StrDict[char])
                        p.pattern_period = pattern_period
                        periodCollection[('%s_%d')%(p.pattern,p.val)] = p


     # 生成结果txt
        f = open("E:\\dns_detection\\final_result.txt","a")
        if periodCollection:
            result = ('%s %s')%(tree.host,tree.domain)
            for pattern in periodCollection.keys():
                    period_info = (' %s,%d:%d,%f ')%(periodCollection[pattern].pattern,periodCollection[pattern].pattern_period,periodCollection[pattern].avgVal,periodCollection[pattern].conf )
                    result = result + period_info
                    print(periodCollection[pattern].pattern)
                    print(periodCollection[pattern].val)
                    print(periodCollection[pattern].foundPosCount)
                    print(periodCollection[pattern].conf)
            result = result +'\n'
            f.write(result)
        f.close()


'''

edge1 = Edge('ab',[0,3,6],2)
edge2 = Edge("abb",[3,6],3)

edge3 = Edge("a",[2,7,12,17,18,22],1)
edge4 = Edge("b",[3,8,12,13],1)
edge5 = Edge("c",[1,6,10,15],1)
edge6 = Edge("ab",[4,9,15,20])

edge7 = Edge("d", [1,10,28,37],1)

tree1 = Tree(9,[edge1,edge2],"主机1","域名1",{"a":3, "b":2})
tree2 = Tree(33,[edge3,edge4,edge5,edge6],"主机2","域名2",{"a":3, "b":2, "c":1})
tree3 = Tree(40,[edge7],"主机3","域名3",{'d':1})

trees = [tree1,tree2,tree3]
period = periodicityDetection(trees,1,0)



'''
trees = pk.load(open("E:\\dns_detection\\Trees.pkl","rb+"))
#print(trees)



#periodicityDetection([Tree(13,[Edge('a',[0,1,2,4,5,6,7,8,9,10,11,12],1)],"zhuji","domain",{"a":117})],1,0)
periodicityDetection(trees,1,0.3333)





