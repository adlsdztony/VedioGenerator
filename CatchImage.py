import requests
from PIL import Image
from bs4 import BeautifulSoup
from random import randint
import os
import shutil
from urllib.parse import quote

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
           }
gif = 'gif'
jpg = 'jpg'


def get_ima(img_url, file_name):
    r = requests.get(img_url, headers=headers, stream=True)
    with open(file_name, 'wb') as f:
        f.write(r.content)


def ima_modify(file):
    img = Image.open(file)
    h = img.height
    return 500/h


def get_url(url):
    url_list = []
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text)
    soup1 = soup.find(name='div', attrs={"class": "ui segment imghover"})
    for a in soup1.find_all('a', href=True):
        img = a.find('img')
        url = img['data-original']
        url_list.append(url)
    return url_list


def get_url_from_baidu(key_word):
    url_list = []
    baidu = 'https://image.baidu.com/search/index?tn=baiduimage&word='
    url = baidu + quote(key_word)
    print(url)
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text)
    print(soup.text)
    soup1 = soup.find(name='div', attrs={"class": "imgpage"})
    print(soup1)
    for a in soup1.find_all('a', href=True):
        img = a.find('img')
        url = img['data-imgurl']
        url_list.append(url)
    return url_list


def random_download_ima(num):
    n = 0
    state = 5

    path = './image'
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)
    else:
        shutil.rmtree(path)
        os.mkdir(path)

    while n < num:
        if state == 5:
            while True:
                img_list = get_url(f'https://www.fabiaoqing.com/biaoqing/lists/page/{randint(1, 201)}.html')
                if not img_list == []:
                    break
            state = 0
        ran = randint(0, len(img_list) - 1)
        get_ima(img_list[ran].replace('bmiddle', 'large'), f'./image/{n}.{gif if gif in img_list[ran] else jpg}')
        n += 1
        state += 1


def download_particular_ima(num):
    img_list = get_url(f'https://www.fabiaoqing.com/biaoqing/lists/page/{randint(1, 201)}.html')
    ran = randint(0, len(img_list) - 1)
    get_ima(img_list[ran].replace('bmiddle', 'large'), f'./image/{num}.{gif if gif in img_list[ran] else jpg}')


def download_ima(num):
    random_download_ima(num)
    while True:
        print(f'已在image目录下生成随机图片，共计{num}张，如要替换请按顺序更改文件名')
        a = input('键入1重新生成单张图片，键入2重新生成所有图片，其他任意键继续：')
        if a == '1':
            while True:
                ima_num = input('输入数字重新生成图片，输入exit退出：')
                if ima_num == 'exit':
                    break
                elif int(ima_num) > num:
                    print('请输入范围内数字')
                else:
                    path = r'./image'
                    img_list = os.listdir(path)
                    for i in img_list:
                        if i == num+'.jpg' or i == num+'.gif':
                            os.remove('./image/' + i)
                    ima_num = int(ima_num)
                    download_particular_ima(ima_num)
        elif a == '2':
            random_download_ima(num)
        else:
            break


if __name__ == '__main__':
    get_url_from_baidu('鲨鱼')
