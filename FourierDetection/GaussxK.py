#产生高斯T检验后对应的xk


if __name__ == '__main__':
    import os
    import pickle

    baseDir = os.path.dirname(os.getcwd())
    writeList = []
    count = 0
    with open(os.path.join(baseDir, 'processedData', 'FFT_GaussFilt.txt')) as fread:
        with open(os.path.join(baseDir, 'processedData', 'FFT_Gauss_xn.pkl'), 'wb') as Objwrite:
            with open(os.path.join(baseDir, 'processedData', 'FFT_xn.pkl'), 'rb') as Objread:
                xnList =   pickle.load(Objread)
                for line in fread:
                    info = line.split(' ')
                    host = info[0]
                    domain = info[1]
                    for xn in xnList:
                        if(xn[0] == host and xn[1] ==domain):
                            writeList.append(xn)
                            break
                    count += 1
                    print(str(count) + '/315')
                pickle.dump(writeList, Objwrite)