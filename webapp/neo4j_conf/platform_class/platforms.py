# -*-coding:utf-8-*-
import json

from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher, Subgraph
from django.conf import settings
from webapp.const import ATTACK_LABEL_LIST

graph = Graph(settings.NEO4J_URL, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))
# graph = Graph("neo4j://localhost:7687", auth=('neo4j', '123456'))


def platforms_search(node_properties: dict, iDisplayStart: int, iDisplayLength: int):
    """
    平台信息查询，通过platforms进行查询相关信息
    @param node_platforms: 平台信息、attack label eg:{'platforms': 'SaaS', 'attack_label': 'Techniques'}
    @param iDisplayStart: 分页开始数
    @param iDisplayLength: 分页数据长度
    @return:
    """
    node_judge = len(node_properties)
    if node_judge == 2:
        query_start = f"""MATCH (n)
                          WHERE n:{node_properties.get('attack_label')}
                          AND n.platforms CONTAINS "{node_properties.get('platforms')}"
                        """
    else:
        query_start = f"""MATCH (n) 
                          WHERE ANY(label_1 IN LABELS(n) WHERE label_1 IN {ATTACK_LABEL_LIST})
                          AND n.platforms CONTAINS "{node_properties.get('platforms')}" """
    query_end = f""" RETURN DISTINCT n.ID, n.name, n.description, n.platforms,
                            n.url, n.created, n.`last modified`, n.version, LABELS(n) AS label,
                            n.industry 
                      SKIP {iDisplayStart} LIMIT {iDisplayLength}
                    """
    query_num = f"""RETURN COUNT(DISTINCT n.name) AS num"""

    info_query = query_start + query_end
    info_num = query_start + query_num
    info = graph.run(info_query).data()
    info_number = list(graph.run(info_num).data()[0].values())[0]
    info_list = []
    for text in info:
        every_info = {}
        every_info.update({'ID': text['n.ID']})
        every_info.update({'name': text['n.name']})
        every_info.update({'description': text['n.description']})
        every_info.update({'platforms': text['n.platforms']})
        every_info.update({'label': "".join(text['label'])})
        every_info.update({'url': text['n.url']})
        every_info.update({'created': text['n.created']})
        every_info.update({'last modified': text['n.`last modified`']})
        every_info.update({'version': text['n.version']})
        if text['n.industry'] == None:
            every_info.update({'industry': ""})
        else:
            every_info.update({'industry': text['n.industry']})
        info_list.append(every_info)
    # print(json.dumps(info_list, indent=4))
    # print(info_number)
    return info_list, info_number


def modify_industry_property(node_properties: dict, modify_info: dict):
    """
    在平台分类页面， 修改平台信息
    @param node_properties: 能够确定这个节点的信息 eg: {'ID': 'T1621'}
    @param modify_info: 节点修改信息 eg: {'platforms': 'SaaS, Windows, macOS'}
    @return:
    """
    node = NodeMatcher(graph).match().where(**node_properties).first()
    node.update(**modify_info)
    graph.push(node)


def platforms_type():
    """
    所有平台信息展示
    @return:
    """
    query = f"""MATCH (n) 
                WHERE ANY(label_1 IN LABELS(n) WHERE label_1 IN {ATTACK_LABEL_LIST})
                RETURN COLLECT(DISTINCT n.platforms) AS plat_list"""
    info = graph.run(query).data()[0].get('plat_list')
    new_info = []
    for x in info:
        for i in x.split(','):
            if i == "":
                continue
            new_info.append(i.strip())
    return list(set(new_info))


if __name__ == '__main__':
    # platforms_search({'platforms': 'SaaS'}, 0, 15)
    # platforms_search({'platforms': 'SaaS', 'attack_label': 'Techniques'}, 0, 15)
    modify_industry_property({'ID': 'T1621', 'name': 'Multi-Factor Authentication Request Generation'},
                          {'platforms': 'SaaS, Windows, macOS'})
    platforms_search({'platforms': 'SaaS', 'attack_label': 'Techniques'}, 0, 15)
    # platforms_type()












