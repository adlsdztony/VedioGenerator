import requests
from datetime import datetime
from bs4 import BeautifulSoup
from time import sleep
import os
import sys
import io

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

log_url = 'http://www.subspeak.top/login'

log_data = {'username': '19521402539',
            'password': 'Asd123456',
            'csrfmiddlewaretoken': 'yxBdLGb0BK1cF402rfegaQflvbyR4kC1MWXfYHkOHBQIV5jPaZa7pKXdT9n6Zfsi'}

cookie = r'_ga=GA1.2.361004398.1594190656; _gid=GA1.2.160725165.1595655607; sessionid=1djvjvit7i067z0vkznv13tetidnd7nt; ' \
         'Hm_lvt_d1e6e48975f87599d83668e0c8263e4a=1595407935,1595655607,1595687632,1595738037; ' \
         'Hm_lpvt_d1e6e48975f87599d83668e0c8263e4a=1595739259'

# data = {
#     'text': '',
#     'speaker': '13',
#     'volume': '100',
#     'pitchr': '0',
#     'speed': '40',
#     'subtitle': '1',
#     'srtnum': '0',
#     'trans': '0',
#     'fh_break': '0',
#     'wav_type': '3',
#     'csrfmiddlewaretoken': 'ohT38gOPaCwhvU4BV7NZNxA1ypovL39ka9rxvV0UE03xmIiEwIOl6wv6cUBDP5zW'
# }

data = {"global": "#[停顿:1000]#",
        "text": "",
        "version": "v1",
        "ali_speaker": 13,
        "speaker_id": 13,
        "volume": 100,
        "rate": 0,
        "speed": 40,
        "config": {"is_srt": "1",
                   "srt_pt": 0,
                   "is_trans": "0",
                   "trans_model": "1",
                   "trans_to": "en",
                   "breaks": 0,
                   "wav_model": "1"}}
url = 'http://www.subspeak.top/api/v2/submit'
submit_headers = {'Accept': '*/*',
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'zh-CN,zh;q=0.9',
                  'Connection': 'keep-alive',
                  'Content-Length': '411',
                  'Content-Type': 'application/json',
                  'Cookie': '_ga=GA1.2.361004398.1594190656; sessionid=n2zwungqv2lyky9dnthn5ifp9o86hhht; _gid=GA1.2.338241176.1596346618; Hm_lvt_d1e6e48975f87599d83668e0c8263e4a=1595810354,1595815597,1596346516,1596364400; Hm_lpvt_d1e6e48975f87599d83668e0c8263e4a=1596365416',
                  'Host': 'www.subspeak.top',
                  'Origin': 'http://www.subspeak.top',
                  'Referer': 'http://www.subspeak.top/speaker/submit',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
                  'X-Requested-With': 'XMLHttpRequest'}

download_url = 'http://www.subspeak.top/speaker/download?task_id=85113&type=1'
download_url_sub = 'http://www.subspeak.top/speaker/download?task_id=85113&type=2'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
}

download_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': "_ga=GA1.2.361004398.1594190656; sessionid=n2zwungqv2lyky9dnthn5ifp9o86hhht; Hm_lvt_d1e6e48975f87599d83668e0c8263e4a=1595764340,1595810354,1595815597,1596346516; Hm_lpvt_d1e6e48975f87599d83668e0c8263e4a=1596346618; _gid=GA1.2.338241176.1596346618; _gat_gtag_UA_123157281_2=1",
    'Host': 'www.subspeak.top',
    'Referer': 'http://www.subspeak.top/speaker/tasks',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
}

params = {
    'task_id': '85284',
    'type': '1'
}

tasks_url = 'http://www.subspeak.top/speaker/tasks'


class Subspeak:
    def __init__(self):
        self.session = None
        self.ID = None

    def log_in(self):
        self.session = requests.Session()
        self.session.post(log_url, log_data)

    def submit_data(self, text):
        data['text'] = text
        response = self.session.post(url, data, headers=submit_headers)
        return response

    def download_audio(self, ID):
        params['task_id'] = ID
        params['type'] = '1'
        download_url.replace('85113', ID)
        response = self.session.get(download_url, headers=download_headers, params=params)
        save_path = f'./Audio'
        folder = os.path.exists(save_path)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(save_path)
        file_name = f"./Audio/audio{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp3"
        with open(file_name, 'wb') as f:
            f.write(response.content)
        return file_name

    def download_subtitle(self, ID):
        params['task_id'] = ID
        params['type'] = '2'
        download_url_sub.replace('85113', ID)
        response = self.session.get(download_url, headers=download_headers, params=params)
        save_path = f'./Subtitle'
        folder = os.path.exists(save_path)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(save_path)
        file_name = f"./Subtitle/subtitle{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.srt"
        with open(file_name, 'wb') as f:
            f.write(response.content)
        return file_name

    def find_ID(self):
        response = self.session.get(tasks_url, headers=headers)
        soup = BeautifulSoup(response.text)
        soup1 = soup.find('div', attrs={"class": "clearfix"})
        ID = soup1.find('span').text
        self.ID = ID[3:8]

    def check_state(self):
        response = self.session.get(tasks_url, headers=headers)
        soup = BeautifulSoup(response.text)
        soup1 = soup.find('div', attrs={"class": "clearfix"})
        ID = soup1.find('span').text
        if len(ID) == 8:
            return False
        else:
            return True

    def close(self):
        self.session.close()

    def get_file(self, text):
        self.log_in()
        self.submit_data(text)
        sleep(1)
        self.find_ID()
        print('提交完成正在等待生成')
        while True:
            sleep(10)
            if self.check_state():
                audio = self.download_audio(self.ID)
                subtitle = self.download_subtitle(self.ID)
                self.close()
                print('音频文件下载完成')
                break
            else:
                print('正在等待生成')
        return audio, subtitle


if __name__ == '__main__':
    Sub = Subspeak()
    Sub.log_in()
    Sub.submit_data('requests库用着真的很方便，使用Session对象还能保持长连接就更美了。不过在使用过程中发现脚本走完后底层的TCP端口没有断开连接要等一会才释放，心里不爽。')
    sleep(1)
    Sub.find_ID()
    print('提交完成正在等待生成')
    while True:
        sleep(10)
        if Sub.check_state():
            Sub.download_audio(Sub.ID)
            Sub.download_subtitle(Sub.ID)
            break
        else:
            print('正在等待生成')
