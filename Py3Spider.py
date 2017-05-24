# coding=utf-8

import configparser
import requests
import os
import codecs
import re
from bs4 import BeautifulSoup

DEBUG = True

HOME_PAGE_NAME = 'test.html'


def get_home_page():
    cfg_parser = configparser.ConfigParser()
    with codecs.open('login.conf', 'r', encoding='utf-8') as f:
        cfg_parser.read_file(f)

    login_params = {'email': cfg_parser.get('account', 'usr'), 'password': cfg_parser.get('account', 'pwd')}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/52.0.2743.116 Safari/537.36'
    }
    r = requests.post('http://3g.renren.com/login.do?autoLogin=true', headers=headers, data=login_params)

    if r.status_code == 200:
        with open(HOME_PAGE_NAME, 'w') as f:
            f.write(r.text)

    home_page = BeautifulSoup(r.text, 'lxml')
    person_text_node = home_page.find(text='个人主页')
    if person_text_node is None:
        return

    person_page_url = person_text_node.parent['href']
    person_page = requests.get(person_page_url)
    if DEBUG:
        with open('person.html', 'w') as f:
            f.write(person_page.text)


if __name__ == '__main__':
    if 1 or not os.path.exists(HOME_PAGE_NAME):
        get_home_page()
