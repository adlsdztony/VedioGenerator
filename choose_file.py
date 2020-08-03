import tkinter as tk
from tkinter import filedialog
from VedioGenerator import VedioGenerator

'''打开选择文件夹对话框'''
root = tk.Tk()
root.withdraw()
print('选择语音音频')
audio = filedialog.askopenfilename()
print('选择字幕文件')
sub = filedialog.askopenfilename()
print('选择背景音乐')
bgm = filedialog.askopenfilename()
input('任意键继续')


VedioGenerator(audio, sub, bgm_path=bgm)
