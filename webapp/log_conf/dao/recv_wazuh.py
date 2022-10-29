from ast import arg
import json
from interface.deal_log_interface import DealLogInterface
from util.recv_log import ReadLogDataByKafka
from model.govern_attck_log.wazuhrlog import Wazhur_Log
from model.govern_attck_log.Normallog import Common_Log

from platform import node
from numpy import source
import datetime
import logging
import threading


# 处理wazuh告警日志
class RecvWazuhAlert(DealLogInterface):
    def __init__(self, config_file_name) -> None:
        self.num = 0
        super().__init__(config_file_name)
        self.wazuh_deal = Wazhur_Log(self.config_instance.get_neo4j_config()["host_url"], self.config_instance.get_neo4j_config()["username"], self.config_instance.get_neo4j_config()["password"])

    def set_config(self, config_file_name):
        '''
        param config_file_name: 配置文件名称, str
        '''
        self.config_instance.set_config(config_file_name)

    # 接受日志进行处理
    def recv_wazuh_to_deal(self):
        config_wazuh_kafka_list = []
        if self.config_instance.get_wazuh_alert_config()["recv_type"] == "kafka":
            config_wazuh_kafka_list = self.config_instance.get_wazuh_alert_config()["kafka"]
        
        for kafka_value in config_wazuh_kafka_list:
            ReadLogDataByKafka(kafka_value["host"], kafka_value["port"], kafka_value["topic"]).read_from_consumer_to_deal(self.deal_wazuh_log_by_kafka)

    # 接受kafka队列数据进行处理
    def deal_wazuh_log_by_kafka(self, msg, topic_name):
        '''
        param msg: 输入的日志数据, dict
        param topic_name: kafka主题名称, str
        '''
        try:
            msg = msg.replace(r'\\', '\\').replace(r'\\', '').replace('+', '')
            msg = json.loads(msg)
            data = msg["message"]
            # print('datatype',type(data))
            data = json.loads(data)
            # print(data)
            # self.wazuh_deal.agent_data(data)
            self.wazuh_deal.Nercreate(data)
        except:
            logging.warning("load wazuh alert json data failed, massage:%s", msg)
        
        logging.debug("topic name is : {} , data: {}".format(topic_name, msg))


class RecvNormalLog(DealLogInterface):
    def __init__(self, config_file_name) -> None:
        super().__init__(config_file_name)
        self.normal_deal = Common_Log(self.config_instance.get_neo4j_config()["host_url"], self.config_instance.get_neo4j_config()["username"], self.config_instance.get_neo4j_config()["password"])
        self.config_file_name = config_file_name

    def set_config(self, config_file_name):
        '''
        param config_file_name: 配置文件名称, str
        '''
        self.config_instance.set_config(config_file_name)

    # 接受日志进行处理
    def recv_nomal_log_to_deal(self):
        config_wazuh_kafka_list = []
        
        if self.config_instance.get_beat_normal_config()["recv_type"] == "kafka":
            config_wazuh_kafka_list = self.config_instance.get_beat_normal_config()["kafka"]
        
        for kafka_value in config_wazuh_kafka_list:
            self.deal_one_beat(kafka_value)
    
    def deal_one_beat(self, kafka_value):
        kafka_one = ReadLogDataByKafka(kafka_value["host"], kafka_value["port"], kafka_value["topic"])
        
        thread_kafka = threading.Thread(target=kafka_one.read_from_consumer_to_deal, args=(RecvNormalLog(self.config_file_name).deal_normal_log_by_kafka,))
        thread_kafka.start()

    # 接受kafka队列数据进行处理
    def deal_normal_log_by_kafka(self, msg, topic_name):
        '''
        param msg: 输入的日志数据, dict
        param topic_name: kafka主题名称, str
        '''
        try:
            # msg = msg.replace(r'\\', '\\').replace(r'\\', '').replace('+', '')
            msg = json.loads(msg)
            # self.normal_deal.agent_data(msg)
            start_time = datetime.datetime.now()
            print("-------------------------start time:{}".format(datetime.datetime.now()))
            # self.normal_deal.Nercreate(msg, self.config_instance.get_beat_normal_config()["rule_dir"])
            self.num += 1
            print(self.num)
            print("-------------------------start_time : {} ,------------------stop time:{}".format(start_time, datetime.datetime.now()))
        except Exception as e:
            print("load wazuh alert json data failed, massage:{}, err: {}\n".format(msg, e))
        
        logging.debug("topic name is : {} , data: {}".format(topic_name, msg))