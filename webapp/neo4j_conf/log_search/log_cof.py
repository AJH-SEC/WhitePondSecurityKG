# -*-coding:utf-8-*-
import json

import pandas as pd
from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher, Subgraph
from django.conf import settings

from webapp.const import LABEL_LIST

graph = Graph(settings.NEO4J_URL, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))
# graph = Graph("neo4j://localhost:7687", auth=('neo4j', '123456'))


def add_property(node_properties: dict, modify_info: dict):
    """
    给日志节点新增operation属性，表明此条属性是否进行处理过
    :param node_properties: 此log节点属性
    :param modify_info: 修改信息 eg:{'operation': 'unhandled/handle/ignore'}
    :return:
    """
    node = NodeMatcher(graph).match().where(**node_properties).first()
    node.update(**modify_info)
    graph.push(node)

    # query = f"MATCH (n) SET n.operation='{node_properties}'"
    # graph.run(query)


def show_node(iDisplayStart, iDisplayLength):
    """
    展示所有日志数据  iDisplayStart, iDisplayLength
    @param iDisplayStart: 分页开始数
    @param iDisplayLength: 分页数据长度
    @return:
    """
    info_list = []
    # label_list = ['SubTechniques', 'Techniques', 'Tactics', 'Citations', 'Datasource',
    #               'DatasourceComponent', 'Software', 'Groups', 'Mitigations', 'Rule', 'NET_ASSERT', 'Campaign']

    info = NodeMatcher(graph).match().where(f"NONE(l in LABELS(_) WHERE l IN {LABEL_LIST})")\
        .order_by('_.event__start DESC').skip(iDisplayStart).limit(iDisplayLength).all()
    total_count = NodeMatcher(graph).match().where(f"NONE(l in LABELS(_) WHERE l IN {LABEL_LIST})").count()
    for text in info:
        info_list.append(dict(text))
    return info_list, total_count


def show_node_property(node_property: str):
    """
    展示节点具体的某个属性值
    @param node_property: 节点属性名【type、event__type】
    @return:
    """
    # label_list = ['SubTechniques', 'Techniques', 'Tactics', 'Citations', 'Datasource',
    #                'DatasourceComponent', 'Software', 'Groups', 'Mitigations', 'Rule', 'Campaign']
    properties_list = []
    query = f"""MATCH (n) WHERE NONE(l in LABELS(n) WHERE l IN {LABEL_LIST}) 
                RETURN DISTINCT(n.{node_property}) AS {node_property}"""
    node_info = graph.run(query).data()
    for text in node_info:
        if text[node_property] == None:
            pass
        else:
            properties_list.append(text[node_property])
    return pd.Series(properties_list).drop_duplicates().tolist()


def search_node(node_property: dict,
                iDisplayStart: int,
                iDisplayLength: int):
    """
    通过条件查询日志数据
    :param node_property: 属性值
    :return:
    """
    log_info = []
    log_number = []
    # label_list = ['SubTechniques', 'Techniques', 'Tactics', 'Citations', 'Datasource',
    #                'DatasourceComponent', 'Software', 'Groups', 'Mitigations', 'Rule']

    query_start = f"""MATCH (n) WHERE NONE(l in LABELS(n) WHERE l IN {LABEL_LIST}) """
    query_end = f"""RETURN PROPERTIES(n) as property SKIP {iDisplayStart} LIMIT {iDisplayLength}"""
    query_end_count = f"""RETURN COUNT(n) AS count"""

    if node_property.get('log_id'):
        name_str = f"""AND n.log_id = "{node_property.get('log_id')}" """
        query_start = query_start + name_str
    if node_property.get('name'):
        name_str = f"""AND n.name = "{node_property.get('name')}" """
        query_start = query_start + name_str
    if node_property.get('type'):
        type_str = f"""AND n.type = "{node_property.get('type')}" """
        query_start = query_start + type_str
    if node_property.get('operation'):
        if node_property.get('operation') == 'unhandled':
            operation_str = f"""AND NOT EXISTS(n.operation) """
        else:
            operation_str = f"""AND n.operation = "{node_property.get('operation')}" """
        query_start = query_start + operation_str
    if node_property.get('event__type'):
        event__type_str = f"""AND n.event__type = {node_property.get('event__type')} """
        query_start = query_start + event__type_str
    if node_property.get('reservationtime'):
        start_time = node_property.get('reservationtime').split(' - ')[0]
        end_time = node_property.get('reservationtime').split(' - ')[1]
        reservationtime_str = f"""AND '{start_time}' <= n.event__start < '{end_time}' """
        query_start = query_start + reservationtime_str

    query = query_start + query_end
    query_count = query_start + query_end_count
    info = graph.run(query).data()
    info_num = graph.run(query_count).data()

    for text in info:
        log_info.append(text['property'])
    for text in info_num:
        log_number.append(text['count'])

    return log_info, sum(log_number)


# if __name__ == '__main__':
#
#     query = "MATCH (n) RETURN DISTINCT LABELS(n) AS LABEL"
#     label_list = ['SubTechniques', 'Techniques', 'Tactics', 'Citations', 'Datasource',
#                    'DatasourceComponent', 'Software', 'Groups', 'Mitigations', 'Rule']
#
#     # info = NodeMatcher(graph).match().where(f"NONE(l in LABELS(_) WHERE l IN {label_list})",
#     #                                         **{'name': 'liu', 'hobby':'play games'}).all()
#     query = f"""MATCH (n) WHERE NONE(l in LABELS(n) WHERE l IN {label_list})
#                AND n.name='liu' AND n.hobby='play games'
#                RETURN PROPERTIES(n) AS property SKIP 0 LIMIT 13"""
#     info = graph.run(query).data()
#     for text in info:
#         print(text['property'])
#
#     query = f"""MATCH (n) WHERE NONE(l in LABELS(n) WHERE l IN {other_label}) AND n.name='liu'
#                  RETURN n"""
#     aa = graph.run(query).data()
#     print(aa)