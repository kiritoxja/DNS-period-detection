#绘制5种字符串算法的acc  F1 score  auc 对比图
from matplotlib.font_manager import FontProperties
from mpl_toolkits.mplot3d import Axes3D
import ML.ConfusionMatrix
import numpy as np
import sklearn.metrics
import matplotlib.pyplot as plt
from matplotlib import cm

def cal(true_label:list,predict_label:list):
    #计算acc f1  auc
    acc = sklearn.metrics.accuracy_score(true_label,predict_label)
    f1 = sklearn.metrics.f1_score(true_label,predict_label)
    auc = sklearn.metrics.roc_auc_score(true_label,predict_label)
    return acc,f1,auc

def drawNum(results,xlabel:str):
    #绘制ACC和叶子节点数量或估计器数量的图
    Chinafont = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=12)
    Englishfont = FontProperties(fname=r"C:\Windows\Fonts\times.ttf", size=12)
    styles = ['b-']
    plt.figure()
    plt.plot([i[0] for i in results], [i[1] for i in results], styles[0])
    plt.xlabel(xlabel, fontproperties=Chinafont)
    plt.ylabel("ACC", fontproperties=Englishfont)
    plt.show()

def ThreeDdraw(results):
    #绘制三维数据调优图
    Chinafont = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=12)
    Englishfont = FontProperties(fname=r"C:\Windows\Fonts\times.ttf", size=12)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax = fig.gca(projection='3d')
    x=np.array([i[0] for i in results])
    y=np.array([i[1] for i in results])
    z=np.array([i[2] for i in results])
    ax.scatter(x, y, z, c='b', marker='o')
    ax.set_xlabel('leaf_size')
    ax.set_ylabel('eestimator_num')
    ax.set_zlabel('ACC')
    plt.show()

if __name__ == '__main__2':
    ThreeDdraw(((1,1,0.2),(2,2,0.8)))





if __name__ == '__main__1':
    # 根据混淆矩阵 [[68, 3], [14, 182]]  计算机器学习的指标
    true_label = []
    predict_label = []
    for i in range(68):
        true_label.append(0)
        predict_label.append(0)
    for i in range(3):
        true_label.append(0)
        predict_label.append(1)
    for i in range(14):
        true_label.append(1)
        predict_label.append(0)
    for i in range(182):
        true_label.append(1)
        predict_label.append(1)
    print(cal(true_label,predict_label))




if __name__ == '__main__':
    #画图
    confidences = [i*0.1 for i in range(11)]
    names = ['STNR','WARP',"AUTO","CONV_SYM","CONV_SEG","FFT"]
    Accs = []
    F1s = []
    Aucs = []

    for name in names:
        Acc = []
        F1 = []
        Auc = []
        for confidence in confidences:
            true_label,predict_label = ML.ConfusionMatrix.getTrueLabelAndPredictLable(name,confidence)
            acc, f1, auc = cal(true_label,predict_label)
            Acc.append(acc)
            F1.append(f1)
            Auc.append(auc)
        Accs.append(Acc)
        F1s.append(F1)
        Aucs.append(Auc)

    #开始画图
    # plt.rcParams['figure.figsize'] = (8.0, 4.0)
    Chinafont = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=12)
    Englishfont = FontProperties(fname=r"C:\Windows\Fonts\times.ttf", size=12)
    styles =['b-','g-.','r-v','c-o','m-^','y-D']

    Yvalues = []
    Yvalues.append(Accs)
    Yvalues.append(F1s)
    Yvalues.append(Aucs)
    YvalueNames = ['ACC','F1-Score','AUC']

    #开始画每张图
    for j in range(len(Yvalues)):
        plt.figure()
        plots= []
        print('---------')
        print(YvalueNames[j])
        for i in range(len(names)):
            maxValue = max(Yvalues[j][i])
            print(Yvalues[j][i].index(maxValue)*0.1,maxValue,end='  ')
            tempPlot,=plt.plot(confidences,Yvalues[j][i],styles[i])
            plots.append(tempPlot)
        # plt.title("标题", fontproperties = font)
        print('---------')
        plt.xlabel("confidence", fontproperties=Englishfont)
        plt.ylabel(YvalueNames[j],fontproperties = Englishfont)
        plt.legend(plots,names, loc='best')
        plt.show()
