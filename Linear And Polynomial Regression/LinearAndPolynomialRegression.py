import numpy as np
import pandas as pd
import copy
import warnings
from pandas.core.common import SettingWithCopyWarning
warnings.filterwarnings(action = 'ignore',category = SettingWithCopyWarning)

def multivariate_linear_regression(dataframe):

    x_numpy = np.asmatrix(dataframe.loc[:99][['x1', 'x2', 'x3', 'x4', 'x5', 'x6']])
    y_numpy = np.asmatrix(dataframe.loc[:99][['Y']])

    Q = np.linalg.pinv(x_numpy) * y_numpy

    print("Q:")
    print(Q)

    dataframe.loc[100:, 'Y'].update(
        dataframe['x1'] * Q.item(0)
        + dataframe['x2'] * Q.item(1)
        + dataframe['x3'] * Q.item(2)
        + dataframe['x4'] * Q.item(3)
        + dataframe['x5'] * Q.item(4)
        + dataframe['x6'] * Q.item(5))


def polynomial_regression(df):

    dataframe = copy.deepcopy(df)

    dataframe.loc[:99, 'x1'].update(dataframe['x1'] ** 6)
    dataframe.loc[:99, 'x2'].update(dataframe['x2'] ** 5)
    dataframe.loc[:99, 'x3'].update(dataframe['x3'] ** 4)
    dataframe.loc[:99, 'x4'].update(dataframe['x4'] ** 3)
    dataframe.loc[:99, 'x5'].update(dataframe['x5'] ** 2)
    dataframe.loc[:99, 'x6'].update(dataframe['x6'])

    x_numpy = np.asmatrix(dataframe.loc[:99][['x1', 'x2', 'x3', 'x4', 'x5', 'x6']])
    y_numpy = np.asmatrix(dataframe.loc[:99][['Y']])

    Q = np.linalg.pinv(x_numpy) * y_numpy

    print("Q:")
    print(Q)

    df.loc[100:, 'Y'].update(
          dataframe['x1'] * Q.item(0)
        + dataframe['x2'] * Q.item(1)
        + dataframe['x3'] * Q.item(2)
        + dataframe['x4'] * Q.item(3)
        + dataframe['x5'] * Q.item(4)
        + dataframe['x6'] * Q.item(5))


def run_linear_regression():
    data_frame = pd.read_csv('dataset.csv', sep=',')
    print(data_frame)
    multivariate_linear_regression(data_frame)
    print('RESULT for linear regression:')
    print(data_frame)
    data_frame.to_csv('updated dataset linear regression.csv', sep=',')

def run_polynomial_regression():
    data_frame = pd.read_csv('dataset.csv', sep=',')
    print(data_frame)
    polynomial_regression(data_frame)
    print('RESULT for polynomial regression:')
    print(data_frame)
    data_frame.to_csv('updated dataset polynomial regression.csv', sep=',')


if __name__== "__main__":
    run_linear_regression()
    run_polynomial_regression()