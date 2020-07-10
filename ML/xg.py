import pandas as pd
import xgboost as xgb
from sklearn.model_selection import GridSearchCV   #Perforing grid search
from sklearn.metrics import accuracy_score
import warnings
import pickle
from ML import MyRF


def xgTrain():

    warnings.filterwarnings(module='sklearn*', action='ignore', category=DeprecationWarning)

    n_features = 6
    predictors = [str(i + 1) for i in range(n_features)]
    name = ['label']
    name.extend(predictors)
    train, test = MyRF.getData()
    data_train = pd.DataFrame(train, columns=name)
    data_test = pd.DataFrame(test, columns=name)
    target='label'
    n_class = int(max(data_train[target]))+1

    #调参
    X_train=data_train[predictors]
    y_train =data_train[target]
    X_test =data_test[predictors]
    y_test=data_test[target]

    cv_params = {'n_estimators': list(range(400,850,50))}
    other_params = {'objective':'multi:softmax','num_class':n_class,'learning_rate': 0.1, 'n_estimators': 500, 'max_depth': 5, 'min_child_weight': 1, 'seed': 0,
                    'subsample': 0.8, 'colsample_bytree': 0.8, 'gamma': 0}
    def find_parameter(other_params,cv_params):
        model = xgb.XGBClassifier(**other_params)
        optimized_GBM = GridSearchCV(estimator=model, param_grid=cv_params,  cv=5, verbose=1) #scoring='accuracy'
        optimized_GBM.fit(X_train, y_train)
        evalute_result = optimized_GBM.cv_results_
        print('每轮迭代运行结果:')
        for i in range(len(evalute_result['params'])):
            print('mean:{0},  std:{1},   params:{2}'.format(evalute_result['mean_test_score'][i], \
                                                       evalute_result['std_test_score'][i], \
                                                       evalute_result['params'][i]))
        print('参数的最佳取值：{0}'.format(optimized_GBM.best_params_))
        print('最佳模型得分:{0}'.format(optimized_GBM.best_score_))
        return optimized_GBM.best_params_

    best_para=find_parameter(other_params,cv_params)
    n_estimators=best_para['n_estimators']
    #best_para={'n_estimators': 500}

    #调min_child_weight以及max_depth
    other_params = {'learning_rate': 0.1, 'n_estimators': n_estimators, 'max_depth': 5, 'min_child_weight': 1, 'seed': 0,
                    'subsample': 0.8, 'colsample_bytree': 0.8, 'gamma': 0}
    cv_params = {'max_depth': [3, 4, 5, 6, 7, 8, 9, 10], 'min_child_weight': [1, 2, 3, 4, 5, 6]}
    best_para = find_parameter(other_params, cv_params)
    max_depth=best_para['max_depth']
    min_child_weight=best_para['min_child_weight']

    #调gamma
    cv_params = {'gamma': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]}
    other_params = {'learning_rate': 0.1, 'n_estimators': n_estimators, 'max_depth': max_depth, 'min_child_weight':min_child_weight, 'seed': 0,
                    'subsample': 0.8, 'colsample_bytree': 0.8, 'gamma': 0, 'reg_alpha': 0, 'reg_lambda': 1}
    best_para = find_parameter(other_params, cv_params)
    gamma=best_para['gamma']


    #接着是subsample以及colsample_bytree
    cv_params = {'subsample': [0.4,0.5,0.6, 0.7, 0.8, 0.9], 'colsample_bytree': [0.4,0.5,0.6,0.7, 0.8, 0.9]}
    other_params = {'learning_rate': 0.1, 'n_estimators': n_estimators, 'max_depth': max_depth, 'min_child_weight':min_child_weight, 'seed': 0,
                    'subsample': 0.8, 'colsample_bytree': 0.8, 'gamma': gamma, 'reg_alpha': 0, 'reg_lambda': 1}
    best_para = find_parameter(other_params, cv_params)
    subsample,colsample_bytree=best_para['subsample'],best_para['colsample_bytree']


    #最后就是learning_rate，一般这时候要调小学习率来测试
    cv_params = {'learning_rate': [0.01, 0.05, 0.07, 0.1, 0.2]}
    other_params = {'learning_rate': 0.1, 'n_estimators': n_estimators, 'max_depth': max_depth, 'min_child_weight':min_child_weight, 'seed': 0,
                    'subsample': subsample, 'colsample_bytree': colsample_bytree, 'gamma': gamma, 'reg_alpha': 0, 'reg_lambda': 1}
    best_para = find_parameter(other_params, cv_params)
    learning_rate=best_para['learning_rate']

    #紧接着就是：reg_alpha以及reg_lambda
    cv_params = {'reg_alpha': [0, 0.001, 0.005, 0.01, 0.05,0.1,1,2,3], 'reg_lambda': [0, 0.001, 0.005, 0.01, 0.05,0.1,1,2,3]}
    other_params = {'learning_rate': learning_rate, 'n_estimators': n_estimators, 'max_depth': max_depth, 'min_child_weight':min_child_weight, 'seed': 0,
                    'subsample': subsample, 'colsample_bytree': colsample_bytree, 'gamma': gamma, 'reg_alpha': 0, 'reg_lambda': 1}
    best_para = find_parameter(other_params, cv_params)
    reg_alpha,reg_lambda=best_para['reg_alpha'],best_para['reg_lambda']


    params = {'learning_rate': learning_rate, 'n_estimators': n_estimators, 'max_depth': max_depth, \
              'min_child_weight':min_child_weight, 'seed': 0,'subsample': subsample, \
              'colsample_bytree': colsample_bytree, 'gamma': gamma, 'reg_alpha': reg_alpha, \
              'reg_lambda': reg_lambda,'silent':1, 'objective':'multi:softmax','num_class':n_class}

    model = xgb.XGBClassifier(**params)
    model.fit(X_train, y_train)
    train_predictions=model.predict(X_train)
    train_accuracy = accuracy_score(y_train, train_predictions)
    print('train_accuracy',train_accuracy)
    test_predictions=model.predict(X_test)
    test_accuracy = accuracy_score(y_test, test_predictions)
    print('test_accuracy',test_accuracy)

    #保存模型
   # pickle.dump(model, open(r'D:\M\trainCode\Myxgboost\model_f_%d.pickle.dat'%(n_features), 'wb'))
    #读取模型
    #loaded_model = pickle.load(open(r'D:\M\trainCode\Myxgboost\model_f_%d.pickle.dat'%(n_features), 'wb'))

    statistical_result = [[0] * n_class for i in range(n_class)]
    for i in range(y_test.shape[0]):
        statistical_result[int(y_test[i])][int(test_predictions[i])] += 1
    print('_______________')
    print(statistical_result)
    print('_______________')
    #保存混淆矩阵
    # pkl_path = r'D:\M\trainCode\result\xg_f_%d.pkl' % (n_features)
    # with open(pkl_path, 'wb') as f:
    #     pickle.dump(statistical_result, f)


if __name__=='__main__':
   xgTrain()