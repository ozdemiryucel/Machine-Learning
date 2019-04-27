# Yucel Ozdemir
# 220201009

import colorize as colorize
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plot
from matplotlib import offsetbox
from sklearn.decomposition import PCA
from sklearn.manifold import MDS
from sklearn.manifold import Isomap
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import LocallyLinearEmbedding as LLE
import sklearn
from sklearn import datasets
from sklearn import manifold
import scipy.io
import math
from mpl_toolkits.mplot3d import Axes3D





def draw(reduction_method):
    if reduction_method == "PCA":
        method = PCA(n_components=3)
    elif reduction_method == "LLE":
        method = LLE(n_components=3, n_neighbors=5, eigen_solver="auto")
    elif reduction_method == "Isomap":
        method = Isomap(n_components=3, n_neighbors=5, eigen_solver="auto")
    elif reduction_method == "MDS":
        method = MDS(n_components=3)

    print()
    print(reduction_method + ' is being plotted')

    fitted_method = method.fit_transform(x)
    data_frame_of_method = pd.DataFrame(data=fitted_method
                               , columns=['component 1', 'component 2', 'component 3'])

    # print(principalDf.head())
    #
    # print(data_frame[['SKC']].head())

    print(int(time.time() - start), 'seconds')

    finalDf = pd.concat([data_frame_of_method, data_frame[['SKC']]], axis=1)
    # print('========================')
    # print(finalDf.head())
    # print('========================')

    fig = plot.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X', fontsize=14)
    ax.set_ylabel('Y', fontsize=14)
    ax.set_zlabel('Z', fontsize=14)
    ax.set_title('3 Components ' + reduction_method, fontsize=20)

    targets = ['BKN', 'SCT', 'CLR', 'OVC']
    colors = ['r', 'g', 'b', 'k']
    for target, color in zip(targets, colors):
        indices_to_keep = finalDf['SKC'] == target
        ax.scatter(finalDf.loc[indices_to_keep, 'component 1']
                   , finalDf.loc[indices_to_keep, 'component 2']
                   , finalDf.loc[indices_to_keep, 'component 3']
                   , c=color
                   , s=1)
    ax.legend(targets)
    ax.grid
    plot.show()

    # if reduction_method == "MDS":
    #     print("hey")
    #     f = open('mds4.txt', 'w') ##############################################
    #     print(fitted_method.tolist())
    #     for i in fitted_method.tolist():
    #         f.write(str(i[0])+ "," + str(i[1]) + "," + str(i[2]))
    #         f.write("\n")
    #     #f.write(fitted_method.tolist())
    #     f.close()


if __name__ == "__main__":

    file_name = '53727641925dat.txt'
    file = open(file_name, 'r')

    line_array = []
    a = 0
    for line in file:
        # if a%4==3: ################################################################
        line_array.append(line.replace('\n', '').split(' '))
        # a+=1
    file.close()
    line_array.remove(line_array[0])

    for line in line_array:
        line[:] = (value for value in line if value != '')  # Removes spaces in lines

    for line in line_array:  # kilcikli line lari kaldiriyor
        if len(line) != 33:
            line_array.remove(line)

    for line in line_array:
        for i in line:
            if '0.00T' in i:
                line_array.remove(line)

        # if line[-2] == '0.00T':
        # line_array.remove(line)

    print('yucel')

    # for i in line_array:
    #     print(i)

    print(len(line_array), 'duzgun item var')

    k = [0, 1, 2, 5, 12, 13, 14, 15, 16, 17, 18, 19, 20, 24, 26, 27, 28, 29, 30, 31, 32]

    for line in line_array:
        for i in reversed(k):
            line.pop(i)

    # print('basladi')

    average_array = []
    for i in range(12):
        sum = 0
        counter = 0
        if i==3:
            average_array.append('CLR')
            continue
        for line in line_array:
            if '*' not in line[i]:
                sum += float(line[i])
            counter += 1
        average_array.append(sum/counter)

    print("merhaba")
    print(average_array)

    for line in line_array:
        for i in line:
            if '*' in str(i):
                # print(i)
                if line.index(i) == 3:
                    line_array.remove(line)
                    break
                line[line.index(i)] = average_array[line.index(i)]

    for line in line_array:
        for i in line:
            if '*' in str(i):
                # print(i)
                if line.index(i) == 3:
                    line_array.remove(line)
                    break
                line[line.index(i)] = average_array[line.index(i)]


    # print('bitti')

    f = open('data.txt', 'w')
    f.write('DIR SPD CLG SKC L M H  VSB TEMP DEWP SLP STP')
    f.write('\n')
    for line in line_array:
        for element in line:
            f.write(str(element) + ' ')
        f.write('\n')
    f.close()

    data_frame = pd.read_csv('data.txt', sep='\s+')

    features = ['DIR', 'SPD', 'CLG', 'L', 'M', 'H', 'VSB', 'TEMP', 'DEWP', 'SLP', 'STP']

    start = time.time()
    print('@@@@@@@@@@@@@@@@')
    print(data_frame)
    print('@@@@@@@@@@@@@@@@')
    x = data_frame.loc[:, features].values
    y = data_frame.loc[:, ['SKC']].values

    x = StandardScaler().fit_transform(x)
    print('Standardize')
    print(pd.DataFrame(data=x, columns=features).head())

    methods = ['PCA', 'LLE', 'Isomap', 'MDS']

    for method in methods:
        draw(method)
