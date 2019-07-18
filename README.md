# DNS period detection


初步处理数据格式（dns.txt）

格式：  主机(host) 域名(domain) 请求次数(times) 请求时间(time) 

例子：  10.59.13.204 android.clients.google.com 2 1562898034.163875 1562898034.19257



- 读取dns.txt 生成时间间隔数据     main/timeStampInterval.py
- 读取时间间隔数据转化为字符串   dataProcess/dataTransfer
- 将时间间隔字符串生成后缀树并转化成对应的边集合  main/String2OccurVec