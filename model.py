import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
from sklearn import tree
from sklearn.externals import joblib

def getDisease(test_list):
    data = pd.read_csv('data.csv')
    #print type(data)
    labels = data['disease']
    data = data.drop('disease', axis=1)
    data = np.array(data)
    labels = np.array(labels)
    #print data
    #print labels

    print(labels)

    x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=40)

    clf = svm.SVC(gamma=0.001, C=100)

    #clf = tree.DecisionTreeClassifier()
    clf.fit(x_train, y_train)
    ans = clf.predict(x_test)
    print(classification_report(y_test, ans))

    correct_count = 0
    for i in range(0, len(ans)):
        if ans[i] == y_test[i]:
            correct_count += 1
    print(correct_count)
    print(len(ans))
    print(float(correct_count)/len(ans))


    filename = 'final_model.sav'
    joblib.dump(clf, filename)

    loaded_model = joblib.load(filename)
    result = loaded_model.predict([test_list])
    print(result)
    return result[0]

test_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
print(getDisease(test_list))    
