import re
import itertools
import copy
import AutocorrelationDetection.globalVar as globalVar

wildcard = '.'

class patternTreeNode:

    def __init__(self,pattern):
        self.pattern = pattern
        self.parent = []
        self.children = {}  #{'0:a' : node} 该孩子节点少了第0个位置的'a'字符
        self.count = 0
        self.ancestors = [] #所有可达祖先节点

    def findAncestor(self):
        #找出该节点所有的可达祖先
        if len(self.parent) == 0:
            return
        for p in self.parent:
            if p not in self.ancestors:
                self.ancestors.append(p)
            p.findAncestor()
            for item in p.ancestors:
                if item not in self.ancestors:
                    self.ancestors.append(item)



    @staticmethod
    def find(root ,paths:list):
        #根据缺失路径查找是否有该子节点 ['0:a','1:b','1:c'] 缺了这些
        if len(paths) == 0:
            root.count += 1
            return True
        if paths[0] in root.children:
            return patternTreeNode.find(root.children[paths[0]],paths[1:])
        else:
            return False

    @staticmethod
    def addChildren(root,path):
        #路径下没找到该节点时  顺着路径添加孩子节点
        if len(path) == 0:
            return
        if path[0] in root.children:
            patternTreeNode.addChildren(root.children[path[0]],path[1:])
        else:
            #这个节点不存在于当前根节点的孩子节点 首先判断是否有这个节点
            #这个孩子节点应该有的pattern
            childPattern = copy.deepcopy(root.pattern)
            index = int(path[0].split(':')[0])
            char = path[0].split(':')[1]
            if isinstance(childPattern[index],str):
                childPattern[index] = wildcard
            else:
                childPattern[index].remove(char)
                if len(childPattern[index]) == 1:
                    childPattern[index] = childPattern[index][0]
            tempNode = None
            for node in globalVar.Nodes:
                if comparePattern(node.pattern,childPattern):
                    tempNode = node
            if tempNode == None:
                #这个节点不存在  要创造
                childNode = patternTreeNode(childPattern)
                globalVar.Nodes.append(childNode)
                if len(path) == 1:
                    childNode.count = 1
                childNode.parent.append(root)
                root.children[path[0]] = childNode
                patternTreeNode.addChildren(root.children[path[0]], path[1:])
            else:
                #该孩子节点存在
                tempNode.parent.append(root)
                root.children[path[0]] = tempNode
                patternTreeNode.addChildren(root.children[path[0]], path[1:])

#返回模式是否与该segment匹配
def matchPattern(pattern,segment):
    if re.match(pattern,segment) == None:
        return False
    else:
        return True

#替换字符串指定位置字符
def replace_char(string,char,index):
     string = list(string)
     string[index] = char
     return ''.join(string)

#判断两个pattern ['a',['b','a']]    ['a',['a',['b']]]相等:
def comparePattern(pattern1,pattern2):
    if len(pattern1) != len(pattern2):
        return False
    for i,j in zip(pattern1,pattern2):
        if type(i) != type(j):
            return False
        if isinstance(i,str):
            if i !=j :
                return False
        else:
            if sorted(i) != sorted(j):
                return False
    return True

#查找该段 和 Cmax匹配的max-subpattern
def max_subpattern(segment,Cmax):
    maxsubpattern=[]
    for i,j in zip(segment,Cmax):
        if isinstance(j,str):
            if j == i:
                maxsubpattern.append(j)
            else:
                maxsubpattern.append(wildcard)
        else:
            if i in j:
                maxsubpattern.append(j)
            else:
                maxsubpattern.append(wildcard)
    return maxsubpattern

#得到Cmax到maxSub的所有path
def Cmax2maxSub(maxSub,Cmax):
    paths = [[]]
    index = 0
    for i ,j in zip(maxSub,Cmax):
        if j==wildcard:
            index+=1
            continue
        if isinstance(j,str):
            if i==j:
                index+=1
                continue
            else:
                for item in paths:
                    item.append(str(index)+':'+j)
        else:
            #这个位置是[a,b]
            diffList = list(set(j) - set(i))
            #获取缺少字母的全排列
            fullyArranged = list(itertools.permutations(diffList))
            for item in copy.deepcopy(paths):
                for arranges in fullyArranged:
                    addItem = copy.deepcopy(item)
                    for arrange in arranges:
                        addItem.append(str(index)+':'+arrange)
                    paths.append(addItem)
                paths.remove(item)
        index+=1

    result = []
    #将paths每个全排
    for l in paths:
        for tempItem in list(itertools.permutations(l)):
            if list(tempItem) not in result:
                result.append(list(tempItem))

    return result

#输入一个字符串  周期  置信度  输出该周期下所有大于置信度的周期模式
def maxSubpattern(originString,P,threshold):
    globalVar.Nodes = []
    patterns = {} #模式：置信度字典
    alphabet = list(set(originString))
    m = len(originString) // P #该字符串有m段
    segments = []  #字符串的所有段
    for i in range(m):
        segments.append(originString[i*P:(i+1)*P])

    #寻找所有匹配次数大于threshold*m的1-pattern集合
    F0 = wildcard*P
    F1 = []
    for i in range(P):
        for j in alphabet:
            F1.append(replace_char(F0,j,i))
    F12Counts = {}
    for segment in segments:
        for pattern in F1:
            if matchPattern(pattern,segment):
                if pattern in F12Counts:
                    F12Counts[pattern]+=1
                else:
                    F12Counts[pattern] =1
    F1Filter = []
    for key in F12Counts:
        if F12Counts[key] >= threshold*m:
            F1Filter.append(key)

    #如果F1Filter为空  则不存在周期性直接返回None
    if len(F1Filter) == 0:
        return None
    for item in F1Filter:
        patterns[item] = F12Counts[item]/m

    # F1Filter=['a...','.b..','.c..','..d.']
    # P=4
    #从F1Filter 得到 Cmax
    Cmax=[]
    for i in range(P):
        tempString=''
        values = set()
        for j in F1Filter:
            values.add(j[i])
        values = list(values)
        if len(values)>1 and wildcard in values:
            values.remove(wildcard)
        if len(values)>1:
            tempString = []
            for value in values:
                tempString.append(value)
        else:
            tempString += values[0]
        Cmax.append(tempString)

    #开始构建subpattern树
    rootNode = patternTreeNode(Cmax)
    for segment in segments:
        #去除最大匹配模式中非通配符长度小于2的
        maxSub = max_subpattern(segment,Cmax)
        if(len([i for i in maxSub if i!=wildcard]))<2:
            continue
        #@@ 通配符太多的时候 根到该maxsub路径太多 是阶乘  如9的全排都有362880个了
        if(maxSub.count(wildcard))>len(maxSub)/2:
            continue
        #得到Cmax到maxSub的所有path
        paths = Cmax2maxSub(maxSub , Cmax)

        #先判断能不能找到这个maxSub节点
        if not patternTreeNode.find(rootNode,paths[0]):
            #没有该节点 就要将每条路径都添加
            for path in paths:
                patternTreeNode.addChildren(rootNode,path)

    #构建好subpattern树以后 遍历这颗树 将所有frequency/m > threshold 的模式保存
    for node in globalVar.Nodes:
        node.findAncestor()
    globalVar.Nodes.append(rootNode)

    for node in globalVar.Nodes:
        frequent = node.count
        for ancestor in node.ancestors:
            frequent += ancestor.count
        if frequent/m >= threshold:
            b=[]
            for i in node.pattern:
                if isinstance(i, str):
                    b.append(i)
                else:
                    b.append('[')
                    for j in i:
                        b.append(',')
                        b.append(j)
                    b.pop()
                    b.append(']')
            patterns[''.join(b)] = frequent/m
    patterns['period'] = P

    return patterns



if __name__ == '__main__':
    # Cmax=['a',['b','c'],'d',wildcard]
    # maxSubs=[[wildcard,'c','d',wildcard] , [wildcard,'b','d',wildcard] , ['a',wildcard,'d',wildcard] , ['a','c',wildcard,wildcard], ['a','b',wildcard,wildcard]]
    # rootNode = patternTreeNode(Cmax)
    # for maxSub in maxSubs:
    #     paths = Cmax2maxSub(maxSub, Cmax)
    #     if not patternTreeNode.find(rootNode,paths[0]):
    #         #没有该节点 就要将每条路径都添加
    #         for path in paths:
    #             patternTreeNode.addChildren(rootNode,path)
    #
    # print(1)
    # print(2)

    print(maxSubpattern('cdgggggggdcidcjgfabigggggggdcigbdchgbggggggdcigeggggdcigggggggbggggbggggdcidcigggggg ',25,0.6))

