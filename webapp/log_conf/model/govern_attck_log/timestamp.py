# -*- coding: UTF-8 -*-
import uuid
import random
import time,datetime

def random_str():
    shijian=str(time.time())#时间戳
    print(shijian)
    # uln = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    # rs = random.sample(uln, num)  # 生成一个 指定位数的随机字符串
    a = uuid.uuid4()  # 根据 时间戳生成 uuid , 保证全球唯一
    b = ''.join(str(a).split("-"))  # 生成将随机字符串 与 uuid拼接
    b='A'+b+shijian
    return b  # 返回随机字符串


# b = random_str()
# print(b)
# print(len(b))
