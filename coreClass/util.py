
class Tree :
    lens = 0 # 字符串长度
    edges = [] # 中间边的集合
    host = ''  # 主机IP
    domain = '' #域名

class Edge:
    pattern = ''   # 后缀树边上的字符串
    current = []   # 出现向量
    value = 0      # 后缀树边对应的值


class Period:
    pattern = '' # 周期字符
    val = 0      # 周期长度
    stops = 0    # 当前所指的pattern的起始位置
    length = 0   # pattern的长度
    foundPosCount = -1 # 传说中的count,pattern在整个字符串中出现的字数
    conf = 0     # 周期性置信度
    avgVal = 0   # pattern 的平均周期
