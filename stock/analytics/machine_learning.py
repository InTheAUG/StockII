import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, plot_confusion_matrix
from xgboost import XGBRFClassifier, XGBRegressor


def machine_learning(df, target):
    df.fillna(method='linear', inplace=True)

    targ = df.pop(target)
    x_train, x_test, y_train, y_test = train_test_split(df, targ)

    model = XGBRFClassifier(max_depth=4, n_estimators=512)
    model.fit(x_train, y_train)

    pred = model.predict(y_test)

    f1 = f1_score(y_test, pred)
    acc = accuracy_score(y_test, pred)

    plot_confusion_matrix(model, x_test, y_test, show=False)

    return model

