# _*_coding:utf-8_*_
"""
# @Author : Sigrid
# env python3.8
# @time   : 8/14/23 8:40 PM
"""
from keras import models
import pandas as pd
from dataprocessing import Predata
from parameters import data_folder, feature, new_data_folder, file_size, example_data, example_folder
from dataloader import dataloader
import numpy as np
import os

#使用模型实例
# Load data
# 读取原始csv文件
df = pd.read_csv(example_folder + '/' + example_data, sep=';', skiprows=1)
# 获取所有列名
columns = df.columns

if len(df) <= file_size:
    missing_rows = file_size - len(df)
    missing_data = pd.DataFrame([[0] * len(df.columns)] * missing_rows, columns=df.columns)
    df = pd.concat([df, missing_data])
else:
    # 取中间的filesize行
    num_rows = len(df)
    start_row = num_rows // 2 - file_size // 2
    end_row = num_rows // 2 + file_size // 2
    df = df.iloc[start_row:end_row, :]

# 将时间戳转换为秒数
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df['Timestamp'] = (df['Timestamp'] - df['Timestamp'].min()).dt.total_seconds()
data = df.drop(['Vbat', 'Trigger', 'fs', 'N'], axis=1)
datas = []
values = data.values.astype('float32')
datas.append(values)

X = np.array(datas)


X = np.array(X).reshape(len(X), -1, X[0].shape[1])
X = X / np.max(X)

# Predict using the trained model
model = models.load_model("LSTM_model")
predictions = model.predict(X)
print(predictions)
#Print predictions
max_value = None
max_index = -1
df2 = pd.read_csv('label_mapping.csv')
for i, num in enumerate(predictions[0]):
    if max_value is None or num > max_value:
        max_index = i
        max_value = num
prediction = df2['Label'][max_index]
print('The prediction is: %s'%prediction)