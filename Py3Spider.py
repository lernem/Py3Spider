#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import requests
import codecs
import os
import re
import sys
import io
from bs4 import BeautifulSoup, element

HOME_PAGE_NAME = 'test.html'


def open_page(url):
    r = requests.get(url)
    return BeautifulSoup(r.content, 'lxml') if r.status_code == 200 else None


def get_node_link(node):
    return node.parent['href'] if node.parent is not None else None


def search_node(page_soup, node_name):
    return page_soup.find(text=node_name)


def search_by_path(start_page_soup, search_path):
    page_soup = start_page_soup
    for node_name in search_path:
        node = search_node(page_soup, node_name)
        if node is None:
            return None

        link = get_node_link(node)
        if link is None:
            return None

        page_soup = open_page(link)
        if page_soup is None:
            return None

    return page_soup


def get_login_params():
    cfg_parser = configparser.ConfigParser()
    with codecs.open('login.conf', 'r', encoding='utf-8') as f:
        cfg_parser.read_file(f)

        login_params = {'email': cfg_parser.get('account', 'usr'),
                        'password': cfg_parser.get('account', 'pwd')}

        return login_params


def enum_page(start_page, total_page_cnt):
    page = start_page
    page_idx = 1
    while page is not None:
        print(page_idx, '{:.2%}'.format(page_idx / total_page_cnt))
        next_page_node = search_node(page, '下一页')
        if next_page_node is None:
            return
        next_page_link = get_node_link(next_page_node)
        if next_page_link is None:
            return
        page = open_page(next_page_link)
        if page is None:
            return
        page_idx += 1

        chat_msg_node = page.find(class_='list')
        if chat_msg_node is None:
            return
        for chat_msg in chat_msg_node.children:
            if type(chat_msg) is element.Tag:
                print(chat_msg)


def analyze_relation():
    pass


def get_sender_user_id():
    pass


def get_reply_user_id():
    pass


def group_msg():
    pass


def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/52.0.2743.116 Safari/537.36'
    }
    r = requests.post('http://3g.renren.com/login.do?autoLogin=true', headers=headers, data=get_login_params())
    if r.status_code != 200:
        print(r.status_code)
        return

    gossip_page = search_by_path(BeautifulSoup(r.content, 'lxml'), ['个人主页', '留言板'])

    page_idx_node = gossip_page.find('span')
    total_page_cnt = int(page_idx_node.string[page_idx_node.string.find('/') + 1:page_idx_node.string.find('页')])

    enum_page(gossip_page, total_page_cnt)


if __name__ == '__main__':
    main()
