#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GLaDOS 自动签到脚本 - glados.cloud
"""

import os
import sys
import requests
import json
from datetime import datetime

def checkin():
    """GLaDOS 签到函数"""
    # 从环境变量中获取 Cookie
    cookies_str = os.environ.get('GLADOS_COOKIE', '')
    
    if not cookies_str:
        print('✗ 错误: 未找到 GLADOS_COOKIE 环境变量')
        sys.exit(1)
    
    # 支持多账号，使用 & 分隔
    cookie_list = cookies_str.split('&')
    
    # GLaDOS API 地址
    checkin_url = 'https://glados.cloud/api/user/checkin'
    status_url = 'https://glados.cloud/api/user/status'
    
    # 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://glados.cloud/console/checkin',
        'Origin': 'https://glados.cloud',
        'Content-Type': 'application/json;charset=UTF-8'
    }
    
    # 签到成功计数
    success_count = 0
    total_count = len(cookie_list)
    
    print(f'\n====== GLaDOS 自动签到 ======')
    print(f'时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'账号数量: {total_count}\n')
    
    for index, cookie in enumerate(cookie_list, 1):
        cookie = cookie.strip()
        if not cookie:
            continue
            
        print(f'[{index}/{total_count}] 处理账号 {index}...')
        
        try:
            # 设置 Cookie
            headers['Cookie'] = cookie
            
            # 发起签到请求
            payload = {'token': 'glados.one'}
            checkin_response = requests.post(
                checkin_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if checkin_response.status_code != 200:
                print(f'  ✗ 签到请求失败: HTTP {checkin_response.status_code}')
                continue
            
            checkin_data = checkin_response.json()
            message = checkin_data.get('message', '未知')
            
            # 获取账号状态
            status_response = requests.get(
                status_url,
                headers=headers,
                timeout=30
            )
            
            if status_response.status_code == 200:
                status_data = status_response.json()
                data = status_data.get('data', {})
                email = data.get('email', '未知')
                left_days = data.get('leftDays', '0')
                
                # 只取整数部分
                try:
                    left_days = int(float(left_days))
                except:
                    pass
                
                print(f'  ✓ 邮箱: {email}')
                print(f'  ✓ 签到结果: {message}')
                print(f'  ✓ 剩余天数: {left_days} 天\n')
                
                success_count += 1
            else:
                print(f'  ✓ 签到结果: {message}')
                print(f'  ⚠ 获取状态失败\n')
                
        except requests.exceptions.Timeout:
            print(f'  ✗ 请求超时\n')
        except requests.exceptions.RequestException as e:
            print(f'  ✗ 请求失败: {str(e)}\n')
        except Exception as e:
            print(f'  ✗ 错误: {str(e)}\n')
    
    print(f'====== 签到完成 ======')
    print(f'成功: {success_count}/{total_count}')
    
    # 如果所有账号都失败，返回错误状态
    if success_count == 0:
        sys.exit(1)

if __name__ == '__main__':
    checkin()
