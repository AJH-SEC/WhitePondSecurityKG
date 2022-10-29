import os
import re
from util.read_config import ConfigInstance
from util.read_yaml import read_yaml_file
from interface.get_template_data_interface import GetTemplateDataInterface


# 安全日志枚举字典数据
class SecurityEquipmentData(GetTemplateDataInterface):
    
    # type_dict = {"flow": r"E:\MselfProject\Neo4j_GDS\log\templates\packetbeat\netflow.yaml",
    # "http": r"E:\MselfProject\Neo4j_GDS\log\templates\packetbeat\http.yaml",
    # "tls": r"E:\MselfProject\Neo4j_GDS\log\templates\packetbeat\tls.yaml",
    # "icmp": r"E:\MselfProject\Neo4j_GDS\log\templates\packetbeat\icmp.yaml",
    # "dns": r"E:\MselfProject\Neo4j_GDS\log\templates\packetbeat\dns.yaml",
    # }
    work_dir = os.path.dirname("__file__")
    dir = os.path.abspath(os.path.join(work_dir, os.path.pardir))
    config_file = os.path.abspath(os.path.join(dir, r'templates\packetbeat'))

    type_dict = {}
    for (dirpath, dirname, filenames) in os.walk(config_file):
        for file in filenames:
            file_str = file.split('.')[0]
            if file_str == 'netflow':
                file_str = 'flow'
            type_dict.update({file_str: os.path.join(dirpath, file)})

    def get_type_list(self):
        return self.type_dict.keys()
    
    def get_template_flow_file_path(self):
        work_dir = os.path.dirname("__file__")
        dir = os.path.abspath(os.path.join(work_dir, os.path.pardir))
        config_file = os.path.abspath(os.path.join(dir, r'templates\packetbeat\netflow.yaml'))
        return config_file
        # return r"E:\MselfProject\Neo4j_GDS\log\templates\packetbeat\netflow.yaml"

    def get_template_flow_data(self, type_val):
        '''
        param type_val: 日志的类型
        '''
        return read_yaml_file(self.get_type_dict()[type_val])

    def get_type_dict(self):
        # TODO:该处将需要优化为数据库存储
        
        return self.type_dict

# 安全日志与att&ck矩阵映射字典
class SecurityAlertMapToAttck:
    apt_web_log_map_tec = {'05008': 'T1190',
                   '01001': 'T1020',
                   '03001': 'T1190',
                   '02002': 'T1205',
                   '09006': 'T1567',
                   '02003': 'T1608',
                   '02001': 'T1505',
                   '02001': 'T1505.003',
                   '06003': 'T1592',
                   '09009': 'T1080',
                   '09009': 'T1528',
                   '05006': 'T1552',
                   '05010': 'T1190',
                   '09002': 'T1082',
                   '09007': 'T1592',
                   '09001': 'T1189',
                   '06007': 'T1189',
                   '01002': 'T1595',
                   '03003': 'T1190',
                   }
    
    apt_net_log_map_tec = {'104637': 'T1595',
                   '105602': 'T1189',
                   '104627': 'T1567',
                   '105080': 'T1082',
                   }
    
    apt_mail_log_map_tec = {'文本': 'T1598.001',
                   '邮件': 'T1598.001',
                   '网址': 'T1598.003',
                   '附件': 'T1598.002'}

    honey_log_map_tec = {'PROBE': 'T1595'}

    def set_apt_web_log_map_tec(self, key, value):
        '''
        param key: 设置的键值
        param value: 设置的值
        '''
        self.apt_web_log_map_tec[key]= value
    
    def get_apt_web_log_map_tec(self):
        return self.apt_web_log_map_tec

    def set_apt_net_log_map_tec(self, key, value):
        '''
        param key: 设置的键值
        param value: 设置的值
        '''
        self.apt_net_log_map_tec[key]= value
    
    def get_apt_net_log_map_tec(self):
        return self.apt_net_log_map_tec

    def set_apt_mail_log_map_tec(self, key, value):
        '''
        param key: 设置的键值
        param value: 设置的值
        '''
        self.apt_mail_log_map_tec[key]= value
    
    def get_apt_mail_log_map_tec(self):
        return self.apt_mail_log_map_tec
    
    def set_honey_log_map_tec(self, key, value):
        '''
        param key: 设置的键值
        param value: 设置的值
        '''
        self.honey_log_map_tec[key]= value
    
    def get_honey_log_map_tec(self):
        return self.honey_log_map_tec

