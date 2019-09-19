#产生WARP 周期检测结果
from gevent import os
import WARPDetection.WARPCofidence as Confidence


if __name__ == '__main__':
    confidenceThreshold = 0
    baseDir = os.path.dirname(os.getcwd())
    with open(os.path.join(baseDir,'processedData','intervalToStr.txt')) as fread:
        with open(os.path.join(baseDir,'processedData','WARP_result_new.txt'),'a') as fwrite:
            for line in fread:
                info = line.split(' ')
                host = info[0]
                domain = info[1]
                originString = info[2]
                maxConfidence, maxP = Confidence.warp(originString,confidenceThreshold)
                writeStr = host +' '+domain +' ' + originString
                if(maxP == None):
                    continue
                writeStr += ' '+str(maxP)+' '+str(maxConfidence)+'\n'
                fwrite.write(writeStr)