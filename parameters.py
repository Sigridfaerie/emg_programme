# _*_coding:utf-8_*_
"""
# @Author : Sigrid
# env python3.8
# @time   : 8/13/23 7:11 PM
"""
# 参数定义

# trigger值
Trigger_value = 1
# 特征-----unused
feature = []

# 存放原始数据的文件夹
data_folder = 'data'
# 存放分割好数据的文件夹
new_data_folder = 'newdata'

# 文件大小 采集数据的帧数*一个动作大概的时间s数得到一个估计的数字即可
file_size = 300

# 存放训练好的模型的位置
model_save_path ='LSTM_model'

#测试模型数据
example_folder = 'example'
example_data = 'finger1_left&right_13_24_28.csv'


