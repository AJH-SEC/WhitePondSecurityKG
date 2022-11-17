# -*-coding:utf-8-*-
import os
from json import dumps
import datetime
import pandas as pd
from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher, Subgraph
from django.conf import settings

graph = Graph(settings.NEO4J_URL, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))
# graph = Graph("neo4j://localhost:7687", auth=('neo4j', '123456'))
matcher = NodeMatcher(graph)

# log_tec_dict = {'log_byte': 'code', 'log_value': '05008', 'tec_ID': 'T1190', 'tec_name': 'Exploit Public-Facing Application'}



def load_rule(rule_data_path):
    """
    导入规则，并创建图
    :param rule_data_path: 规则数据路径
    :return:
    """
    df = pd.read_csv(rule_data_path, encoding='utf-8')
    df = df.fillna('')
    df_header = df.columns
    log_dict = {}

    for index in df.index:
        log_data = df.iloc[index, :]
        map_relation = df.iloc[index, 2]
        tech_id = df.iloc[index, 3]
        tech_name = df.iloc[index, 4]
        log_dict.update({k: str(v).strip() for k, v in zip(df_header, log_data)})
        now_time = datetime.datetime.now().strftime("%d %B %Y")
        log_dict.update({'created': now_time, 'last_modified': now_time})

        result = NodeMatcher(graph).match().where(**log_dict).exists()
        if result == True:
            pass
        else:
            log_node = Node('Rule', **log_dict)
            graph.merge(log_node, 'Rule', 'log_value')

            tech_judge = len(tech_id.split('.'))
            if tech_judge >= 2:
                tech_node = matcher.match('SubTechniques').where(f"_.ID='{tech_id}' or _.name='{tech_name}'").first()
                # print('*'*10,tech_node)
                rule_relation = Relationship(log_node, map_relation, tech_node)
                graph.merge(rule_relation)
            if tech_judge < 2:
                tech_node = matcher.match('Techniques').where(f"_.ID='{tech_id}' or _.name='{tech_name}'").first()
                # print(tech_node)
                rule_relation = Relationship(log_node, map_relation, tech_node)
                graph.merge(rule_relation)


def create_singleRule(node_label, node_properties):
    """
    新建数据，单个规则数据添加 增加节点与关系
    :param node_label: 节点标签
    :param node_properties: 节点属性
    :return:
    """

    result = NodeMatcher(graph).match(node_label).where(**node_properties).exists()
    if result == False:
        node = Node(node_label, **node_properties)
        graph.create(node)

        relation = node_properties.get('attack_model')
        tech_id = node_properties.get('techniques_id')
        tech_name = node_properties.get('techniques_name')
        tech_judge = len(tech_id.split('.'))
        if tech_judge >= 2:
            tech_node = matcher.match('SubTechniques').where(f"_.ID='{tech_id}' or _.name='{tech_name}'").first()
            rule_relation = Relationship(node, relation, tech_node)
            graph.merge(rule_relation)

        if tech_judge < 2:
            tech_node = matcher.match('Techniques').where(f"_.ID='{tech_id}' or _.name='{tech_name}'").first()
            rule_relation = Relationship(node, relation, tech_node)
            graph.merge(rule_relation)


    else:
        # node = NodeMatcher(graph).match(node_label).where(**node_properties).all()
        return "此节点关系已经存在"

def delete_rule(node_label, node_name):
    """
    删除规则
    :param node_label: 节点标签
    :param node_name: 节点name
    :return:
    """
    info = NodeMatcher(graph).match(node_label).where(**node_name).first()
    graph.delete(info)


def show_rule(node_label):
    """
    显示所有规则数据
    :param node_label: 节点标签【Rule】
    :return:
    """
    info = NodeMatcher(graph).match(node_label).all()
    info_list = []
    for text in info:
        info_list.append(dict(text))
    # print(dumps(info_list, ensure_ascii=False, indent=4))
    return info_list


def search_rule(node_label, node_properties):
    """
    查找规则数据
    :param node_label: 节点标签【Rule】
    :param node_properties: 节点属性
    :return:
    """
    info = NodeMatcher(graph).match(node_label).where(**node_properties).all()
    info_list = []
    for text in info:
        info_list.append(dict(text))
    return info_list


def load_graph(rule_data_path):
    """
    将规则数据进行导入图数据库
    :param rule_data_path: 规则数据路径
    :return:
    """
    for file in os.listdir(rule_data_path):
        file_data = os.path.abspath(os.path.join(rule_data_path, file))
        load_rule(file_data)

# if __name__ == '__main__':

    # load_graph('../../static/cache_data/rule_data')












