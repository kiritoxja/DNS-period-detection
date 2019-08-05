#读入分割字符串数据   产生 模式：置信度 结果

import AutocorrelationDetection.candidate as candidate
import AutocorrelationDetection.maxSubpatternTree as maxSubpatternTree
import os

if __name__ == '__main__':
    confidenceThreshold = 0.6
    baseDir = os.path.dirname(os.getcwd())
    with open(os.path.join(baseDir, 'processedData', 'intervalToStr.txt')) as fread:
        with open(os.path.join(baseDir, 'processedData', 'Autocorrelation_patterns.txt'), 'w') as fwrite1:
            with open(os.path.join(baseDir, 'processedData', 'Autocorrelation_result.txt'), 'w') as fwrite2:
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
                    for period in condidateP:
                        patternsDict = maxSubpatternTree.maxSubpattern(originString,period,confidenceThreshold)
                        if None == patternsDict:
                            continue
                        else:
                            patterns.append(patternsDict)
                    if len(patterns) == 0:
                        continue
                    writeStr1 = host +' '+domain +' ' + originString
                    writeStr2 = host + ' ' + domain + ' ' + originString
                    flag = False
                    for pattern in patterns:
                        dictPeriod = pattern['period']
                        pattern.pop('period')
                        for k,v in pattern.items():
                            writeStr1 += (' '+k+':'+str(v))
                            #通配符小于等于一半 认为是有周期的
                            if k.count(maxSubpatternTree.wildcard)<= dictPeriod/2:
                                flag = True
                                writeStr2 += (' '+k+':'+str(v))
                    writeStr1 += '\n'
                    fwrite1.write(writeStr1)
                    if flag:
                        writeStr2 += '\n'
                        fwrite2.write(writeStr2)
                    count+=1
                    print(str(count)+'/'+'444')