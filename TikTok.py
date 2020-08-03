import requests
from datetime import datetime
from bs4 import BeautifulSoup
from time import sleep
import os

log_url = 'https://sso.douyin.com/account_login/v2/'

log_data = {'account': '2e3d33343c30373431353730363c',
            'password': '447661343736313033',
            'service': 'https://creator.douyin.com/?logintype=user&loginapp=douyin&jump=https://creator.douyin.com/',
            'aid': '2906',
            'mix_mode': '1',
            'is_vcd': '1',
            'fp': 'kdct8qdh_g3AdYIbA_TWQb_4cuF_Berv_p1kuHD6LURuS',
            'ttwid': '6853399145694643716'}
