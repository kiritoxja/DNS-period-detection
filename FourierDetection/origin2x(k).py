import os
import pickle

if __name__ == '__main__':
    baseDir = os.path.dirname(os.getcwd())
    filt = 0
    writeList = []
    with open(os.path.join(baseDir, 'processedData', 'FFT_originData.txt')) as fread:
        with open(os.path.join(baseDir, 'processedData', 'FFT_x(n).pkl'), 'wb') as Objwrite:
            for line in fread:
                filt += 1
                if(filt<=3):
                    continue
                info = line.split(' ')
                host = info[0]
                domain = info[1]
                timestamps = info[3:]
                timesNumList = [float(i) for i in timestamps]
                minTime = min(timesNumList)
                tempList = [i - minTime for i in timesNumList]
                tempList.sort()
                k=0
                xn=[]
                xn.append(host)
                xn.append(domain)
                limit = len(tempList)
                for i in range(int(tempList[-1])+1):
                    tempCount = 0
                    while(k< limit and i<=tempList[k]<(i+1)):
                        tempCount+=1
                        k+=1
                    xn.append(tempCount)
                writeList.append(xn)
                print(str(filt) + '/444')
            pickle.dump(writeList,Objwrite)

