#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/17 01:12
# @Name    : sxfae.py
# @Author  : yanlee

from loguru import logger
from faker import Faker
import requests
import base64
from hashlib import md5
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.PublicKey import RSA

# 配置日志记录器
logger.add("debug.log", rotation="1 week")


def generate_md5_signature(data):
    """为提供的数据生成MD5签名。"""
    return md5(data.encode()).hexdigest()


def zero_pad(data):
    """应用零填充确保数据长度是AES块大小的倍数。"""
    return data + b"\0" * (AES.block_size - len(data) % AES.block_size)


def encrypt_aes(key, iv, text):
    """使用AES加密和CBC模式加密文本。"""
    try:
        padded_text = zero_pad(text.encode('utf-8'))
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
        return base64.b64encode(cipher.encrypt(padded_text)).decode()
    except Exception as e:
        logger.error(f"加密文本失败: {e}")
        raise


def encrypt_rsa(public_key, key):
    """使用RSA公钥加密AES密钥。"""
    try:
        rsa_key = RSA.importKey(public_key)
        cipher = PKCS1_v1_5.new(rsa_key)
        return base64.b64encode(cipher.encrypt(key.encode())).decode()
    except Exception as e:
        logger.error(f"使用RSA加密失败: {e}")
        raise


def generate_headers():
    """生成请求用的HTTP头部，包括动态用户代理。"""
    return {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://jjbl.sxfae.com',
        'Pragma': 'no-cache',
        'Referer': 'https://jjbl.sxfae.com/marketingIndex',
        'User-Agent': Faker().chrome()
    }


def fetch_rsa_public_key(url, headers):
    """给定URL获取RSA公钥。"""
    try:
        response = requests.post(url, headers=headers, json={})
        response.raise_for_status()  # 对4XX或5XX错误抛出异常
        rsa_public_key = response.json()["data"]["publicKey"]
        return rsa_public_key
    except requests.exceptions.RequestException as e:
        logger.error(f"获取RSA公钥失败: {e}")
        raise


def prepare_encrypted_payload(page, rsa_public_key):
    """准备带有签名数据的加密参数进行传输。"""
    try:
        ciphertext = f'{{"page": {page},"size": 10}}'
        md5_signature = generate_md5_signature(ciphertext)

        key = 'XyrWHOmkaZEyRWHu'
        iv = "szazgM3zOYCCHWih"
        encrypted_data = encrypt_aes(key, iv, ciphertext)

        rsa_key = f"key_{key}|iv_{iv}"
        encrypted_rsa_key = encrypt_rsa(rsa_public_key, rsa_key)

        return {
            'sign': md5_signature,
            'data': encrypted_data,
            'rsaKey': encrypted_rsa_key
        }
    except Exception as e:
        logger.error(f"准备加密参数失败: {e}")
        raise


if __name__ == '__main__':
    try:
        headers = generate_headers()
        rsa_public_key = fetch_rsa_public_key('https://jjbl.sxfae.com/sxfaeApi/000002', headers)
        current_page = 1
        json_data = prepare_encrypted_payload(current_page, rsa_public_key)
        response = requests.post('https://jjbl.sxfae.com/sxfaeApi/801014', headers=headers, json=json_data)
        print(response.json())
    except Exception as e:
        logger.error(f"主执行块中发生错误: {e}")
