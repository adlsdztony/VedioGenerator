from pydub import AudioSegment
from pydub.silence import split_on_silence
import sys
import os
import time


def split(name):
    # 载入
    sound = AudioSegment.from_wav(name)
    # sound = sound[:3*60*1000] # 如果文件较大，先取前3分钟测试，根据测试结果，调整参数

    # 设置参数
    silence_thresh = -70  # 小于-70dBFS以下的为静默
    min_silence_len = 700  # 静默超过700毫秒则拆分
    length_limit = 60 * 1000  # 拆分后每段不得超过1分钟
    abandon_chunk_len = 500  # 放弃小于500毫秒的段
    joint_silence_len = 1300  # 段拼接时加入1300毫秒间隔用于断句

    # 将录音文件拆分成适合百度语音识别的大小
    total = prepare_for_baiduaip(name, sound, silence_thresh, min_silence_len, length_limit, abandon_chunk_len,
                                 joint_silence_len)
    return total


def prepare_for_baiduaip(name, sound, silence_thresh=-70, min_silence_len=700, length_limit=60 * 1000,
                         abandon_chunk_len=500, joint_silence_len=1300):
    '''
    将录音文件拆分成适合百度语音识别的大小
    百度目前免费提供1分钟长度的语音识别。
    先按参数拆分录音，拆出来的每一段都小于1分钟。
    然后将，时间过短的相邻段合并，合并后依旧不长于1分钟。

    Args:
        name: 录音文件名
        sound: 录音文件数据
        silence_thresh: 默认-70      # 小于-70dBFS以下的为静默
        min_silence_len: 默认700     # 静默超过700毫秒则拆分
        length_limit: 默认60*1000    # 拆分后每段不得超过1分钟
        abandon_chunk_len: 默认500   # 放弃小于500毫秒的段
        joint_silence_len: 默认1300  # 段拼接时加入1300毫秒间隔用于断句
    Return:
        total：返回拆分个数
    '''

    # 按句子停顿，拆分成长度不大于1分钟录音片段
    print('开始拆分(如果录音较长，请耐心等待)\n', ' *' * 30)
    chunks = chunk_split_length_limit(sound, min_silence_len=min_silence_len, length_limit=length_limit,
                                      silence_thresh=silence_thresh)  # silence time:700ms and silence_dBFS<-70dBFS
    print('拆分结束，返回段数:', len(chunks), '\n', ' *' * 30)

    # 放弃长度小于0.5秒的录音片段
    for i in list(range(len(chunks)))[::-1]:
        if len(chunks[i]) <= abandon_chunk_len:
            chunks.pop(i)
    print('取有效分段：', len(chunks))

    # 时间过短的相邻段合并，单段不超过1分钟
    chunks = chunk_join_length_limit(chunks, joint_silence_len=joint_silence_len, length_limit=length_limit)
    print('合并后段数：', len(chunks))

    # 保存前处理一下路径文件名
    if not os.path.exists('./chunks'): os.mkdir('./chunks')
    namef, namec = os.path.splitext(name)
    namec = namec[1:]

    # 保存所有分段
    total = len(chunks)
    for i in range(total):
        new = chunks[i]
        save_name = '%s_%04d.%s' % (namef, i, namec)
        new.export('./chunks/' + save_name, format=namec)
        # print('%04d'%i,len(new))
    print('保存完毕')

    return total


def chunk_split_length_limit(chunk, min_silence_len=700, length_limit=60 * 1000, silence_thresh=-70):
    '''
    将声音文件按正常语句停顿拆分，并限定单句最长时间，返回结果为列表形式
    Args:
        chunk: 录音文件
        min_silence_len: 拆分语句时，静默满足该长度，则拆分，默认0.7秒。
        length_limit：拆分后单个文件长度不超过该值，默认1分钟。
        silence_thresh：小于-70dBFS以下的为静默
    Return:
        done_chunks：拆分后的列表
    '''
    todo_arr = []  # 待处理
    done_chunks = []  # 处理完
    todo_arr.append([chunk, min_silence_len, silence_thresh])

    while len(todo_arr) > 0:
        # 载入一个音频
        temp_chunk, temp_msl, temp_st = todo_arr.pop(0)
        # 不超长的，算是拆分成功
        if len(temp_chunk) < length_limit:
            done_chunks.append(temp_chunk)
        else:
            # 超长的，准备处理
            # 配置参数
            if temp_msl > 100:  # 优先缩小静默判断时常
                temp_msl -= 100
            elif temp_st < -10:  # 提升认为是静默的分贝数
                temp_st += 10
            else:
                # 提升到极致还是不行的，输出异常
                tempname = 'temp_%d.wav' % int(time.time())
                chunk.export(tempname, format='wav')
                print('万策尽。音长%d,静长%d分贝%d依旧超长,片段已保存至%s' % (len(temp_chunk), temp_msl, temp_st, tempname))
                raise Exception
            # 输出本次执行的拆分，所使用的参数
            msg = '拆分中 音长,剩余[静长,分贝]:%d,%d[%d,%d]' % (len(temp_chunk), len(todo_arr), temp_msl, temp_st)
            print(msg)
            # 拆分
            temp_chunks = split_on_silence(temp_chunk, min_silence_len=temp_msl, silence_thresh=temp_st)
            # 拆分结果处理
            doning_arr = [[c, temp_msl, temp_st] for c in temp_chunks]
            todo_arr = doning_arr + todo_arr

    return done_chunks


def chunk_join_length_limit(chunks, joint_silence_len=1300, length_limit=60 * 1000):
    '''
    将声音文件合并，并限定单句最长时间，返回结果为列表形式
    Args:
        chunk: 录音文件
        joint_silence_len: 合并时文件间隔，默认1.3秒。
        length_limit：合并后单个文件长度不超过该值，默认1分钟。
    Return:
        adjust_chunks：合并后的列表
    '''
    #
    silence = AudioSegment.silent(duration=joint_silence_len)
    adjust_chunks = []
    temp = AudioSegment.empty()
    for chunk in chunks:
        length = len(temp) + len(silence) + len(chunk)  # 预计合并后长度
        if length < length_limit:  # 小于1分钟，可以合并
            temp += silence + chunk
        else:  # 大于1分钟，先将之前的保存，重新开始累加
            adjust_chunks.append(temp)
            temp = chunk
    else:
        adjust_chunks.append(temp)
    return adjust_chunks


if __name__ == '__main__':
    split('v200725-172919.mp3')
