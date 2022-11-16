from interface.deal_log_interface import DealLogInterface
from util.recv_log import ReadLogDataByKafka
from model.govern_attck_log.wazuhrlog import Wazhur_Log
from model.govern_attck_log.Normallog import Common_Log
from datasource.enum import NormalBeatsDealEnum
from util.util import trans_time_zone

from platform import node
from numpy import source
import datetime
import logging
import threading
import json
import uuid


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
            msg_dict = json.loads(msg)
            start_time = datetime.datetime.now()
            print("-------------------------start time:{}".format(datetime.datetime.now()))
            # 老版本日志命中规则处理
            # self.normal_deal.Nercreate(msg, self.config_instance.get_beat_normal_config()["rule_dir"])
            
            # 新版本处理日志
            key_value_map = {}
            for key, val in msg_dict.items():
                if "@" in key:
                    key = key.replace("@", "")
                key_value_map.update(self.recursion_map_value(val, key))

            labels = [key_value_map["metadata__beat"], NormalBeatsDealEnum.NORMAL_LOG.value]
            key_value_map[NormalBeatsDealEnum.LOG_ID.value] = key_value_map["metadata__beat"] + str(uuid.uuid4().hex)
            key_value_map["name"] = key_value_map["metadata__beat"]
            
            # 修改时间字段  将时间调整为东八时区
            key_value_map["event__start"] = trans_time_zone(key_value_map["timestamp"])
            if "event__end" in key_value_map.keys():
                key_value_map["event__end"] = trans_time_zone(key_value_map["event__end"])
            
            if "process__created" in key_value_map.keys():
                key_value_map["process__created"] = trans_time_zone(key_value_map["process__created"])
            
            self.neo4j_db.add_node(key_value_map, labels)
            self.neo4j_db.add_log_rule_relation(labels, key_value_map)
            print("-------------------------start_time : {} ,------------------stop time:{}".format(start_time, datetime.datetime.now()))


        except Exception as e:
            print("load beats failed, massage:{}, err: {}\n".format(msg, e))
        
        logging.debug("topic name is : {} , data: {}".format(topic_name, msg))


    def recursion_map_value(self, map_value, pre_key):
        '''
        des : 递归字典转换为一维度字典
        param msg: 输入的日志数据, dict
        '''
        key_value_map = {}
        if type(map_value) == dict:
            for key, value in map_value.items():
                key = pre_key + "__" + key
                if type(value) == type(dict()):
                    dat_emp =self.recursion_map_value(value, key)
                    key_value_map.update(dat_emp)
                elif type(value) == type([]):
                    key_value_map[key] = ",".join([i for i in value])
                else:
                    key_value_map[key] = value
        else:
            key = {pre_key: map_value}
            key_value_map.update(key)
        return key_value_map