import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

# 读取yaml文件，适配不同的平台
def read_yaml_file(file_name):
    '''
    param file_name: yaml文件名称, str
    '''
    with open(file_name,encoding="utf-8") as f:
        return yaml.safe_load(f)