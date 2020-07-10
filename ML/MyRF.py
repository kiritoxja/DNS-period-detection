import random

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
# from RF import Rf_format
import pickle
from sklearn.externals import joblib
import pickle as pk
import os
import Draw.draw_StringPattern as draw



def RF_train():
    n_features = 6
    predictors =[str(i+1) for i in range(n_features)]
    name=['label']
    name.extend(predictors)
    train,test = getData()
    data_train=pd.DataFrame(train,columns = name)
    data_test=pd.DataFrame(test,columns = name)
    #label=2 feature=13 sample=269
    #predictors =['A','B','C','D','E','F','G','H','I','J','K','L','M']
    sample_leaf_options = list(range(1, 100, 3))
    n_estimators_options = list(range(1, 100, 5))
    ground_truth = data_test['label']
    results = []
    #只是用STNR 和 FFT的特征进行训练
    predictors=['1','6']

    # # 画图部分
    # estimators = []
    # for n_estimators_size in n_estimators_options:
    #     alg = RandomForestClassifier(n_estimators=n_estimators_size, random_state=50)
    #     alg.fit(data_train[predictors], data_train['label'])
    #     predict = alg.predict(data_test[predictors])
    #     estimators.append((n_estimators_size, (ground_truth == predict).mean()))
    # draw.drawNum(estimators, "估计器数量")
    # best_estimators = max(estimators, key=lambda x: x[1])
    # print('最佳估计器数量：', best_estimators[0])
    #
    # leaf_sizes = []
    # for leaf_size in sample_leaf_options:
    #     alg = RandomForestClassifier(min_samples_leaf=leaf_size, \
    #                                  n_estimators=best_estimators[0], random_state=50)
    #
    #     alg.fit(data_train[predictors], data_train['label'])
    #     predict = alg.predict(data_test[predictors])
    #     leaf_sizes.append((leaf_size, (ground_truth == predict).mean()))
    # draw.drawNum(leaf_sizes, "叶子节点数量")
    # best_leaf = max(leaf_sizes, key=lambda x: x[1])
    # print('最佳叶子数量：', best_leaf[0])


    #训练参数调优
    for leaf_size in sample_leaf_options:
        for n_estimators_size in n_estimators_options:
            alg = RandomForestClassifier(min_samples_leaf=leaf_size,\
                                         n_estimators=n_estimators_size, random_state=50)

            alg.fit(data_train[predictors],data_train['label'])
            predict = alg.predict(data_test[predictors])
            results.append((leaf_size, n_estimators_size, (ground_truth == predict).mean()))
            #print((ground_truth == predict).mean())

    #画图
    draw.ThreeDdraw(results)

    #使用最优参数进行训练
    print(max(results, key=lambda x: x[2]))
    max_list=max(results, key=lambda x: x[2])
    best_leaf_size=max_list[0]
    best_estimators_size=max_list[1]
    alg = RandomForestClassifier(min_samples_leaf=best_leaf_size,\
                                         n_estimators=best_estimators_size, random_state=50)
    alg.fit(data_train[predictors],data_train['label'])
    print('___________________________________________')
    print('score')
    print('train',alg.score(data_train[predictors],data_train['label']))
    print('test',alg.score(data_test[predictors],data_test['label'] ))
    test_predict=alg.predict(data_test[predictors])
    classNum=int(max(ground_truth))+1

    statistical_result = [[0] * classNum for i in range(classNum)]
    print(ground_truth.shape[0])
    for i in range(ground_truth.shape[0]):
        statistical_result[int(ground_truth[i])][int(test_predict[i])] += 1
    print('_______________')
    print(statistical_result)
    print('_______________')
    #保存混淆矩阵
    pkl_path = r'D:\code\项目\dns周期检测\DNS-period-detection\ML\rf_confusionMatrix_%d.pkl' % (n_features)
    with open(pkl_path, 'wb') as f:
        pickle.dump(statistical_result, f)

    #b保存模型
    # joblib.dump(alg, r'D:\code\项目\dns周期检测\DNS-period-detection\ML\model_f_%d.pkl'%(n_features))
    #model = joblib.load(f)

def getData():
    baseDir = os.path.dirname(os.getcwd())
    with open(os.path.join(baseDir, 'processedData', 'train.pkl'),'rb') as ftrain:
        with open(os.path.join(baseDir, 'processedData', 'test.pkl'),'rb') as ftest:
            trainData = pk.load(ftrain)
            testData=pk.load(ftest)
            train=[]
            test=[]
            for i in trainData:
                temp = [i[2]]
                for j in i[1]:
                    temp.append(j)
                train.append(temp)
            for i in testData:
                temp = [i[2]]
                for j in i[1]:
                    temp.append(j)
                test.append(temp)

            # #随机打乱
            benign = []
            mal = []
            for i in train:
                if i[0] <1:
                    benign.append(i)
                else:
                    mal.append(i)
            for i in test:
                if i[0] < 1:
                    benign.append(i)
                else:
                    mal.append(i)
            random.shuffle(benign)
            random.shuffle(mal)
            train=[]
            test=[]
            benign_num = int(len(benign)*0.4)
            mal_num = int(len(mal) * 0.4)
            train.extend(benign[:benign_num])
            test.extend(benign[benign_num:])
            train.extend(mal[:mal_num])
            test.extend(mal[mal_num:])

            with open(os.path.join(baseDir, 'ML', 'test_shuffle.pkl'), 'wb') as fShuffle:
                pk.dump(test,fShuffle)

            return train,test

if __name__ == '__main__':
    RF_train()