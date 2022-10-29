import re
import urllib3

http_pool = urllib3.PoolManager()

# 获取远程数据字典
def get_data_type_dict(url):
    '''
    param url: 请求地址
    '''
    get_re = http_pool.request("GET",url)
    if get_re.status == 200:
        return get_re.data.decode("utf-8")
    else:
        return False

if __name__ == "__main__":
    get_data_type_dict("https://www.baidu.com")
    