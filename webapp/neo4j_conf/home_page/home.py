import pandas as pd
from django.conf import settings
from py2neo import Graph

from webapp.const import LABEL_LIST

graph = Graph(settings.NEO4J_URL, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))


def node_count(start_time: str, end_time: str):
    """
    统计某个时间段log节点数量
    @param start_time: 开始时间
    @param end_time: 结束时间
    @return:
    """

    query_count = f"""MATCH (n) WHERE NONE(l in LABELS(n) WHERE l IN {LABEL_LIST}) 
                        AND '{start_time}' <= n.event__start <= '{end_time}' RETURN COUNT(n) AS count"""
    info_number = graph.run(query_count).data()
    # print(info_number[0]['count'])
    return info_number[0]['count']


def show_node_property_value(node_label: str, node_property: str):
    """
    展示节点具体的某个属性值
    @param node_label: 节点名
    @param node_property: 节点属性名
    @return:
    """
    query = f"""MATCH (n:{node_label}) RETURN DISTINCT(n.{node_property}) AS {node_property}"""
    node_info = graph.run(query).data()
    properties_list = []
    for text in node_info:
        if text[node_property] == None:
            pass
        else:
            properties_list.append(text[node_property])
    return pd.Series(properties_list).drop_duplicates().tolist()


def show_hit_branch(node_label: str, node_property: str):
    """
    命中规则在战术中的分布雷达图占比数据
    @param node_label: 节点名
    @param node_property: 节点属性名
    @return:
    """
    properties_list = show_node_property_value(node_label, node_property)
    info_list = []
    for property in properties_list:
        query = f"""MATCH p=(log)-[r:`log_hit_rule`]->(rule)-[]-(n:Techniques) where n.tactics='{property}' 
        return COUNT(n) AS count"""
        node_info = graph.run(query).data()
        if node_info:
            for text in node_info:
                info_list.append(text['count'])
        else:
            info_list.append(0)
    sum_tactic = sum(info_list)
    proportion_list = []
    for info in info_list:
        if sum_tactic:
            p = (info * 100) // sum_tactic
        else:
            p = 0
        proportion_list.append(p)
    return proportion_list, properties_list

