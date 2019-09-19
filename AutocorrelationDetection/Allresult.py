#读入分割字符串数据   产生 模式：置信度 结果
#result文件只考虑了通配符占了一半以下的周期模式
#产生所有周期的置信度

import AutocorrelationDetection.candidate as candidate
import AutocorrelationDetection.maxSubpatternTree as maxSubpatternTree
import os

if __name__ == '__main__':
    confidenceThreshold = 0.6
    baseDir = os.path.dirname(os.getcwd())
    with open(os.path.join(baseDir, 'processedData', 'intervalToStr.txt')) as fread:
        with open(os.path.join(baseDir, 'processedData', 'Autocorrelation_result_new.txt'), 'w') as fwrite2:
            count = 0
            for line in fread:
                info = line.split(' ')
                host = info[0]
                domain = info[1]
                originString = info[2]
                condidateP = candidate.candidatePeriod(originString,confidenceThreshold)
                if(len(condidateP) == 0 ):
                    continue
                patterns = []
                confidenceThreshold = 0 #输出所有周期的置信度
                for period in condidateP:
                    patternsDict = maxSubpatternTree.maxSubpattern(originString,period,confidenceThreshold)
                    if None == patternsDict:
                        continue
                    else:
                        patterns.append(patternsDict)
                if len(patterns) == 0:
                    continue
                writeStr2 = host + ' ' + domain + ' ' + originString
                flag = False
                for pattern in patterns:
                    dictPeriod = pattern['period']
                    pattern.pop('period')
                    for k,v in pattern.items():
                        #通配符小于等于一半 认为是有周期的
                        if k.count(maxSubpatternTree.wildcard)<= dictPeriod/2:
                            flag = True
                            writeStr2 += (' '+k+':'+str(v))
                if flag:
                    writeStr2 += '\n'
                    fwrite2.write(writeStr2)
                count+=1
                print(str(count)+'/'+'444')