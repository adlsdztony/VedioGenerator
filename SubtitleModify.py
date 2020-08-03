# -*- coding:utf-8 -*-
import datetime
import math
import os.path
import re


#提取时间戳，
def time_stamp2time(x):
    time_list = [str(i) for i in x.split(' --> ')]
    time_list1_1 = [x for x in time_list[0].split(':')]
    time_list1_2 = [int(x) for x in time_list1_1[2].split(',')]
    time_list1_1.pop()

    time_list2_1 = [x for x in time_list[1].split(':')]
    time_list2_2 = [int(x) for x in time_list2_1[2].split(',')]
    time_list2_1.pop()

    t1 = [int(time_list1_1[0]), int(time_list1_1[1]), (time_list1_2[0]+time_list1_2[1]/1000)]
    t2 = [int(time_list2_1[0]), int(time_list2_1[1]), (time_list2_2[0]+time_list2_2[1]/1000)]
    return t1, t2


#加上指定的时间
def modifying_time(time, s):
    time[2] = time[2]+s
    if time[2] >= 60:
        time[1] = time[1]+int(time[2]//60)
        time[2] = time[2] % 60
        if time[1] >= 60:
            time[0] = time[0]+int(time[1]//60)
            time[1] = time[1] % 60
    return time


#返回时间戳
def time2time_stamp(x):
    x.append(round((x[2]-math.floor(x[2])), 3))
    x[2] = math.floor(x[2])
    H = str(x[0]).zfill(2)
    M = str(x[1]).zfill(2)
    S = str(x[2]).zfill(2)
    MS = str(int(x[3]*1000)).zfill(3)
    time_stamp = H+':'+M+':'+S+','+MS
    return time_stamp


def time_difference(t1, t2):
    if t1[2] > t2[2]:
        t2[2] += 60
    t1 = int(t1[2]*1000)
    t2 = int(t2[2]*1000)
    return t2 - t1


def get_length_list(file_name):
    with open(file_name, encoding='UTF-8') as f:
        length_list = []
        for line in f:
            if re.match(r'\d{1,2}:\d{1,2}:\d{1,2},\d{1,3} --> \d{1,2}:\d{1,2}:\d{1,2},\d{3}', line):
                line = line.strip()
                time_stamp1 = line
                t1, t2 = time_stamp2time(time_stamp1)
                length = time_difference(t1, t2)
                length_list.append(length)
    return length_list


def get_time(file_name):
    with open(file_name, encoding='UTF-8') as f:
        time_list = []
        for line in f:
            if re.match(r'\d{1,2}:\d{1,2}:\d{1,2},\d{1,3} --> \d{1,2}:\d{1,2}:\d{1,2},\d{3}', line):
                line = line.strip()
                time_stamp1 = line
                t1, t2 = time_stamp2time(time_stamp1)
                time = [t1[0]*3600 + t1[1]*60 + t1[2], t2[0]*3600 + t2[1]*60 + t2[2]]
                time_list.append(time)
    return time_list


def move_back(file_path, second):
    starttime = datetime.datetime.now()

    # 打开字幕文件
    with open(file_path, 'r') as f1:
        path, name = os.path.split(file_path)
        f2 = open(os.path.join(path, 'Temporary.srt'), 'a')
        for line in f1:
            if re.match(r'\d{1,2}:\d{1,2}:\d{1,2},\d{1,3} --> \d{1,2}:\d{1,2}:\d{1,2},\d{3}', line):
                line = line.strip()
                time_stamp1 = line

                t1, t2 = time_stamp2time(time_stamp1)

                t1 = modifying_time(t1, second)
                t2 = modifying_time(t2, second)

                time_stamp_1 = time2time_stamp(t1)
                time_stamp_2 = time2time_stamp(t2)
                time_stamp2 = time_stamp_1 + ' --> ' + time_stamp_2 + '\n'
                line = time_stamp2
            f2.write(line)
        f2.close()
    # 写入完毕后删除原文件
    os.remove(name)
    os.rename('Temporary.srt', name)
    endtime = datetime.datetime.now()
    print('转换耗时：', endtime - starttime)


modify = {'中国': 'ZG', '美国': 'MG', '印度': 'YD', '英国': 'YG'}


class Subtitle:
    def __init__(self, file):
        self.file = file
        self.file_path, self.name = os.path.split(file)
        self.length_list = [i/1000 for i in get_length_list(file)]
        time_list = get_time(file)
        self.length = time_list[-1][-1]
        self.time_list = [i[0] for i in time_list]
        self.num = len(time_list)

    def subtitle_modify(self):
        with open(self.file, 'r', encoding='UTF-8') as f:
            txt = f.read()
        for key in modify:
            txt.replace(key, modify[key])
        with open(self.file, 'w', encoding='UTF-8') as f:
            f.write(txt)


if __name__ == '__main__':
    sub = Subtitle('test.srt')
    print(sub.time_list)
    print(sub.length_list)
    print(sub.length)
