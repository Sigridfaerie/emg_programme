# #_*_coding:utf-8_*_
"""
# @Author : Sigrid
# env python3.8
# @time   : 8/3/23 8:09 PM
"""
import csv
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from keras.models import Sequential
from keras.layers import LSTM, GRU, Dense
from keras.callbacks import EarlyStopping
from dataloader import dataloader
from parameters import new_data_folder, model_save_path

# 读取数据
datas, labels = dataloader(new_data_folder)

# Convert labels to numerical values
label_mapping = {label: index for index, label in enumerate(set(labels))}
labels = [label_mapping[label] for label in labels]

# 存放标签对应关系
df = pd.DataFrame(label_mapping.items(), columns=['Label', 'BinaryResult'])
df.to_csv('label_mapping.csv', index=False)
# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(datas, labels, test_size=0.2, random_state=42)
# Reshape data to fit LSTM model
X_train = np.array(X_train).reshape(len(X_train), -1, X_train[0].shape[1])
X_test = np.array(X_test).reshape(len(X_test), -1, X_test[0].shape[1])

# Normalize data
X_train = X_train / np.max(X_train)
X_test = X_test / np.max(X_test)

y_train = np.array(y_train)
y_test = np.array(y_test)

# Build LSTM model
model = Sequential()
model.add(LSTM(128, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dense(len(label_mapping), activation='softmax'))

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# train
model.fit(X_train, y_train, epochs=10, batch_size=16, validation_data=(X_test, y_test))

# save model
model.save(model_save_path)


#评估
score, accuracy = model.evaluate(X_test, y_test, batch_size=16)
print('Test score:', score)
print('Test accuracy:', accuracy)




