#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import requests
import os
import codecs
import re
import sys
import io
from bs4 import BeautifulSoup

DEBUG = True

HOME_PAGE_NAME = 'test.html'


def search_node(page, text):
    soup = BeautifulSoup(page, 'lxml')
    text_node = soup.find(text=text)
    if text_node is not None and text_node.parent is not None:
        print(text, text_node.parent['href'])
        return text_node.parent
    else:
        print('error: no node {0}'.format(text))
        return None


def search_by_path(start_page, texts):
    page = start_page
    for text in texts:
        node = search_node(page, text)
        if node is not None:
            r = requests.get(node['href'])
            if r.status_code != 200:
                print('error: requests.get status_code={0}'.format(r.status_code))
                return None
            page = r.content
        else:
            return None
    return page


def get_home_page():
    # cfg_parser = configparser.ConfigParser()
    # with codecs.open('login.conf', 'r', encoding='utf-8') as f:
    #     cfg_parser.read_file(f)
    #
    # login_params = {'email': cfg_parser.get('account', 'usr'),
    #                 'password': cfg_parser.get('account', 'pwd')}
    #
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) '
    #                   'Chrome/52.0.2743.116 Safari/537.36'
    # }
    # r = requests.post('http://3g.renren.com/login.do?autoLogin=true', headers=headers, data=login_params)
    # if r.status_code != 200:
    #     print(r.status_code)
    #     return
    #
    # gossip_page = search_by_path(r.content, ['个人主页', '留言板'])
    # gossip_soup = BeautifulSoup(gossip_page, 'lxml')

    gossip_soup = BeautifulSoup(open('gossip.html', 'rb'), 'lxml')
    idx_node = gossip_soup.find(re.compile("AAA.*BBB"))
    if idx_node is not None:
        print(idx_node)
    else:
        print('error')


if __name__ == '__main__':
    if DEBUG or not os.path.exists(HOME_PAGE_NAME):
        get_home_page()
