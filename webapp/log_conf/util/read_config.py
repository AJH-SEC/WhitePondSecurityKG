import json
import os

class ConfigInstance:
    _instance = None

    def __init__(self) -> None:
        self.config_file_name = "../config.json"

    # 单例模式
    def __new__(cls, *args, **kwargs):
            if not cls._instance:
                cls._instance = object.__new__(cls)
            return cls._instance

    # 设置配置文件路径
    def set_config(self, file_name) -> dict:
        '''
        param file_name: 配置文件名称， 
        '''
        self.config_file_name = file_name
        self.config_value = self._init_config_instance(file_name)
        return self.config_value

    # 获取net的网络流量获取配置
    def get_net_config(self):
        return self.config_value["net"]

    # 获取安全日志获取配置
    def get_network_security_equipment_config(self):
        return self.config_value["network_security_equipment"]
    
    # 获取防火墙安全日志配置
    def get_fw_config(self):
        return self.config_value["network_security_equipment"]["fw"]

    # 获取入侵防御安全日志配置
    def get_ips_config(self):
        return self.config_value["network_security_equipment"]["ips"]

    # 获取web应用防火墙安全日志配置
    def get_waf_config(self):
        return self.config_value["network_security_equipment"]["waf"]

    # 获取apt web安全日志配置
    def get_apt_web_config(self):
        return self.config_value["network_security_equipment"]["apt_web"]
    
    # 获取apt 网络安全日志配置
    def get_apt_net_config(self):
        return self.config_value["network_security_equipment"]["apt_net"]

    # 获取apt 邮件安全日志配置
    def get_apt_mail_config(self):
        return self.config_value["network_security_equipment"]["apt_mail"]

    # 获取蜜罐安全日志配置
    def get_honey_config(self):
        return self.config_value["network_security_equipment"]["honey"]

    # 获取其他类型安全日志配置
    def get_other_config(self):
        return self.config_value["network_security_equipment"]["other"]

    # 获取其他类型安全日志配置
    def get_wazuh_alert_config(self):
        return self.config_value["wazuh_alert"]

    # 获取beat日志配置
    def get_beat_normal_config(self):
        return self.config_value["nomal_log"]

    # 获取图数据库neo4j地址，用户，密码配置
    def get_neo4j_config(self):
        return self.config_value["neo4j_profile"]

    # 获取日志记录级别
    def get_log_level_config(self) -> int:
        return self.config_value["log_level"]

    @staticmethod
    def _init_config_instance(file_name):
        if os.path.splitext(file_name)[-1] == ".json":
            if os.path.isfile(file_name):
                with open(file_name) as f:
                    return json.load(f)
                
            

   