#计算六种算法的混淆矩阵
import pickle
import os

class TestList:
    baseDir = os.path.dirname(os.getcwd())
    with open(os.path.join(baseDir, 'ML', 'test_shuffle.pkl'), 'rb') as fShuffle:
        testList = pickle.load(fShuffle)


def getLable(testList:list,index:int,threshold:float):
    return [ 0 if i[index+1] <threshold else 1 for i in testList]

def calConfusion(true_label:list,predict_label:list,name):
    classNum = 2
    statistical_result = [[0] * classNum for i in range(classNum)]
    for i in range(len(true_label)):
        statistical_result[true_label[i]][predict_label[i]] += 1
    return statistical_result
    print('------')
    print(name)
    print(statistical_result)
    print((statistical_result[0][0]+statistical_result[1][1])/(statistical_result[0][0]+statistical_result[1][1]+statistical_result[0][1]+statistical_result[1][0]))
    print('------')

def getTrueLabelAndPredictLable(name , confidence):
    testList = TestList.testList
    true_label = [i[0] for i in testList]
    swicth ={
        "STNR":getLable(testList,0,confidence),
        "WARP":getLable(testList,1,confidence),
        "AUTO":getLable(testList, 2, confidence),
        "CONV_SYM":getLable(testList,3,confidence),
        "CONV_SEG":getLable(testList,4,confidence),
        "FFT":getLable(testList,5,confidence)
    }
    return true_label,swicth[name]

if __name__ == '__main__':
    testList = TestList.testList
    true_label = [i[0] for i in testList ]
    STNR_label = getLable(testList,0,0.6)
    WARP_label = getLable(testList,1,0.6)
    AUTO_label = getLable(testList,2,0.6)
    CONV_SYM_label = getLable(testList,3,0.6)
    CONV_SEG_label = getLable(testList,4,0.6)
    FFT_label = getLable(testList,5,0.6)
    calConfusion(true_label,STNR_label,"STNR")
    calConfusion(true_label, WARP_label, "WARP")
    calConfusion(true_label, AUTO_label, "AUTO")
    calConfusion(true_label, CONV_SYM_label, "CONV_SYM")
    calConfusion(true_label, CONV_SEG_label, "CONV_SEG")
    calConfusion(true_label, FFT_label, "FFT")


