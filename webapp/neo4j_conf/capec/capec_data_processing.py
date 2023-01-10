# -*-coding:utf-8-*-
import re
import pandas as pd
import csv
from django.conf import settings
from py2neo import Graph, Node, Relationship, NodeMatcher

graph = Graph(settings.NEO4J_URL, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))
# graph = Graph("neo4j://localhost:7687", auth=('neo4j', '123456'))


def read_capec_related_attack(csv_data, save_file):
    """
    cpaec 数据处理，将capec中ATTACK的技术、子技术ID和name提取出来
    @param csv_data: capec 与 attack 关联数据 eg: '658.csv'
    @param save_file: 保存的文件 eg: 'capec_attack.csv'
    @return:
    """
    csv_file = pd.read_csv(csv_data, index_col=False)
    # 从官网导入的数据 表头ID 问题
    csv_file["'ID"] = 'CAPEC-' + csv_file["'ID"].astype(str)
    csv_file['ID'] = csv_file["'ID"]
    del csv_file["'ID"]

    mapping_ino = csv_file['Taxonomy Mappings'].str
    mapping_ino_list = mapping_ino.split('::').to_list()

    attack_id_list = []
    attack_name_list = []

    # ATTACK 数据处理
    for message in mapping_ino_list:
        tech_id_list = []
        tech_name_list = []
        new_list = []
        for info in message:
            if 'ATTACK' in info:
                new_list.append(info)
        for nn in new_list:
            tech_id_list.append("T" + "".join(re.findall('ENTRY ID:(.+?):ENTRY NAME', nn)))
            tech_name_list.append("".join(re.findall(r'(?<=ENTRY NAME:).*$', nn)))

        attack_id_list.append(",".join(tech_id_list))
        attack_name_list.append(",".join(tech_name_list))

    csv_file['Techniques ID'] = attack_id_list
    csv_file['Techniques name'] = attack_name_list
    csv_file.to_csv(save_file, index=None, index_label=False)


def capec_attack_relation(csv_data):
    """
    capec建立节点，同时与attack技术、子技术 建立关系
    @param csv_data: capec与attack关联数据  eg: '658.csv''
    @return:
    """
    with open(csv_data, 'r', encoding='utf-8') as fr:
        capec_info_list = csv.DictReader(fr)

        for capec in capec_info_list:
            capec_info = dict(capec)
            capec_node = Node('Capec', **capec_info)
            # 建立Capec节点
            graph.merge(capec_node, 'Capec', 'Name')

            # 建立关系
            for tech_id, tech_name in zip(capec_info.get('Techniques ID').split(','), capec_info.get('Techniques name').split(',')):
                tech_node = NodeMatcher(graph).match().where(f"_.ID='{tech_id}' OR _.name='{tech_name}'").first()
                relation = Relationship(tech_node, 'mapping', capec_node)
                graph.merge(relation)

if __name__ == '__main__':
    csv_data = './658.csv'
    save_file = './capec_attack.csv'
    # read_capec_related_attack(csv_data, save_file)
    capec_attack_relation(save_file)














