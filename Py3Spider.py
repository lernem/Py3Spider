#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import requests
import codecs
import os
import re
import sys
import io
from bs4 import BeautifulSoup

HOME_PAGE_NAME = 'test.html'


def open_page(url):
    r = requests.get(url)
    return BeautifulSoup(r.content, 'lxml') if r.status_code == 200 else None


def get_node_link(node):
    return node.parent['href'] if node.parent is not None else None


def search_node(page_soup, text):
    return page_soup.find(text=text)


def search_by_path(start_page_soup, texts):
    page_soup = start_page_soup
    for text in texts:
        node = search_node(page_soup, text)
        if node is None:
            return None

        link = get_node_link(node)
        if link is None:
            return None

        page_soup = open_page(link)
        if page_soup is None:
            return None

    return page_soup


def get_home_page():
    cfg_parser = configparser.ConfigParser()
    with codecs.open('login.conf', 'r', encoding='utf-8') as f:
        cfg_parser.read_file(f)
    login_params = {'email': cfg_parser.get('account', 'usr'),
                    'password': cfg_parser.get('account', 'pwd')}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/52.0.2743.116 Safari/537.36'
    }
    r = requests.post('http://3g.renren.com/login.do?autoLogin=true', headers=headers, data=login_params)
    if r.status_code != 200:
        print(r.status_code)
        return

    gossip_page_soup = search_by_path(BeautifulSoup(r.content, 'lxml'), ['个人主页', '留言板'])
    gossip_soup = BeautifulSoup(gossip_page, 'lxml')

    idx_node = gossip_soup.find('span')
    total_page_cnt = int(idx_node.string[idx_node.string.find('/') + 1:idx_node.string.find('页')])

    page_idx = 1
    print(page_idx)
    # next_page_node = search_node(open('gossip.html', 'rb'), '下一页')
    next_page_node = search_node(gossip_page, '下一页')
    if next_page_node is None:
        return

    next_page_link = get_node_link(next_page_node)
    while next_page_link is not None:
        next_page = open_page(next_page_link)
        if next_page is None:
            return

        print(page_idx)
        next_page_link = search_node(r.content, '下一页')
        page_idx += 1


if __name__ == '__main__':
    get_home_page()
