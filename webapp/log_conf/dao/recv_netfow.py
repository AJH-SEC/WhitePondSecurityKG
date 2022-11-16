from util.recv_log import ReadLogDataByKafka
from util.util import trans_time_zone
from datasource.packetbeat_data import PacketBeatData
from interface.deal_log_interface import DealLogInterface


import logging
import json
import uuid


class RecvNet(DealLogInterface):
    def set_config(self, config_file_name):
        '''
        param config_file_name: 配置文件名称, str
        '''
        self.config_instance.set_config(config_file_name)

    # 处理网络包数据
    def recv_net_packet_by_kafka(self):
        config_kafka_list = []
        if self.config_instance.get_net_config()["recv_type"] == "kafka":
            config_kafka_list = self.config_instance.get_net_config()["kafka"]
        
        for kafka_value in config_kafka_list:
            ReadLogDataByKafka(kafka_value["host"], kafka_value["port"], kafka_value["topic"]).read_from_consumer_to_deal(self.deal_packetbeat_by_kafka)

    # 接受kafka队列数据进行处理
    def deal_packetbeat_by_kafka(self, msg, topic_name):
        '''
        param msg: 输入的日志数据, dict
        '''
        json_data = json.loads(msg)
        packet_beat_data = PacketBeatData(self.config_file_name)
        list_type = packet_beat_data.get_type_list()
        if json_data["type"] in list_type:
            self.deal_packetbeat_currency(json_data, packet_beat_data)
        
        return
    
    # 通用packetbeat处理函数
    def deal_packetbeat_currency(self, json_data, packet_beat_data):
        '''
        param json_data: json类型的字典数据
        param packet_beat_data: packetbeat的配置实例
        '''
        get_template_data = packet_beat_data.get_template_flow_data(json_data["type"])
        logging.debug(get_template_data["name"])
        data = get_template_data["data"]
        uuid_val = str(uuid.uuid4())
        node_name =  uuid_val

        if "if_node_attribute" in data.keys():
            # TODO:遍历属性，多级key使用 双下划线 __ 连接如 agent__id
            key_value_map = {}
            for net_node_temp in data["if_node_attribute"]:
                feild_name = net_node_temp["filed"]
                if feild_name in json_data.keys():
                    if type(net_node_temp["son_filed"]) == type(""):
                        if net_node_temp["son_filed"] == "__all":
                            if type(json_data[feild_name]) == type(dict()):
                                for key_son, value in json_data[feild_name].items():
                                    key_son = feild_name + "__" +key_son
                                    if type(value) == type(dict()) or type(value) == type([]):
                                        key_value_map.update(self.recursion_map_value(value, key_son))
                                    else:
                                        key_value_map[key_son] = value
                            elif type(json_data[feild_name]) == type([]):
                                key_value_map[feild_name] = ",".join([i for i in json_data[feild_name]])
                            elif type(json_data[feild_name]) == type(''):
                                key_value_map[feild_name] = json_data[feild_name]

                    elif type(net_node_temp["son_filed"]) == type([]):
                        for attr_value in net_node_temp["son_filed"]:
                            if attr_value in json_data[feild_name]:                                
                                key_son = feild_name + "__" +attr_value
                                key_value_map.update(self.recursion_map_value(value, key_son))  
                    
            key_value_map = self.add_name_attr(key_value_map["agent__type"], key_value_map)
            key_value_map["log_id"] = node_name
            # 转换时间时区
            key_value_map["event__start"] = trans_time_zone(key_value_map["event__start"])
            key_value_map["event__end"] = trans_time_zone(key_value_map["event__end"])

            self.neo4j_db.add_node(key_value_map, data["if_node_labels"])
            self.neo4j_db.add_log_rule_relation(data['if_node_labels'], key_value_map)

        if "if_node" in data.keys():
            for node_val_temp in data["if_node"]:
                attr_node = {}
                node_name_assert = "net_assert"
                node_val_filed = node_val_temp["filed"]
                if node_val_filed in json_data.keys():
                    for key in node_val_temp["value"]:
                        if key in json_data[node_val_temp["filed"]].keys():
                            if key == "ip":
                                node_name_assert = json_data[node_val_temp["filed"]][key]
                            # print(type(json_data[node_val_temp["filed"]]))
                            attr_node[str(node_val_filed) + "__" + str(key)]= json_data[node_val_temp["filed"]][key]
                attr_node = self.add_attr_num(attr_node)
                attr_node = self.add_name_attr(node_name_assert, attr_node)
                if self.neo4j_db.match_node_num_by(attr_node, node_val_temp["labels"]) == 0:
                    self.neo4j_db.add_node(attr_node, node_val_temp["labels"])
        
        if "if_node_relationship" in data.keys():
            for mach_val in data["if_node_relationship"]["filed_match"]:
                map_value = {}
                for key_val in mach_val["attr"]:
                    if key_val in json_data[mach_val["filed"]].keys():
                        map_value[str(mach_val["filed"]) + "__" + str(key_val)] = json_data[mach_val["filed"]][key_val]
                if mach_val["is_num"]:
                    map_value = self.add_attr_num(map_value)
                if mach_val["dircertion"] == "left":
                    dest_map = {"log_id": node_name}
                    self.neo4j_db.add_relationship(mach_val["source_node_labels"], map_value, mach_val["dest_node_labels"], dest_map,mach_val["rs_label"], map_value)
                elif mach_val["dircertion"] == "right":
                    source_map = {"log_id": node_name}
                    self.neo4j_db.add_relationship(mach_val["source_node_labels"], source_map, mach_val["dest_node_labels"], map_value,mach_val["rs_label"], map_value)
        return
    def add_name_attr(self, name, map_value):
        '''
        param name: 节点name的值
        param map_value: 属性map
        '''
        if "name" not in map_value.keys():
            map_value["name"] = name
        return map_value

    def add_attr_num(self, map_value):
        '''
        param name: 节点name的值
        param map_value: 属性map
        '''
        if "attr_num" not in map_value.keys():
            map_value["attr_num"] = len(map_value)
        return map_value

    def recursion_map_value(self, map_value, pre_key):
        '''
        des : 递归字典转换为一维度字典
        param msg: 输入的日志数据, dict
        '''
        key_value_map = {}
        if type(map_value) == type(dict()):
            for key, value in map_value.items():
                key = pre_key + "__" + key
                if type(value) == type(dict()) or type(value) == type([]):
                    dat_emp = self.recursion_map_value(value, key)
                    key_value_map.update(dat_emp)
                else:
                    key_value_map[key] = value
        elif type(map_value) == type([]):
            i = 0
            str_list = []
            for list_val in map_value:
                key_l = pre_key + "__list__" + str(i)
                if type(list_val) == type(dict()) or type(list_val) == type([]):                        
                    dat_emp = self.recursion_map_value(list_val, key_l)
                    key_value_map.update(dat_emp)
                elif type(list_val) != type(""):
                    key_value_map[key_l] = list_val
                else:
                    str_list.append(list_val)
                i += 1
            if len(str_list) > 0:
                key_value_map[pre_key] = str_list

        return key_value_map


    # def recursion_map_value(self, map_value, pre_key):
    #     '''
    #     des : 递归字典转换为一维度字典
    #     param msg: 输入的日志数据, dict
    #     '''
    #     key_value_map = {}
    #     for key, value in map_value.items():
    #         key = pre_key + "__" + key
    #         if type(value) == type(dict()):
    #             dat_emp = self.recursion_map_value(value, key)
    #             key_value_map.update(dat_emp)
    #         elif type(value) == type([]):
    #             i = 0
    #             str_list = []
    #             for list_val in value:
    #                 key_l = key + "__list__" + str(i)
    #                 if type(list_val) == type(dict()) or type(list_val) == type([]):                        
    #                     dat_emp = self.recursion_map_value(list_val, key_l)
    #                     key_value_map.update(dat_emp)
    #                 elif type(list_val) != type(""):
    #                     key_value_map[key_l] = list_val
    #                 else:
    #                     str_list.append(list_val)
    #                 i += 1
    #             if len(str_list) > 0:
    #                 key_value_map[key] = str_list
    #         else:
    #             key_value_map[key] = value
    #     return key_value_map    
    
    

