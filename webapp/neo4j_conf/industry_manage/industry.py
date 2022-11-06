# -*-coding:utf-8-*-
import json
from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher, Subgraph
from django.conf import settings
from webapp.const import ATTACK_LABEL_LIST

graph = Graph(settings.NEO4J_URL, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))
# graph = Graph("neo4j://localhost:7687", auth=('neo4j', '123456'))


def industry_search(node_properties: dict, iDisplayStart: int, iDisplayLength: int):
    """
    行业信息展示
    @param node_properties: 行业信息 eg:{'industry': 'finance', 'attack_label': 'Software'}
    @param iDisplayStart: 分页开始数
    @param iDisplayLength: 分页数据长度
    @return:
    """

    query_start = f"""MATCH (n) 
                      WHERE ANY(label_1 IN LABELS(n) WHERE label_1 IN {ATTACK_LABEL_LIST})
                    """
    query_end = f""" RETURN DISTINCT n.ID, n.name, n.description, n.industry,
                            n.url, n.created, n.`last modified`, n.version, LABELS(n) AS label,
                            n.platforms
                    SKIP {iDisplayStart} LIMIT {iDisplayLength}"""
    query_num = f"""RETURN COUNT(DISTINCT n.name) AS num"""
    if node_properties.get('industry'):
        query_industry = f"""AND n.industry CONTAINS "{node_properties.get('industry')}" """
        query_start = query_start + query_industry
    if node_properties.get('attack_label'):
        query_attack = f"""AND n:{node_properties.get('attack_label')} """
        query_start = query_start + query_attack
    else:
        query_start = query_start

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
        if text['n.industry'] == None:
            every_info.update({'industry': ""})
        else:
            every_info.update({'industry': text['n.industry']})
        every_info.update({'label': "".join(text['label'])})
        every_info.update({'url': text['n.url']})
        every_info.update({'created': text['n.created']})
        every_info.update({'last modified': text['n.`last modified`']})
        every_info.update({'version': text['n.version']})
        every_info.update({'platforms': text['n.platforms']})
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

if __name__ == '__main__':
    # modify_industry_property({'ID': 'S0225'}, {'industry': 'finance'})
    # industry_search({}, 0, 15)
    # industry_search({'industry': 'finance'}, 0, 15)
    # industry_search({'attack_label': 'Software'}, 0, 15)
    industry_search({'industry': 'finance', 'attack_label': 'Software'}, 0, 15)



















