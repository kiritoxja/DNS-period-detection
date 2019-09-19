import pandas as pd
from sklearn.ensemble import RandomForestClassifier
# from RF import Rf_format
import pickle
from sklearn.externals import joblib
from numpy.core.umath_tests import inner1d
import pickle as pl



def RF_train(feature_list):

    f_train_path=r'D:\M\trainCode\formatData\rf_train_featured.txt'
    f_test_path=r'D:\M\trainCode\formatData\rf_test_featured.txt'
    n_features=len(feature_list)
    n_features=17

    predictors =[str(i+1) for i in range(n_features)]
    name=['label']
    name.extend(predictors)
    data_train=pd.read_table(f_train_path,names=name,sep=' ')
    data_test=pd.read_table(f_test_path,names=name,sep=' ')
    #label=2 feature=13 sample=269
    #predictors =['A','B','C','D','E','F','G','H','I','J','K','L','M']
    sample_leaf_options = list(range(1, 100, 3))
    n_estimators_options = list(range(1, 100, 5))
    ground_truth = data_test['label']
    results = []

    for leaf_size in sample_leaf_options:
        for n_estimators_size in n_estimators_options:
            alg = RandomForestClassifier(min_samples_leaf=leaf_size,\
                                         n_estimators=n_estimators_size, random_state=50)

            alg.fit(data_train[predictors],data_train['label'])
            predict = alg.predict(data_test[predictors])
            results.append((leaf_size, n_estimators_size, (ground_truth == predict).mean()))
            #print((ground_truth == predict).mean())

    print(max(results, key=lambda x: x[2]))
    max_list=max(results, key=lambda x: x[2])
    best_leaf_size=max_list[0]
    best_estimators_size=max_list[1]
    alg = RandomForestClassifier(min_samples_leaf=best_leaf_size,\
                                         n_estimators=best_estimators_size, random_state=50)
    alg.fit(data_train[predictors],data_train['label'])
    print('___________________________________________')
    print('score')
    print(alg.score(data_train[predictors],data_train['label']))
    print(alg.score(data_test[predictors],data_test['label'] ))
    test_predict=alg.predict(data_test[predictors])
    classNum=int(max(ground_truth))

    statistical_result = [[0] * classNum for i in range(classNum)]
    for i in range(ground_truth.shape[0]):
        statistical_result[int(ground_truth[i]) - 1][int(test_predict[i]) - 1] += 1
    print('_______________')
    print(statistical_result)
    print('_______________')
    pkl_path = r'D:\M\trainCode\result\rf_f_%d.pkl' % (n_features)
    with open(pkl_path, 'wb') as f:
        pickle.dump(statistical_result, f)

    #b保存模型
    joblib.dump(alg, r'D:\M\trainCode\RF\model_f_%d.pkl'%(n_features))
    #model = joblib.load(f)

def main(featureList):
    sourece_path= r'D:\M\trainCode\formatData'
    # Rf_format.format(featureList,sourece_path)
    RF_train(featureList)

if __name__=='__main__':
    main([1, 2, 3, 4, 5, 7, 8])