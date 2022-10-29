from util.recv_log import ReadLogDataByKafka
from interface.deal_log_interface import DealLogInterface
from model.equipment_data_kg import Create_FireWall_KG, Create_Canister_KG, Create_WafIntercept_KG, Create_Web_KG, Create_Internet_KG, Create_Mail_KG
from datasource.security_equipment_data import SecurityAlertMapToAttck

import json

class RecvSecurityEquipment(DealLogInterface):
    def __init__(self, config_file_name) -> None:
        super().__init__(config_file_name)
        self.security_alert_map_to_attck = SecurityAlertMapToAttck()

    def set_config(self, config_file_name):
        '''
        param config_file_name: 配置文件名称, str
        '''
        self.config_instance.set_config(config_file_name)

    # fw日志信息处理
    def recv_fw_to_deal(self):
        config_kafka_fw_list = []
        fw_conf = self.config_instance.get_fw_config()

        if fw_conf["is_enable"] == False:
            return
        if fw_conf["recv_type"] == "kafka":
            config_kafka_fw_list = fw_conf["kafka"]

        for kafka_value in config_kafka_fw_list:
            ReadLogDataByKafka(kafka_value["host"], kafka_value["port"], kafka_value["topic"]).read_from_consumer_to_deal(self.deal_fw_log_by_kafka)
    
    # ips安全日志处理
    def recv_ips_to_deal(self):
        config_kafka_ips_list = []
        ips_conf = self.config_instance.get_ips_config()

        if ips_conf["is_enable"] == False:
            return
        if ips_conf["recv_type"] == "kafka":
            config_kafka_ips_list = ips_conf["kafka"]

        for kafka_value in config_kafka_ips_list:
            ReadLogDataByKafka(kafka_value["host"], kafka_value["port"], kafka_value["topic"]).read_from_consumer_to_deal(self.deal_ips_log_by_kafka)

    # waf安全日志处理
    def recv_waf_to_deal(self):
        config_kafka_waf_list = []
        waf_conf = self.config_instance.get_waf_config()

        if waf_conf["is_enable"] == False:
            return
        if waf_conf["recv_type"] == "kafka":
            config_kafka_waf_list = waf_conf["kafka"]

        for kafka_value in config_kafka_waf_list:
            ReadLogDataByKafka(kafka_value["host"], kafka_value["port"], kafka_value["topic"]).read_from_consumer_to_deal(self.deal_waf_log_by_kafka)

    # apt web溯源安全日志处理
    def recv_apt_web_to_deal(self):
        config_kafka_apt_list = []
        apt_web_conf = self.config_instance.get_apt_web_config()

        if apt_web_conf["is_enable"] == False:
            return
        if apt_web_conf["recv_type"] == "kafka":
            config_kafka_apt_list = apt_web_conf["kafka"]

        for kafka_value in config_kafka_apt_list:
            ReadLogDataByKafka(kafka_value["host"], kafka_value["port"], kafka_value["topic"]).read_from_consumer_to_deal(self.deal_apt_web_log_by_kafka)

    # apt 网络溯源安全日志处理
    def recv_apt_net_to_deal(self):
        config_kafka_apt_list = []
        apt_net_conf = self.config_instance.get_apt_net_config()

        if apt_net_conf["is_enable"] == False:
            return
        if apt_net_conf["recv_type"] == "kafka":
            config_kafka_apt_list = apt_net_conf["kafka"]

        for kafka_value in config_kafka_apt_list:
            ReadLogDataByKafka(kafka_value["host"], kafka_value["port"], kafka_value["topic"]).read_from_consumer_to_deal(self.deal_apt_net_log_by_kafka)

    # apt 邮件溯源安全日志处理
    def recv_apt_mail_to_deal(self):
        config_kafka_apt_list = []
        apt_mail_conf = self.config_instance.get_apt_mail_config()

        if apt_mail_conf["is_enable"] == False:
            return
        if apt_mail_conf["recv_type"] == "kafka":
            config_kafka_apt_list = apt_mail_conf["kafka"]

        for kafka_value in config_kafka_apt_list:
            ReadLogDataByKafka(kafka_value["host"], kafka_value["port"], kafka_value["topic"]).read_from_consumer_to_deal(self.deal_apt_mail_log_by_kafka)

    # 蜜罐安全日志处理
    def recv_honey_to_deal(self):
        config_kafka_honey_list = []
        honey_conf = self.config_instance.get_honey_config()

        if honey_conf["is_enable"] == False:
            return
        if honey_conf["recv_type"] == "kafka":
            config_kafka_honey_list = honey_conf["kafka"]

        for kafka_value in config_kafka_honey_list:
            ReadLogDataByKafka(kafka_value["host"], kafka_value["port"], kafka_value["topic"]).read_from_consumer_to_deal(self.deal_honey_log_by_kafka)

    def deal_fw_log_by_kafka(self, msg, topic_name):
        '''
        param msg: 输入的日志数据, dict
        param topic_name: 接收到的日志主题名称, str
        '''
        firewall_log = Create_FireWall_KG(self.config_instance.get_neo4j_config()["host_url"], self.config_instance.get_neo4j_config()["username"], self.config_instance.get_neo4j_config()["password"])
        firewall_log.create_FireWall(msg)
        

    def deal_ips_log_by_kafka(self, msg, topic_name):
        '''
        param msg: 输入的日志数据, dict
        param topic_name: 接收到的日志主题名称, str
        '''
        # firewall_log = Create_FireWall_KG(self.config_instance.get_neo4j_config()["host_url"], self.config_instance.get_neo4j_config()["username"], self.config_instance.get_neo4j_config()["password"])
        # firewall_log.create_FireWall(msg)
      

    def deal_waf_log_by_kafka(self, msg, topic_name):
        '''
        param msg: 输入的日志数据, dict
        param topic_name: 接收到的日志主题名称, str
        '''
        waf_log = Create_WafIntercept_KG(self.config_instance.get_neo4j_config()["host_url"], self.config_instance.get_neo4j_config()["username"], self.config_instance.get_neo4j_config()["password"])
        waf_log.create_WafIntercept(msg)
        

    def deal_apt_web_log_by_kafka(self, msg, topic_name):
        '''
        param msg: 输入的日志数据, dict
        param topic_name: 接收到的日志主题名称, str
        '''
        apt_web_log = Create_Web_KG(self.config_instance.get_neo4j_config()["host_url"], self.config_instance.get_neo4j_config()["username"], self.config_instance.get_neo4j_config()["password"])
        apt_web_log.create_Web(msg, self.security_alert_map_to_attck.get_apt_web_log_map_tec())
        
    
    def deal_apt_net_log_by_kafka(self, msg, topic_name):
        '''
        param msg: 输入的日志数据, dict
        param topic_name: 接收到的日志主题名称, str
        '''
        apt_net_log = Create_Internet_KG(self.config_instance.get_neo4j_config()["host_url"], self.config_instance.get_neo4j_config()["username"], self.config_instance.get_neo4j_config()["password"])
        apt_net_log.create_Internet(msg, self.security_alert_map_to_attck.get_apt_net_log_map_tec())
   
    
    def deal_apt_mail_log_by_kafka(self, msg, topic_name):
        '''
        param msg: 输入的日志数据, dict
        param topic_name: 接收到的日志主题名称, str
        '''
        apt_mail_log = Create_Mail_KG(self.config_instance.get_neo4j_config()["host_url"], self.config_instance.get_neo4j_config()["username"], self.config_instance.get_neo4j_config()["password"])
        apt_mail_log.create_Mail(msg, self.security_alert_map_to_attck.get_apt_mail_log_map_tec())
       

    def deal_honey_log_by_kafka(self, msg, topic_name):
        '''
        param msg: 输入的日志数据, dict
        param topic_name: 接收到的日志主题名称, str
        '''
        honey_log = Create_Canister_KG(self.config_instance.get_neo4j_config()["host_url"], self.config_instance.get_neo4j_config()["username"], self.config_instance.get_neo4j_config()["password"])
        honey_log.create_Canister(msg, self.security_alert_map_to_attck.get_honey_log_map_tec())
     
