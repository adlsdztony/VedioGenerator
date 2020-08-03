from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.fx.loop import loop
from CatchImage import ima_modify, download_ima, random_download_ima
from SubtitleModify import Subtitle
from datetime import datetime
from random import randint
import os
import re


def tryint(s):
    try:
        return int(s)
    except ValueError:
        return s


def str2int(v_str):
    return [tryint(sub_str) for sub_str in re.split('([0-9]+)', v_str)]


def sort_humanly(v_list):
    return sorted(v_list, key=str2int)


def VedioGenerator(audio_path, sub_path, bgm_path='random', sub_size=35, sub_color='white', fps=24, auto=0):
    sub = Subtitle(sub_path)  # 导入字幕
    sub.subtitle_modify()

    if bgm_path == 'random':
        bgm_folder = r'./bgm'
        bgm_list = os.listdir(bgm_folder)
        bgm_list = ['./bgm/' + i for i in bgm_list]
        bgm_num = randint(0, len(bgm_list)-1)
        bgm_path = bgm_list[bgm_num]

    if auto == 0:
        a = input('输入skip跳过下载图片：')
        if a != 'skip':
            print('正在下载图片。。。')
            download_ima(sub.num)  # 启动图片下载流程
    else:
        print('正在下载图片。。。')
        random_download_ima(sub.num)

    # 获取并排序图片路径
    path = r'./image'
    img_list = sort_humanly(os.listdir(path))
    img_list = ['./image/' + i for i in img_list]

    audio = AudioFileClip(audio_path)  # 导入语音
    bgm = AudioFileClip(bgm_path).subclip(t_start=0, t_end=sub.length)  # 导入BGM
    background_clip = ColorClip(size=(1280, 720), color=[0, 0, 0]).set_audio(
        CompositeAudioClip([bgm, audio])).set_duration(sub.length)  # 创建背景
    generator = lambda txt: TextClip(txt, font='SimHei', fontsize=sub_size, color=sub_color)
    subtitle = SubtitlesClip(sub_path, generator).set_position(('center', 'bottom'))  # 导入字幕

    clips = [background_clip, subtitle]

    # 导入所有图片
    for i, time in enumerate(sub.time_list):
        ima = img_list[i]
        if 'gif' in ima:
            clip1 = (VideoFileClip(ima)
                     .fx(loop)
                     .set_position('center')
                     .set_duration(sub.length_list[i])
                     .resize(ima_modify(ima))
                     .set_start(time)
                     )
            clips.append(clip1)
        else:
            clip1 = (ImageClip(ima)
                     .set_position('center')
                     .set_duration(sub.length_list[i])
                     .resize(ima_modify(ima))
                     .set_start(time)
                     )
            clips.append(clip1)

    video = CompositeVideoClip(clips)

    save_path = f'./Vedio'
    folder = os.path.exists(save_path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(save_path)
    video_path = f"./Vedio/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp4"
    video.write_videofile(video_path, codec="libx264", fps=fps)
    return video_path


if __name__ == '__main__':
    Audio = input('audio:')
    subtitles = input('sub:')
    BGM = input('bgm:')
    VedioGenerator(Audio, subtitles, bgm_path=BGM)
