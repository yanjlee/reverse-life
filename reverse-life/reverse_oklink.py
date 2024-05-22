#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/16 22:52
# @Name    : oklink.py
# @Author  : yanlee

import time
import requests
from faker import Faker
import execjs
from loguru import logger

logger.add("debug.log", rotation="1 week")  # 配置日志文件，每周轮换

def get_current_milliseconds():
    """获取当前时间的毫秒值。"""
    return int(time.time() * 1000)

def fetch_richest_bitcoin_addresses(api_key):
    """从OKLink API获取当前最富有的比特币地址列表。"""
    url = f"https://www.oklink.com/api/explorer/v1/btc/richers?offset=0&limit=20&t={get_current_milliseconds()}"
    headers = {
        'accept': 'application/json',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
        'app-type': 'web',
        'referer': 'https://www.oklink.com/zh-hans/btc/rich-list',
        'user-agent': Faker().chrome(),
        'x-apikey': api_key,
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 确保响应状态是200
        return response.json()
    except requests.RequestException as e:
        logger.error(f"获取比特币富豪榜失败: {e}")
        raise

if __name__ == '__main__':
    try:
        # 读取并编译JavaScript代码以获取API密钥
        with open("sign.js", 'r', encoding='utf-8') as file:
            js_code = file.read()
        api_key = execjs.compile(js_code).call("getApiKey")

        # 获取并打印比特币富豪榜
        richest_addresses = fetch_richest_bitcoin_addresses(api_key)
        print(richest_addresses)
    except Exception as e:
        logger.error(f"主程序执行中发生错误: {e}")
