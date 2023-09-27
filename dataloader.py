# _*_coding:utf-8_*_
"""
# @Author : Sigrid
# env python3.8
# @time   : 8/14/23 6:12 PM
"""
import os
import numpy as np
import csv
import pandas as pd
def dataloader(path):
    """
    处理训练数据用于输入模型

    Args:
        path (str): 数据集所在路径，本程序中就是处理后的数据 即 newdata文件夹下的数据

    Returns:
        X (list): 数据列表，由多个二维数组组成，每个二维数组代表一个数据样本
        Y (list): 标签列表，每个元素代表一个数据样本的标签，每个标签为对应文件夹的名字
    """
    Y = [] #label
    X = [] #data
    subdirectories = []
    for entry in os.scandir(path):
        if entry.is_dir():
            subdirectories.append(entry.name)
    print(subdirectories)
    for label in subdirectories:
        for filename in os.listdir(os.path.join(path, label)):
            if not filename.endswith('.csv'):
                continue
            with open(os.path.join(path, label, filename), 'r') as file:
                # 读取数据
                data = pd.read_csv(file)
                # 数据预处理
                # 去除无用特征
                data = data.drop(['Vbat', 'Trigger', 'fs', 'N'], axis=1)
                values = data.values.astype('float32')
                X.append(values)
                Y.append(label)


    return X, Y


