# DNS period detection


初步处理数据格式（dns.txt）

格式：  主机(host) 域名(domain) 请求次数(times) 请求时间(time) 

例子：  10.59.13.204 android.clients.google.com 2 1562898034.163875 1562898034.19257




- 读取dns.txt 生成时间间隔数据     main/timeStampInterval.py
- 读取时间间隔数据转化为字符串   dataProcess/dataTransfer
- 将时间间隔字符串生成后缀树并转化成对应的边集合  main/String2OccurVec



## 后缀树结果

最终结果数据格式（final_result.txt）

格式： 主机 域名 周期字符串1,对应周期间隔长度:字符串出现平均周期,周期置信度 周期字符串2,对应周期间隔长度:字符串出现平均周期,周期置信度 ...

例子： 10.59.13.204 android.clients.google.com ab,5:3,1.000000  abb,7:3,1.000000  

注：每个字符串中的pattern的周期，只取置信度最高的那个周期



## WARP（时间扭曲计算）

最终结果数据格式（final_result.txt）

只取置信度大于0.8的最高的周期

格式：主机  域名  原始字符串  周期值   置信度

```
192.168.248.165 sbcglobalnet.com aaaaaaaaaaaaabaaaaaaaaaaaaa 1 1.0
```



## Autocorrelation（基于自相关的周期检测）

通配符太多 会导致树指数增长  只选了通配符占匹配模式一半以下的匹配模式

1. 扫描一遍初始字符串（长度为N）为每个字母建立长度为N的二进制向量   如abab  a:1010  b:0101
2. 算自相关值  得到候选周期
3. 运用maxSubpattern算法 得到模式的置信度

最终

其中.表示通配符

格式：主机  域名  原始字符串  周期模式   置信度

```
10.0.2.15 www.it885.com.cn aaabaaaaaaaaa a:0.9230769230769231 a.:1.0 .a:0.8333333333333334 aa:0.8333333333333334 .aa:1.0 aaa:0.75 aaa.:1.0 aaaa:0.6666666666666666 aaa.a:1.0 aaa.aa:1.0
```

