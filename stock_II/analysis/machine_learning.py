import pandas as pd
import numpy as np
import pickle
from defs import MODELS

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, plot_confusion_matrix
from xgboost import XGBRFClassifier, XGBRegressor


def imputeMissing(df):
    return df.fillna(method="linear")


def machine_learning(df, target):
    frame = df.copy()

    frame.fillna(method='linear', inplace=True)

    targ = frame.pop(target)

    x_train, x_test, y_train, y_test = train_test_split(frame, targ)

    model = XGBRFClassifier(max_depth=5, n_estimators=512)
    model.fit(x_train, y_train)

    pred = model.predict(y_test)

    f1 = f1_score(y_test, pred)
    acc = accuracy_score(y_test, pred)

    plot_confusion_matrix(model, x_test, y_test, show=False)

    return model

