import numpy as np
from sklearn import linear_model
from sklearn.externals import joblib
from sklearn.metrics import mean_squared_error
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import time
import sys

def predict(filename_test_X, filename_test_y, filename_model, filename_test_y_predict, filename_test_y_predict_proba):
    start = time.time()
    print(start)

    clf = joblib.load(filename_model)

    print(clf.coef_)
    print(clf.intercept_)

    array_X = np.loadtxt(filename_test_X, delimiter=',')
    array_y = np.loadtxt(filename_test_y, delimiter=',')
    array_y_predict_proba = clf.predict_proba(array_X)
    array_y_predict = clf.predict(array_X)

    print(mean_squared_error(array_y, array_y_predict))
    print(classification_report(array_y, array_y_predict))
    print(confusion_matrix(array_y, array_y_predict))#, labels=["0", "1"]))

    np.savetxt(filename_test_y_predict, array_y_predict, delimiter=',', fmt="%.0f")
    np.savetxt(filename_test_y_predict_proba, array_y_predict_proba, delimiter=',')

    end = time.time()
    print(end)

    print('training time :', str(end-start))

def main():
    filename_test_X = sys.argv[1]
    filename_test_y = sys.argv[2]
    filename_model = sys.argv[3]
    filename_test_y_predict = sys.argv[4]
    filename_test_y_predict_proba = sys.argv[5]

    predict(filename_test_X, filename_test_y, filename_model, filename_test_y_predict, filename_test_y_predict_proba)

if __name__ == '__main__':
    main()

