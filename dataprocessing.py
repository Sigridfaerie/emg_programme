# _*_coding:utf-8_*_
"""
# @Author : Sigrid
# env python3.8
# @time   : 8/13/23 7:11 PM
"""
import os
import pandas as pd
import numpy as np
from parameters import data_folder, feature, new_data_folder, file_size, example_data, example_folder, Trigger_value


class Predata:
    def __init__(self, data_folder):
        self.data_folder = data_folder

    # 修改时间过短动作导致视频无法采集沟100帧问题
    def size_standard_data(self, df):
        """
        对视频数据进行处理，使其长度达到规定大小
        """
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
        return df

    def original_data_split(self, new_data_folder):
        data_folder = self.data_folder
        # 遍历所有动作文件夹
        for action_folder in os.listdir(data_folder):
            # 获取动作文件夹路径
            action_path = os.path.join(data_folder, action_folder)

            # 读取每个csv文件
            for csv_file in os.listdir(action_path):
                csv_file_path = os.path.join(action_path, csv_file)

                # 读取原始csv文件
                df = pd.read_csv(csv_file_path, sep=';', skiprows=1)

                # 获取所有列名
                columns = df.columns
                # 将时间戳转换为秒数
                df['Timestamp'] = pd.to_datetime(df['Timestamp'])
                df['Timestamp'] = (df['Timestamp'] - df['Timestamp'].min()).dt.total_seconds()

                # 获取所有trigger==1的索引位置
                trigger_indexes = df[df['Trigger'] == Trigger_value].index
                trigger_indexes = list(trigger_indexes)
                trigger_indexes = [int(1)] + trigger_indexes + [int(len(df))]
                # 创建新文件夹
                newpath = new_data_folder + '/' + action_folder
                if not os.path.exists(newpath):
                    os.mkdir(newpath)
                else:
                    pass
                # 分离并保存每个动作的数据
                for i in range(1, len(trigger_indexes)):
                    # 获取每个动作的开始和结束位置
                    start = trigger_indexes[i - 1]
                    end = trigger_indexes[i]

                    # 分离动作数据
                    action_data = df[start:end]

                    # 统一数据大小
                    action_data = self.size_standard_data(action_data)

                    # 保存到新文件
                    newpathaction = newpath + '/' + 'action{%s}' % i + csv_file
                    action_data.to_csv(newpathaction, index=False, columns=columns)

    # def example_data_process_to_test(self):
    #
    #     data = pd.read_csv(example_folder+'/'+ example_data, sep=';', skiprows=1)
    #     columns = data.columns
    #     # 将时间戳转换为秒数
    #     data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    #     data['Timestamp'] = (data['Timestamp'] - data['Timestamp'].min()).dt.total_seconds()
    #     values = data.values.astype('float32')
    #     # 获取所有trigger==1的索引位置
    #     trigger_indexes = data[data['Trigger'] == 1].index
    #     trigger_indexes = list(trigger_indexes)
    #     trigger_indexes = [int(1)] + trigger_indexes + [int(len(data))]
    #     # 创建新文件夹
    #     newpath = example_folder + '/' + 'split'
    #     if not os.path.exists(newpath):
    #         os.mkdir(newpath)
    #     else:
    #         pass
    #     # 分离并保存每个动作的数据
    #     for i in range(1, len(trigger_indexes)):
    #         # 获取每个动作的开始和结束位置
    #         start = trigger_indexes[i - 1]
    #         end = trigger_indexes[i]
    #         # 分离动作数据
    #         action_data = data[start:end]
    #         # 统一数据大小
    #         action_data = self.size_standard_data(action_data)
    #         # 保存到新文件
    #         newpathaction = newpath + '/' + 'action{%s}' % i + example_data
    #         action_data.to_csv(newpathaction, index=False, columns=columns)
    #     return newpath


if __name__ == '__main__':
    data = Predata(data_folder)
    data.original_data_split(new_data_folder)
