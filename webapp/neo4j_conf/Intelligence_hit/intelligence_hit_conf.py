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

    query_num = f"""MATCH (rule:`Rule`)<-[rel_2]-(log)
                    WHERE NONE(label_1 IN LABELS(log) WHERE label_1 IN {LABEL_LIST})
                    RETURN COUNT(DISTINCT log) AS count
                 """
    query_groups = f"""MATCH (g)-[rel_0]->(tech)<-[rel_1]-(rule:`Rule`)<-[rel_2:`log hit rule`]-(log)
                       WHERE NONE(label_1 IN LABELS(log) WHERE label_1 IN {LABEL_LIST})
                       AND ANY(label_2 IN LABELS(g) WHERE label_2 IN ['Groups'])
                       RETURN COLLECT(DISTINCT g.name) AS group, log.`name` AS log, 
                              log.event__start AS event__start,
                              log.type AS type, tech.name AS techniques, log.operation AS operation
                       SKIP {iDisplayStart} LIMIT {iDisplayLength}"""

    query_software = f"""MATCH (s)-[rel_0]->(tech)<-[rel_1]-(rule:`Rule`)<-[rel_2:`log hit rule`]-(log)
                         WHERE NONE(label_1 IN LABELS(log) WHERE label_1 IN {LABEL_LIST})
                         AND ANY(label_2 IN LABELS(s) WHERE label_2 IN ['Software'])
                         RETURN COLLECT(DISTINCT s.name) AS software, log.`name` AS log, 
                                log.event__start AS event__start,
                                log.type AS type, tech.name AS techniques, log.operation AS operation
                         SKIP {iDisplayStart} LIMIT {iDisplayLength}"""

    info_groups = graph.run(query_groups).data()
    info_software = graph.run(query_software).data()
    info_num = graph.run(query_num).data()
    info_list = []
    info_number = []

    for g, s in zip(info_groups, info_software):
        every_info = {}
        every_info.update({'log': g['log']})
        every_info.update({'type': g['type']})
        every_info.update({'event__start': g['event__start']})
        if g['operation'] == None:
            every_info.update({'operation': ''})
        else:
            every_info.update({'operation': g['operation']})
        every_info.update({'techniques': g['techniques']})
        every_info.update({'group': ",".join(g['group'])})
        every_info.update({'software': ",".join(s['software'])})
        info_list.append(every_info)
    # print(json.dumps(info_list, indent=4))
    for text in info_num:
        info_number.append(text['count'])

    return info_list, sum(info_number)


def information_search(node_properties: dict, iDisplayStart: int, iDisplayLength: int):
    """
    情报信息条件查询
    @param node_properties: 查询节点属性
    @param iDisplayStart: 分页开始数
    @param iDisplayLength: 分页数据长度
    @return:
    """

    query_start = f"""MATCH (gs)-[rel_0]->(tech)<-[rel_1]-(rule:`Rule`)<-[rel_2]-(log)
                       WHERE NONE(label_1 IN LABELS(log) WHERE label_1 IN {LABEL_LIST})
                    """
    query_end = f"""WITH log
                    MATCH (log)-[]->(ru:Rule)-[]->(t)<-[]-(gg:Groups)
                    MATCH (log)-[]->(ru:Rule)-[]->(t)<-[]-(ss:Software)
                    RETURN COLLECT(DISTINCT gg.name) AS group, COLLECT(DISTINCT ss.name) AS software,
                           log.`name` AS log, log.type AS type,
                           t.name AS techniques, log.operation AS operation
                    SKIP {iDisplayStart} LIMIT {iDisplayLength}"""
    # query_num = f"""MATCH (rule:`Rule`)<-[rel_2]-(log)
    #                 WHERE NONE(label_1 IN LABELS(log) WHERE label_1 IN {label_list})
    #                 RETURN COUNT(DISTINCT log) AS count
    #              """
    query_end_num = f"""RETURN COUNT(DISTINCT log) AS count"""

    if node_properties.get('name'):
        log_value = f"""AND log.`name`="{node_properties.get('name')}" """
        query_start = query_start + log_value

    if node_properties.get('type'):
        log_type = f"""AND log.type="{node_properties.get('type')}" """
        query_start = query_start + log_type

    if node_properties.get('techniques'):
        techniques = f"""AND tech.name="{node_properties.get('techniques')}" """
        query_start = query_start + techniques

    if node_properties.get('group_or_software'):
        group = f"""AND gs.name="{node_properties.get('group_or_software')}" """
        query_start = query_start + group

    query = query_start + query_end
    query_num = query_start + query_end_num
    # print(query)
    info = graph.run(query).data()
    info_num = graph.run(query_num).data()

    info_list = []
    info_number = []
    for text in info:
        every_info = {}
        every_info.update({'log': text['log']})
        every_info.update({'type': text['type']})
        if text['operation'] == None:
            every_info.update({'operation': ''})
        else:
            every_info.update({'operation': text['operation']})
        every_info.update({'techniques': text['techniques']})
        every_info.update({'group': ",".join(text['group'])})
        every_info.update({'software': ",".join(text['software'])})
        info_list.append(every_info)
    for text in info_num:
        info_number.append(text['count'])

    # print(info_list)
    # print(json.dumps(info_list, indent=4))
    return info_list, sum(info_number)

if __name__ == '__main__':
    # print(information_show(0, 15))
    information_search({
        "log": "c3f70729-6c65-4874-b521-f9d8d2220866",
        "type": "http",
        "operation": "",
        "techniques": "Multi-Factor Authentication Interception",
        # "group_or_software": "Operation Wocao,Kimsuky,Chimera",
        "group_or_software": "Sykipot"
    }, 0, 15)




