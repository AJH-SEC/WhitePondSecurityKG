# -*-coding:utf-8-*-
import datetime
import json
from django.conf import settings
from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher, Subgraph

from webapp.const import LABEL_LIST

graph = Graph(settings.NEO4J_URL, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))
# graph = Graph("neo4j://localhost:7687", auth=('neo4j', '123456'))

def information_show(iDisplayStart: int, iDisplayLength: int):
    """
    情报信息展示 展示组织和软件
    @param iDisplayStart: 分页开始数
    @param iDisplayLength: 分页数据长度
    @return:
    """

    query_start = f"""MATCH (g:`Groups`)-[]->(t)<-[]-(r)<-[rel:`log_hit_rule`]-(log)
                      WHERE NONE(label_1 IN LABELS(log) WHERE label_1 IN {LABEL_LIST})
                      MATCH (g)-[:uses]->(tech)
                      WHERE ANY(label_t IN LABELS(tech) WHERE label_t IN ['SubTechniques', 'Techniques'])
                      MATCH (g)-[:uses]->(s:Software)
                      MATCH (tt)<-[]-(rr)<-[rel:`log_hit_rule`]-()
                    """
    query_num = f"""RETURN COUNT(DISTINCT g.name) AS num"""
    query_end = f"""RETURN DISTINCT g.name AS group, COLLECT(DISTINCT s.name) AS software,
                    COLLECT(DISTINCT tt.name) AS hit_techniques,
                    COLLECT(DISTINCT tech.name) AS group_techniques,
                    COUNT(DISTINCT tech.name) AS group_techniques_num, 
                    COUNT(DISTINCT tt.name) AS hit_techniques_num
                    SKIP {iDisplayStart} LIMIT {iDisplayLength}"""

    query_info = query_start + query_end
    query_number = query_start + query_num
    info = graph.run(query_info).data()
    info_num = graph.run(query_number).data()[0]
    number = info_num['num']
    info_list = []
    for text in info:
        every_info = {}
        every_info.update({'group': text['group']})
        every_info.update({'software': ",".join(text['software'])})
        every_info.update({'hit_techniques': ",".join(text['hit_techniques'])})
        every_info.update({'group_techniques': ",".join(text['group_techniques'])})
        every_info.update({'group_all_techniques_number': text['group_techniques_num']})               # 此组织下的所有技术
        every_info.update({'group_hit_techniques_number': text['hit_techniques_num']})                 # 此组织目前命中技术
        every_info.update({'hit_percentage': str(text['hit_techniques_num']) + '/' + str(text['group_techniques_num'])})
        info_list.append(every_info)
    return info_list, number

def information_search(node_properties: dict, iDisplayStart: int, iDisplayLength: int):
    """
    情报信息条件查询
    @param node_properties: 查询节点属性
    @param iDisplayStart: 分页开始数
    @param iDisplayLength: 分页数据长度
    @return:
    """

    query_start = f"""MATCH (g:`Groups` {'{name:"' + list(node_properties.values())[0] +'"}'})-[]->(t)<-[]-(r)<-[rel:`log_hit_rule`]-(log)
                      WHERE NONE(label_1 IN LABELS(log) WHERE label_1 IN {LABEL_LIST})
                      MATCH (g)-[:uses]->(tech)
                      WHERE ANY(label_t IN LABELS(tech) WHERE label_t IN ['SubTechniques', 'Techniques'])
                      MATCH (g)-[:uses]->(s:Software)
                      MATCH (tt)<-[]-(rr)<-[rel:`log_hit_rule`]-()
                    """
    query_num = f"""RETURN COUNT(DISTINCT g.name) AS num"""
    query_end = f"""RETURN DISTINCT g.name AS group, COLLECT(DISTINCT s.name) AS software,
                    COLLECT(DISTINCT tt.name) AS hit_techniques,
                    COLLECT(DISTINCT tech.name) AS group_techniques,
                    COUNT(DISTINCT tech.name) AS group_techniques_num, 
                    COUNT(DISTINCT tt.name) AS hit_techniques_num
                    SKIP {iDisplayStart} LIMIT {iDisplayLength}"""

    query_info = query_start + query_end
    query_number = query_start + query_num
    info = graph.run(query_info).data()
    info_num = graph.run(query_number).data()[0]
    number = info_num['num']
    info_list = []
    for text in info:
        every_info = {}
        every_info.update({'group': text['group']})
        every_info.update({'software': ",".join(text['software'])})
        every_info.update({'hit_techniques': ",".join(text['hit_techniques'])})
        every_info.update({'group_techniques': ",".join(text['group_techniques'])})
        every_info.update({'group_all_techniques_number': text['group_techniques_num']})               # 此组织下的所有技术
        every_info.update({'group_hit_techniques_number': text['hit_techniques_num']})                # 此组织目前命中技术
        every_info.update({'hit_percentage': str(text['hit_techniques_num']) +'/'  + str(text['group_techniques_num'])})
        info_list.append(every_info)
    return info_list, number


if __name__ == '__main__':
    print(information_show(0, 15))
    # information_search({'name': 'HEXANE'}, 0, 15)






