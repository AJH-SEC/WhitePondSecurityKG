# -*-coding:utf-8-*-
import os
import time
from json import dumps
import pandas as pd
from py2neo import Graph, Node, Relationship, NodeMatcher
from django.conf import settings

graph = Graph(settings.NEO4J_URL, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))
# graph = Graph("neo4j://localhost:7687", auth=('neo4j', '123456'))

matcher = NodeMatcher(graph)


def get_techniques(tech_path):
    """
    对技术、子技术数据创建节点，
    同时创建技术与子技术，战术与技术/子技术，技术、子技术与引用链接的关系
    :param tech_path: techniques 文件路径
    :return:
    """
    df = pd.read_csv(tech_path, encoding='utf-8')
    df = df.fillna('')
    df_header = df.columns
    info_dict = {}
    for index in df.index:
        info_all = df.iloc[index, :].copy()
        info = info_all.values

        description = info_all['description']
        if 'description_zh' in info_all:
            description_zh = info_all['description_zh']
            if '中国' in description_zh:
                info_all['description_zh'] = str('')

        if 'China' in description or 'Chinese' in description:
            info_all['description'] = str('')

        if 'name_zh' in info_all:
            info_dict.update({k: str(v) for k, v in zip(df_header, info)})
        else:
            info_dict.update({k: str(v) for k, v in zip(df_header, info)})
            info_dict.update({'name_zh': '', 'description_zh': ''})

        citations_list = info_all['relationship citations'].split('),')

        # 判断是否是子技术
        # 建立子技术节点
        if info_all['is sub-technique'] == True:
            sub_tec_node = Node('SubTechniques', **info_dict)
            graph.create(sub_tec_node)
            
            # 子技术与技术之间的关系
            tech_id = info_all['sub-technique of']
            tech_node = matcher.match('Techniques').where(f"_.ID='{tech_id}'").first()
            ts_relation = Relationship(tech_node, 'sub-techniques of', sub_tec_node)
            graph.create(ts_relation)
            
            # 子技术与战术之间的关系
            tactics_name = info_all['tactics'].split(',')
            for tactic in tactics_name:
                tactic_node = matcher.match('Tactics').where(f"_.name='{tactic.strip()}'").first()
                tts_relation = Relationship(tactic_node, 'tactic of', sub_tec_node)
                graph.create(tts_relation)
            
            # 子技术引用的资源、链接
            for citation in citations_list:
                if citation == '' or citation == ',':
                    continue
                citation = citation.replace('(', '').replace(')', '').split(':')[1].strip()

                citation_node = matcher.match('Citations').where(f'_.reference=~"{citation}"').first()
                sc_relation = Relationship(sub_tec_node, 'citations of', citation_node)
                graph.create(sc_relation)
        
        # 建立技术节点
        if info_all['is sub-technique'] == False:
            tec_node = Node('Techniques', **info_dict)
            graph.create(tec_node)
            # 技术与战术之间的关系
            tactics_name = info_all['tactics'].split(',')
            for tactic in tactics_name:
                tactic_node = matcher.match('Tactics').where(f"_.name='{tactic.strip()}'").first()
                tt_relation = Relationship(tactic_node, 'tactic of', tec_node)
                graph.create(tt_relation)
            # 技术引用的资源、链接
            for citation in citations_list:
                if citation == '' or citation == ',':
                    continue
                citation = citation.replace('(', '').replace(')', '').split(':')[1].strip()
                citation_node = matcher.match('Citations').where(f'_.reference=~"{citation}"').first()

                sc_relation = Relationship(tec_node, 'citations of', citation_node)
                graph.create(sc_relation)


def get_NodeRelation(data_path,
                       subject_label,
                       relation_judge=False,
                       object_label=None,
                       relation_type=None):
    """
    创建相对应的节点信息与节点间的关系
    :param data_path: 数据路径
    :param subject_label: 创建的节点标签
    :param relation_judge: 关系判断，是否需要创建关系
    :param object_label: 匹配的节点标签
    :param relation_type: 建立的关系类型
    :return:
    """
    df = pd.read_csv(data_path, encoding='utf-8')
    df = df.fillna('')
    df_header = df.columns
    info_dict = {}
    for index in df.index:
        info_all = df.iloc[index, :].copy()                # 注意此处pandans数据类型
        info = info_all.values
        
        if 'description' in info_all:
            description = info_all['description']
            if 'China' in description or 'Chinese' in description:
                info_all['description'] = str('')
            info_dict.update({k: str(v).strip() for k, v in zip(df_header, info)})
            info_dict.update({'name_zh': '', 'description_zh': ''})

        if 'description_zh' in info_all:
            description_zh = info_all['description_zh']
            if '中国' in description_zh:
                info_all['description_zh'] = str('')
            info_dict.update({k: str(v).strip() for k, v in zip(df_header, info)})

        else:
            info_dict.update({k: str(v).strip() for k, v in zip(df_header, info)})
            info_dict.update({'name_zh': '',  'description_zh': ''})

        subject_node = Node(subject_label, **info_dict)
        graph.create(subject_node)
        
        # 如果创建关系
        if relation_judge == True:
            citations = info_all['relationship citations']
            if type(citations) == float:
                continue
            if type(citations) == str:
                citations_list = citations.split('),')
                for citation in citations_list:
                    if citation == '' or citation == ',' or citation == ',,':
                        continue
                    citation = citation.replace('(', '').replace(')', '').split(':')[1].strip()
                    object_node = matcher.match(object_label).where(f'_.reference=~"{citation}"').first()
                    relation = Relationship(subject_node, relation_type, object_node)
                    graph.create(relation)


def get_datasources(datasource_path):
    """
    创建数据源与数据组件节点与关系
    :param datasource_path: 数据源路径
    :return:
    """
    df = pd.read_csv(datasource_path, encoding='utf-8')
    df = df.fillna('')
    for index in df.index:
        df_header = list(df.columns)
        info_dict = {}
        info_all = df.iloc[index, :].copy()
        info = info_all.values

        data_judge = info_all['name'].split(':')
        # 数据源与数据组件的判断
        if len(data_judge) >= 2:
            if 'name_zh' in info_all and 'description_zh':
                data_judge_zh = info_all['name_zh'].split('：')
                ds = data_judge[0].strip()

                info[0] = data_judge[1].strip()
                info[1] = data_judge[0].strip()
                df_header[1] = 'datasource'

                datasource_zh = data_judge_zh[0].strip()
                name_zh = data_judge_zh[1].strip()

                info_dict.update({k: str(v) for k, v in zip(df_header, info)})
                info_dict.update({'name_zh': name_zh, 'datasource_zh': datasource_zh})
                # print('z'*3, info_dict)

                ds_component_node = Node('DatasourceComponent', **info_dict)
                graph.create(ds_component_node)

                ds_node = matcher.match('Datasource').where(f"_.name='{ds}'").first()
                dsc_relation = Relationship(ds_node, 'data-component of', ds_component_node)
                graph.create(dsc_relation)
            else:
                ds = data_judge[0].strip()
                info[0] = data_judge[1].strip()
                info[1] = data_judge[0].strip()
                df_header[1] = 'datasource'
                info_dict.update({k: str(v) for k, v in zip(df_header, info)})
                info_dict.update({'name_zh': '', 'datasource_zh': '', 'description_zh': ''})
                # print('e'*6, info_dict)

                ds_component_node = Node('DatasourceComponent', **info_dict)
                graph.create(ds_component_node)

                ds_node = matcher.match('Datasource').where(f"_.name='{ds}'").first()
                dsc_relation = Relationship(ds_node, 'data-component of', ds_component_node)
                graph.create(dsc_relation)

        if len(data_judge) < 2:
            if 'name_zh' in info_all:
                info_dict.update({k: str(v) for k, v in zip(df_header, info)})
            else:
                info_dict.update({k: str(v) for k, v in zip(df_header, info)})
                info_dict.update({'name_zh': '', 'description_zh': ''})
            # print('d'*10, info_dict)

            ds_node = Node('Datasource', **info_dict)
            graph.create(ds_node)


def relationships(relation_path):
    """
    创建关系，数据组件与技术/子技术、缓解措施与技术/子技术、
            组织与软件、组织与技术/子技术、软件与技术/子技术
    :param relation_path: 关系文件路径
    :return:
    """
    df = pd.read_csv(relation_path, encoding='utf-8')
    df = df.fillna('')
    for index in df.index:
        info_all = df.iloc[index, :]
        
        source_name = info_all['source name'].strip()
        target_id = info_all['target ID'].strip()
        mapping_type = info_all['mapping type'].strip()
        source_type = info_all['source type'].strip()
        target_type = info_all['target type'].strip()
        mapping_desc = info_all['mapping description']
        
        # 关系信息
        if 'mapping_description_zh' in info_all:
            mapping_desc_zh = info_all['mapping_description_zh']
            relation_info = {'source type': source_type,
                             'target type': target_type,
                             'mapping description': mapping_desc,
                             'mapping_description_zh': mapping_desc_zh
                             }
        else:
            relation_info = {'source type': source_type,
                             'target type': target_type,
                             'mapping description': mapping_desc
                             }
        id_judge = info_all['target ID'].split('.')

        # 数据组件与技术/子技术
        if info_all['source type'] == 'datacomponent':
            ds_component_node = matcher.match('DatasourceComponent').where(f"_.name=~'{source_name}'").first()
            # print('数据组件与技术/子技术', ds_component_node)
            create_relation(id_judge, target_type, target_id, ds_component_node, mapping_type, relation_info)
        # 缓解措施与技术/子技术
        if info_all['source type'] == 'mitigation':
            mitigation_node = matcher.match('Mitigations').where(f"_.name='{source_name}'").first()
            # print('缓解措施与技术/子技术', mitigation_node)
            create_relation(id_judge, target_type, target_id, mitigation_node, mapping_type, relation_info)
        # 组织与软件、组织与技术/子技术
        if info_all['source type'] == 'group':
            group_node = matcher.match('Groups').where(f"_.name='{source_name}'").first()
            # print('组织与软件、组织与技术/子技术', group_node)
            create_relation(id_judge, target_type, target_id, group_node, mapping_type, relation_info)
        # 软件与技术/子技术
        if info_all['source type'] == 'software':
            software_node = matcher.match('Software').where(f"_.name='{source_name}'").first()
            # print('软件与技术/子技术', source_name, target_id)
            create_relation(id_judge, target_type, target_id, software_node, mapping_type, relation_info)
        # 战役与技术/子技术
        if info_all['source type'] == 'campaign':
            campaign_node = matcher.match('Campaign').where(f"_.name='{source_name}'").first()
            # print('战役与技术/子技术', campaign_node)
            create_relation(id_judge, target_type, target_id, campaign_node, mapping_type, relation_info)


def create_relation(id_judge, target_type, target_id, 
                    source_type_node, mapping_type, relation_info):
    """
    关系判断，与技术和子技术的关系判定、与软件的关系判定
    :param id_judge: 目标id判断，技术、子技术
    :param target_type: 目标节点数据类型
    :param target_id: 目标id
    :param source_type_node: 源数据节点【主节点】
    :param mapping_type: 关系类型
    :param relation_info: 关系信息
    :return:
    """
    if len(id_judge) >= 2 and target_type == 'technique':
        sub_tech_node = matcher.match('SubTechniques').where(f"_.ID='{target_id}'").first()
        dst_relation = Relationship(source_type_node, mapping_type, sub_tech_node, **relation_info)
        graph.create(dst_relation)

    if len(id_judge) < 2 and target_type == 'technique':
        tech_node = matcher.match('Techniques').where(f"_.ID='{target_id}'").first()
        dt_relation = Relationship(source_type_node, mapping_type, tech_node, **relation_info)
        graph.create(dt_relation)

    if len(id_judge) < 2 and target_type == 'software':
        # print(target_id)
        software_node = matcher.match('Software').where(f"_.ID='{target_id}'").first()
        gs_relation = Relationship(source_type_node, mapping_type, software_node, **relation_info)
        graph.create(gs_relation)


def load_graph(cache_path):

    file_set = {}
    for file in os.listdir(cache_path):
        file_name = file.split('.')[0]
        if file_name == 'Enterprise ATT&CK matrix':
            pass
        else:
            file_data = os.path.join(cache_path, file)
            file_set.update({file_name: file_data})

    tactic_path = file_set['tactics']
    citations_path = file_set['citations']
    datasource_path = file_set['datasources']
    software_path = file_set['software']
    groups_path = file_set['groups']
    mitigations_path = file_set['mitigations']
    campaigns_path = file_set['campaigns']

    tech_path = file_set['techniques']
    relation_path = file_set['relationships']
    
    start = time.time()
    try: 
        graph.delete_all()
    except Exception as e:
        print(e)
    get_NodeRelation(tactic_path, 'Tactics')
    tactic = time.time()
    print(f"创建* 战术 *共计时--{tactic-start}")
    get_NodeRelation(citations_path, 'Citations')
    citation = time.time()
    print(f"创建* 引用 *共计时--{citation - tactic}")
    get_datasources(datasource_path)
    datasource = time.time()
    print(f"创建* 数据 *共计时--{datasource - citation}")

    get_NodeRelation(software_path, 'Software', True, 'Citations', 'citations of')
    software = time.time()
    print(f"创建* 软件 *共计时--{software - datasource}")

    get_NodeRelation(groups_path, 'Groups', True, 'Citations', 'citations of')
    groups = time.time()
    print(f"创建* 组织 *共计时--{groups - software}")
    get_NodeRelation(mitigations_path, 'Mitigations', True, 'Citations', 'citations of')
    mitigations = time.time()
    print(f"创建* 缓解措施 *共计时--{mitigations - groups}")
    get_NodeRelation(campaigns_path, 'Campaign', True, 'Citations', 'citations of')
    campaigns = time.time()
    print(f"创建* 战役 *共计时--{campaigns - mitigations}")
    get_techniques(tech_path)
    tech = time.time()
    print(f"创建* 技术/子技术&引用 *共计时--{tech - mitigations}")
    relationships(relation_path)
    relation = time.time()
    # print(f"创建* 关系 *共计时--{relation - tech}")
    print('*'*10,  time.time() - start, end='\n')



if __name__ == '__main__':
    cache_path = '../../static/cache_data'
    load_graph(cache_path)















