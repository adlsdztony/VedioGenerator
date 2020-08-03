import os
from random import randint


bgm_folder = r'./bgm'
bgm_list = os.listdir(bgm_folder)
bgm_list = ['./bgm/' + i for i in bgm_list]
print(bgm_list)
print(len(bgm_list))
bgm_num = randint(0, len(bgm_list))
bgm_path = bgm_list[bgm_num]