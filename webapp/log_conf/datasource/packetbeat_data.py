import re
from util.read_config import ConfigInstance
from util.read_yaml import read_yaml_file
from interface.get_template_data_interface import GetTemplateDataInterface
from os import path
import os


class PacketBeatData(GetTemplateDataInterface):
    work_dir = os.path.dirname("__file__")
    # dir = os.path.abspath(os.path.join(work_dir, os.path.pardir))
    config_file = os.path.abspath(os.path.join(work_dir, 'config.json'))

    conf_instance = ConfigInstance()
    conf_instance.set_config(config_file)
    # conf_instance.set_config(r"E:\MselfProject\Neo4j_GDS\log\config.json")
    conf = conf_instance.get_net_config()

    type_dict = {"flow": path.join(conf["templates"], "netflow.yaml"),
                 "http": path.join(conf["templates"], "http.yaml"),
                 "tls": path.join(conf["templates"], "tls.yaml"),
                 "icmp": path.join(conf["templates"], "icmp.yaml"),
                 "dns": path.join(conf["templates"], "dns.yaml"),
                 "nfs": path.join(conf["templates"], "nfs.yaml"),
                 "rpc": path.join(conf["templates"], "rpc.yaml"),
                 "mysql": path.join(conf["templates"], "mysql.yaml"),
                 "amqp": path.join(conf["templates"], "amqp.yaml"),
                 "dhcpv4": path.join(conf["templates"], "dhcpv4.yaml"),
                 "sip": path.join(conf["templates"], "sip.yaml"),
                 "docker": path.join(conf["templates"], "docker.yaml"),
                 "mongodb": path.join(conf["templates"], "mongodb.yaml"),
                 "pgsql": path.join(conf["templates"], "pgsql.yaml"),
                 "redis": path.join(conf["templates"], "redis.yaml"),
                 "jolokia": path.join(conf["templates"], "jolokia.yaml"),
                 "memcache": path.join(conf["templates"], "memcache.yaml"),
                 }
    
    def get_type_list(self):
        return self.type_dict.keys()
    
    def get_template_flow_file_path(self):
        work_dir = os.path.dirname("__file__")
        dir = os.path.abspath(os.path.join(work_dir, os.path.pardir))
        config_file = os.path.abspath(os.path.join(dir, r'templates\packetbeat\netflow.yaml'))
        # print(config_file)
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
