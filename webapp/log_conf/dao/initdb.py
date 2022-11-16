import datetime
import re

from neo4j import GraphDatabase
from neo4j import unit_of_work
from urllib3 import Retry
import logging

from datasource.enum import NormalBeatsDealEnum


class Neo4jDb():
    _instance = None

    def __init__(self, url, username, password):
        self.graph = GraphDatabase.driver(url,auth=(username, password))

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance

    def match_node(self):
        with self.graph.session() as session:
            cypher = "return apoc"
        for node in self.graph.match(r_type="subtechnique_of"):
            logging.debug(node.end_node["name"])

    @unit_of_work(timeout=5)
    def create_node(self, tx, attr_map, labels):
        '''
        param tx: 事务执行实例
        param attr_map: 传入的属性字典
        param labels: 标签列表
        param node_name: 传入的字段名称
        '''
        value = self.generation_node_attr(attr_map)
        return tx.run("CREATE (s:"+labels+ value+") return s").single().value()

    def add_node(self, attr_map, labels):
        '''
        param attr_map: 传入的属性字典
        param labels: 标签列表
        '''
        labels = ":".join([i for i in labels])
        with self.graph.session() as session:
            return session.write_transaction(self.create_node, attr_map, labels)

    def match_node_num_by(self, attr_map, labels):
        '''
        param attr_map: 传入的属性字典
        param labels: 标签列表
        '''
        res_num = 0
        labels = ":".join([i for i in labels])
        value = self.generation_node_attr(attr_map)
        with self.graph.session() as session:
            res = session.run("MATCH (g:"+ labels + value +") return count(g)")
            res_list = res.values()
            if len(res_list) > 0:
                res_num = res_list[0][0]
        return res_num
    
    def generation_node_attr(self, attr_map):
        '''
        param attr_map: 传入的属性字典
        '''
        value = ""

        if type(attr_map) == type(dict()):
            val_list = []
            for k, v in attr_map.items():
                k = str(k).replace("-", "_")
                if type(v) == type([]):
                    val_list.append(k + ":" + str(v) + "")
                elif type(v) == type(""):
                    val_list.append(k + ":'" + str(v).replace("'", '"') + "'")
            value = ",".join([i for i in val_list])
            value = "{"+ value + "}"
        else:
            value = attr_map
        
        return value

    @unit_of_work(timeout=5)
    def crete_relationship(self, tx, source_label, source_map, dest_label, dest_map, relate_label, relate_map):
        '''
        param tx: 事务执行实例
        param source_label
        param source_map
        param dest_label
        param dest_map
        param relate_label
        param relate_map
        '''
        source_map_value = self.generation_node_attr(source_map)
        dest_map_value = self.generation_node_attr(dest_map)
        relate_map_value = self.generation_node_attr(relate_map)
        # data = "MATCH (s:" + source_label + source_map_value + ")" + "MERGE (d:"+ dest_label + dest_map_value +") " + "MERGE (s)-[:"+ relate_label + relate_map_value +"]->(d)"
        # print(data)
        # return tx.run(data)
        return tx.run("MATCH (s:" + source_label + source_map_value + ")"
                        "MERGE (d:"+ dest_label + dest_map_value +") "
                        "MERGE (s)-[:"+ relate_label + relate_map_value +"]->(d)")


    def add_relationship(self, source_labels, source_map, dest_labels, dest_map, relate_label, relate_map):
        '''
        
        '''
        source_labels = ",".join([i for i in source_labels])
        dest_labels = ",".join([i for i in dest_labels])
        with self.graph.session() as session:
            return session.write_transaction(self.crete_relationship, source_labels, source_map, dest_labels, dest_map, relate_label, relate_map)

    def create_log_rule_relation(self, tx, log_labels: str, log_map: dict):
        """
        创建日志规则关系
        @param tx:
        @param log_labels: 日志标签
        @param log_map: 日志信息
        @return:
        """
        log_keys = list(log_map.keys())
        print(log_keys)
        print(self.show_rule_keys())
        for kk in self.show_rule_keys():
            print(kk)
            if kk in log_keys:
                log_info_key = kk
                log_info_value = log_map.get(kk)
                print(log_info_key)
                print(log_info_value)
                query = f"""MATCH (rule:`Rule`) WHERE rule.`log value`='{log_info_value}' AND rule.`log byte` IN {log_keys}
                            MATCH (log:`{log_labels}`) WHERE log.`{log_info_key}`='{log_info_value}'
                            MERGE (log)-[r:`log hit rule`""" + """{create:""" + f""" "{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}" """ + """}]->(rule)"""+f"""
                            
                         """
                return tx.run(query)
            else:
                pass

    # def add_log_rule_relation(self, log_labels, log_map):
    #     labels = ":".join([i for i in log_labels])
    #
    #     with self.graph.session() as session:
    #         return session.write_transaction(self.create_log_rule_relation, labels, log_map)


    def add_log_rule_relation(self, log_labels, log_map):
        log_labels = ":".join([i for i in log_labels])
        log_keys = list(log_map.keys())
        # print(log_keys)
        # print(self.show_rule_keys())
        for kk in self.show_rule_keys():
            # print(kk)
            if kk in log_keys:
                log_info_key = kk
                log_info_value = log_map.get(kk)
                log_id_value= log_map.get(NormalBeatsDealEnum.LOG_ID.value)
                # print(log_info_key)
                # print(log_info_value)
                # TODO :是否为版本问题，修改以id方式进行查询日志
                query = f"""MATCH (rule:Rule) WHERE rule.`log value`='{log_info_value}' AND rule.`log byte`='{log_info_key}'
                            MATCH (log:{log_labels}) WHERE log.`{log_info_key}`='{log_info_value}' AND log.{NormalBeatsDealEnum.LOG_ID.value}='{log_id_value}'
                            MERGE (log)-[r:`log hit rule`""" + """{create:""" + f""" "{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}" """ + """}]->(rule)""" + f"""
                         """
                with self.graph.session() as session:
                    session.run(query)

    def search_rule(self, tx):
        query_rule = ("MATCH (rule:Rule) "
                      "RETURN DISTINCT rule.`log byte` AS rule_key")

        result = tx.run(query_rule)
        # return [row['rule_key'] for row in result]
        return list(map(lambda x: x['rule_key'], result))

    def show_rule_keys(self):
        with self.graph.session() as session:
            result = session.read_transaction(self.search_rule)
            return result


    def test_create_node_by_map(self):
        with self.graph.session() as session:
            return session.write_transaction(self.create_node_test_map)

    def create_node_test_map(self, tx):
        data_map = '1:E+OHBtoW8UyuPYye57NeL18NJxs='

        return tx.run("create (ss:TEST{data: $data_map})", data_map=data_map)

    def close_connection(self):
        self.graph.close()

if __name__ == "__main__":
    # instance = Neo4jDb()
    # instance.test_create_node_by_map()
    neo4j_db = Neo4jDb("neo4j://localhost:7687", username='neo4j', password='123456')
    kk = neo4j_db.show_rule_keys()
    # neo4j_db.close_connection()