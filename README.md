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

